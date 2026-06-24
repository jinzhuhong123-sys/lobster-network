"""
节点注册中心 - 兼容桥接层

.. deprecated:: 0.4.0
   此模块已弃用。请使用 lobster_network.registry.NodeRegistry（生产级注册中心），
   该版本支持传输通道管理、6级节点状态、原子持久化，并被 messenger.py 和 integration.py 使用。
   本文件仅保留用于向后兼容，将在 v0.5.0 中移除。

此文件不再包含独立实现，而是桥接到生产级 registry.py，
提供旧版 API（NodeRegistration / NodeRegistry）的兼容适配。
"""

import warnings as _warnings
_warnings.warn(
    "network.node_registry 已弃用 (v0.4.0)，请使用 lobster_network.registry",
    DeprecationWarning,
    stacklevel=2,
)

import time
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime
from pathlib import Path

# 从生产级注册中心导入（作为唯一真实实现）
from src.lobster_network.registry import (
    NodeRegistry as _ProductionNodeRegistry,
    RegistrationInfo,
    NodeStatus,
    TransportConfig,
)

# Re-export production classes for code that wants to use them via this path
__all__ = [
    "NodeRegistration",
    "NodeRegistry",
    "RegistrationInfo",
    "NodeStatus",
    "TransportConfig",
]


class NodeRegistration:
    """
    节点注册信息 - 兼容适配代理

    包装生产级 RegistrationInfo，将旧版字段（host / port 等）映射到
    metadata 字典，并通过属性代理实现双向读写：对 NodeRegistration
    属性的修改会直接反映到底层 RegistrationInfo，反之亦然。
    """

    def __init__(self, info: RegistrationInfo):
        object.__setattr__(self, '_info', info)

    # ---- 工厂方法 ----

    @classmethod
    def from_registration_info(cls, info: RegistrationInfo) -> "NodeRegistration":
        """从生产级 RegistrationInfo 构建兼容代理"""
        return cls(info)

    @classmethod
    def from_dict(cls, data: dict) -> "NodeRegistration":
        info = RegistrationInfo.from_dict(data)
        # 旧版 host/port 字段存入 metadata 以保持兼容
        if 'host' in data:
            info.metadata['host'] = data['host']
        if 'port' in data:
            info.metadata['port'] = data['port']
        return cls(info)

    # ---- 属性代理（读） ----

    def __getattr__(self, name: str):
        info = object.__getattribute__(self, '_info')
        if name == 'host':
            return info.metadata.get('host', '')
        if name == 'port':
            return info.metadata.get('port', 0)
        return getattr(info, name)

    # ---- 属性代理（写） ----

    def __setattr__(self, name: str, value):
        info = object.__getattribute__(self, '_info')
        if name == 'host':
            info.metadata['host'] = value
        elif name == 'port':
            info.metadata['port'] = value
        elif hasattr(info, name):
            setattr(info, name, value)
        else:
            object.__setattr__(self, name, value)

    # ---- 序列化 ----

    def to_dict(self) -> dict:
        info = object.__getattribute__(self, '_info')
        return {
            "node_id": info.node_id,
            "name": info.name,
            "node_type": info.node_type,
            "host": info.metadata.get("host", ""),
            "port": info.metadata.get("port", 0),
            "capabilities": info.capabilities,
            "registered_at": info.registered_at,
            "last_heartbeat": info.last_heartbeat,
            "status": info.status,
            "metadata": info.metadata,
            "version": info.version,
        }


class NodeRegistry:
    """
    节点注册中心 - 兼容桥接层

    内部委托给生产级 lobster_network.registry.NodeRegistry，
    同时保留旧版 API（host/port 参数、事件回调、旧版健康检查格式等）。
    """

    def __init__(
        self,
        heartbeat_timeout: int = 60,
        cleanup_interval: int = 30,
        storage_dir: Optional[str] = None,
    ):
        """
        初始化节点注册中心

        Args:
            heartbeat_timeout: 心跳超时时间（秒），超过此时间未收到心跳视为离线
            cleanup_interval: 清理间隔（秒）
            storage_dir: 持久化目录
        """
        self.heartbeat_timeout = heartbeat_timeout
        self.cleanup_interval = cleanup_interval
        self.storage_dir = Path(storage_dir) if storage_dir else None

        # 构建生产级注册中心的 storage_path
        storage_path = None
        if self.storage_dir:
            storage_path = str(self.storage_dir / "registry.json")

        self._registry = _ProductionNodeRegistry(storage_path=storage_path)

        self._callbacks: Dict[str, List[Callable]] = {
            "register": [],
            "deregister": [],
            "heartbeat": [],
            "status_change": [],
        }
        self._running = False
        self._cleanup_thread: Optional[threading.Thread] = None

    # ---- helpers ----

    def _wrap(self, info: RegistrationInfo) -> NodeRegistration:
        """将生产级 RegistrationInfo 包装为旧版 NodeRegistration 代理"""
        return NodeRegistration(info)

    def _trigger_callback(self, event: str, node: NodeRegistration) -> None:
        """触发回调"""
        for callback in self._callbacks.get(event, []):
            try:
                callback(node)
            except Exception as e:
                print(f"回调执行失败 ({event}): {e}")

    # ---- 旧版 API ----

    @property
    def nodes(self) -> Dict[str, NodeRegistration]:
        """兼容旧代码直接访问 .nodes 属性"""
        return {
            nid: self._wrap(info)
            for nid, info in self._registry.nodes.items()
        }

    def register(
        self,
        node_id: str,
        name: str,
        node_type: str = "agent",
        host: str = "",
        port: int = 0,
        capabilities: Optional[List[str]] = None,
        metadata: Optional[Dict] = None,
    ) -> bool:
        """
        注册节点

        Args:
            node_id: 节点ID
            name: 节点名称
            node_type: 节点类型
            host: 主机地址
            port: 端口
            capabilities: 能力列表
            metadata: 元数据

        Returns:
            bool: 是否注册成功
        """
        meta = dict(metadata) if metadata else {}
        if host:
            meta["host"] = host
        if port:
            meta["port"] = port

        self._registry.register(
            node_id=node_id,
            name=name,
            node_type=node_type,
            capabilities=capabilities,
            metadata=meta,
            ttl_seconds=self.heartbeat_timeout,
        )

        node = self.get_node(node_id)
        self._trigger_callback("register", node)
        return True

    def deregister(self, node_id: str) -> bool:
        """
        注销节点

        Args:
            node_id: 节点ID

        Returns:
            bool: 是否注销成功
        """
        node = self.get_node(node_id)
        result = self._registry.unregister(node_id)
        if result and node:
            self._trigger_callback("deregister", node)
        return result

    def heartbeat(self, node_id: str, metadata: Optional[Dict] = None) -> bool:
        """
        节点心跳

        Args:
            node_id: 节点ID
            metadata: 额外元数据

        Returns:
            bool: 心跳是否成功
        """
        result = self._registry.heartbeat(node_id)
        if result:
            # 合并元数据到节点
            info = self._registry.get_node(node_id)
            if info and metadata:
                info.metadata.update(metadata)

            node = self.get_node(node_id)
            if node:
                self._trigger_callback("heartbeat", node)
        return result

    def get_node(self, node_id: str) -> Optional[NodeRegistration]:
        """获取节点信息"""
        info = self._registry.get_node(node_id)
        if info:
            return self._wrap(info)
        return None

    def get_active_nodes(self) -> List[NodeRegistration]:
        """获取所有活跃节点"""
        return [
            self._wrap(info)
            for info in self._registry.nodes.values()
            if info.status == NodeStatus.ACTIVE
        ]

    def get_nodes_by_type(self, node_type: str) -> List[NodeRegistration]:
        """按类型获取节点"""
        return [
            self._wrap(info)
            for info in self._registry.nodes.values()
            if info.node_type == node_type
        ]

    def get_nodes_by_capability(self, capability: str) -> List[NodeRegistration]:
        """按能力获取节点"""
        return [
            self._wrap(info)
            for info in self._registry.nodes.values()
            if capability in info.capabilities
        ]

    def get_inactive_nodes(self) -> List[NodeRegistration]:
        """获取离线节点"""
        return [
            self._wrap(info)
            for info in self._registry.nodes.values()
            if info.status != NodeStatus.ACTIVE
        ]

    def get_registry_status(self) -> Dict:
        """获取注册中心状态"""
        active = len([
            n for n in self._registry.nodes.values()
            if n.status == NodeStatus.ACTIVE
        ])
        inactive = len([
            n for n in self._registry.nodes.values()
            if n.status in (NodeStatus.IDLE, NodeStatus.DEGRADED, "inactive")
        ])
        dead = len([
            n for n in self._registry.nodes.values()
            if n.status in (NodeStatus.OFFLINE, "dead")
        ])

        return {
            "total_nodes": len(self._registry.nodes),
            "active_nodes": active,
            "inactive_nodes": inactive,
            "dead_nodes": dead,
            "heartbeat_timeout": self.heartbeat_timeout,
            "nodes": {
                nid: self._wrap(info).to_dict()
                for nid, info in self._registry.nodes.items()
            },
        }

    def check_health(self) -> Dict:
        """
        检查所有节点健康状态（旧版格式）

        使用 heartbeat_timeout 阈值将节点标记为 inactive（>1x）或 dead（>2x）。

        Returns:
            Dict: 健康检查结果
        """
        now = datetime.now()
        unhealthy = []

        for node_id, info in self._registry.nodes.items():
            try:
                last_hb_str = info.last_heartbeat.replace('Z', '').split('+')[0]
                fmt = "%Y-%m-%dT%H:%M:%S.%f" if '.' in last_hb_str else "%Y-%m-%dT%H:%M:%S"
                last_hb = datetime.strptime(last_hb_str, fmt)
                elapsed = (now - last_hb).total_seconds()

                if elapsed > self.heartbeat_timeout * 2:
                    info.status = "dead"
                    unhealthy.append(node_id)
                    self._trigger_callback("status_change", self._wrap(info))
                elif elapsed > self.heartbeat_timeout:
                    info.status = "inactive"
                    unhealthy.append(node_id)
                    self._trigger_callback("status_change", self._wrap(info))
            except (ValueError, TypeError):
                pass

        return {
            "total": len(self._registry.nodes),
            "healthy": len(self._registry.nodes) - len(unhealthy),
            "unhealthy": len(unhealthy),
            "unhealthy_nodes": unhealthy,
        }

    def on(self, event: str, callback: Callable) -> None:
        """
        注册事件回调

        Args:
            event: 事件类型 (register|deregister|heartbeat|status_change)
            callback: 回调函数
        """
        if event in self._callbacks:
            self._callbacks[event].append(callback)

    def start_cleanup(self) -> None:
        """启动定期清理线程"""
        self._running = True
        self._cleanup_thread = threading.Thread(target=self._cleanup_loop, daemon=True)
        self._cleanup_thread.start()

    def stop_cleanup(self) -> None:
        """停止定期清理线程"""
        self._running = False

    def _cleanup_loop(self) -> None:
        """清理循环"""
        while self._running:
            try:
                self.check_health()
            except Exception as e:
                print(f"清理循环异常: {e}")
            time.sleep(self.cleanup_interval)

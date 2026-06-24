"""
节点注册中心
提供节点注册、发现、心跳、健康检查、持久化存储
"""

import json
import os
import uuid
import threading
from typing import Dict, List, Optional, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict

from src.lobster_network.utils.logger import get_logger

logger = get_logger(__name__)


# 节点状态枚举
class NodeStatus:
    ACTIVE = "active"        # 活跃
    IDLE = "idle"            # 空闲（在线但无任务）
    BUSY = "busy"            # 忙碌
    DEGRADED = "degraded"    # 降级（部分功能不可用）
    OFFLINE = "offline"      # 离线
    SUSPECTED = "suspected"  # 疑似离线（心跳超时但未确认）


# 传输通道类型
class TransportType:
    NFS = "nfs"
    HTTP = "http"
    SSH = "ssh"
    REDIS = "redis"
    FILE = "file"  # 本地文件兜底


@dataclass
class TransportConfig:
    """传输通道配置"""
    transport_type: str
    endpoint: str  # URL、路径等
    enabled: bool = True
    priority: int = 0  # 优先级，数字越小优先级越高
    last_error: Optional[str] = None
    last_success_at: Optional[str] = None
    
    def to_dict(self) -> dict:
        return asdict(self)


def _parse_time(s: str) -> datetime:
    """解析 ISO 时间字符串（兼容 Python 3.6+）"""
    s = s.replace('Z', '').split('+')[0]
    fmt = "%Y-%m-%dT%H:%M:%S.%f" if '.' in s else "%Y-%m-%dT%H:%M:%S"
    return datetime.strptime(s, fmt)


@dataclass
class RegistrationInfo:
    """注册信息"""
    node_id: str
    name: str
    node_type: str
    registered_at: str
    last_heartbeat: str
    status: str = NodeStatus.ACTIVE
    capabilities: List[str] = field(default_factory=list)
    transports: List[TransportConfig] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)
    version: str = "1.0.0"
    ttl_seconds: int = 300  # 默认5分钟心跳超时
    
    def to_dict(self) -> dict:
        return {
            "node_id": self.node_id,
            "name": self.name,
            "node_type": self.node_type,
            "registered_at": self.registered_at,
            "last_heartbeat": self.last_heartbeat,
            "status": self.status,
            "capabilities": self.capabilities,
            "transports": [t.to_dict() for t in self.transports],
            "metadata": self.metadata,
            "version": self.version,
            "ttl_seconds": self.ttl_seconds,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "RegistrationInfo":
        transports = [TransportConfig(**t) for t in data.get("transports", [])]
        return cls(
            node_id=data["node_id"],
            name=data["name"],
            node_type=data.get("node_type", "agent"),
            registered_at=data.get("registered_at", datetime.now().isoformat()),
            last_heartbeat=data.get("last_heartbeat", datetime.now().isoformat()),
            status=data.get("status", NodeStatus.ACTIVE),
            capabilities=data.get("capabilities", []),
            transports=transports,
            metadata=data.get("metadata", {}),
            version=data.get("version", "1.0.0"),
            ttl_seconds=data.get("ttl_seconds", 300),
        )
    
    def is_alive(self) -> bool:
        """检查节点是否还活着（心跳未超时）"""
        try:
            last = _parse_time(self.last_heartbeat)
            return (datetime.now() - last).total_seconds() < self.ttl_seconds
        except (ValueError, TypeError):
            return False


class NodeRegistry:
    """
    节点注册中心
    
    功能：
    1. 节点注册与注销
    2. 心跳检测与健康检查
    3. 节点发现与查询
    4. 传输通道管理与故障切换
    5. 持久化存储
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        """
        初始化注册中心
        
        Args:
            storage_path: 持久化存储路径，None 则仅内存模式
        """
        self.nodes: Dict[str, RegistrationInfo] = {}
        self.storage_path = storage_path
        self._lock = threading.RLock()
        self._heartbeat_callbacks: List = []
        self._status_change_callbacks: List = []
        
        # 从持久化存储加载
        if storage_path and os.path.exists(storage_path):
            self._load()
        
        logger.info(f"NodeRegistry initialized (storage={storage_path or 'memory-only'})")
    
    # ==================== 注册与注销 ====================
    
    def register(
        self,
        node_id: str,
        name: str,
        node_type: str = "agent",
        capabilities: Optional[List[str]] = None,
        transports: Optional[List[TransportConfig]] = None,
        metadata: Optional[Dict] = None,
        ttl_seconds: int = 300,
    ) -> RegistrationInfo:
        """
        注册节点
        
        Args:
            node_id: 节点唯一标识
            name: 节点名称
            node_type: 节点类型
            capabilities: 能力列表
            transports: 传输通道配置
            metadata: 元数据
            ttl_seconds: 心跳超时时间（秒）
        
        Returns:
            RegistrationInfo: 注册信息
        """
        with self._lock:
            now = datetime.now().isoformat()
            
            info = RegistrationInfo(
                node_id=node_id,
                name=name,
                node_type=node_type,
                registered_at=now,
                last_heartbeat=now,
                capabilities=capabilities or [],
                transports=transports or [],
                metadata=metadata or {},
                ttl_seconds=ttl_seconds,
            )
            
            was_existing = node_id in self.nodes
            self.nodes[node_id] = info
            
            self._save()
            logger.info(f"Node registered: {node_id} ({name}) {'[updated]' if was_existing else '[new]'}")
            
            return info
    
    def unregister(self, node_id: str) -> bool:
        """
        注销节点
        
        Args:
            node_id: 节点ID
        
        Returns:
            bool: 是否成功注销
        """
        with self._lock:
            if node_id in self.nodes:
                del self.nodes[node_id]
                self._save()
                logger.info(f"Node unregistered: {node_id}")
                return True
            return False
    
    # ==================== 心跳 ====================
    
    def heartbeat(self, node_id: str, status: Optional[str] = None) -> bool:
        """
        节点心跳
        
        Args:
            node_id: 节点ID
            status: 可选的状态更新
        
        Returns:
            bool: 是否成功
        """
        with self._lock:
            if node_id not in self.nodes:
                logger.warning(f"Heartbeat from unregistered node: {node_id}")
                return False
            
            node = self.nodes[node_id]
            old_status = node.status
            node.last_heartbeat = datetime.now().isoformat()
            
            if status:
                node.status = status
            
            self._save()
            
            # 触发心跳回调
            for cb in self._heartbeat_callbacks:
                try:
                    cb(node_id, node)
                except Exception as e:
                    logger.error(f"Heartbeat callback error: {e}")
            
            # 状态变化回调
            if status and status != old_status:
                for cb in self._status_change_callbacks:
                    try:
                        cb(node_id, old_status, status)
                    except Exception as e:
                        logger.error(f"Status change callback error: {e}")
            
            return True
    
    def on_heartbeat(self, callback) -> None:
        """注册心跳回调"""
        self._heartbeat_callbacks.append(callback)
    
    def on_status_change(self, callback) -> None:
        """注册状态变化回调"""
        self._status_change_callbacks.append(callback)
    
    # ==================== 节点发现 ====================
    
    def get_node(self, node_id: str) -> Optional[RegistrationInfo]:
        """获取节点注册信息"""
        with self._lock:
            return self.nodes.get(node_id)
    
    def is_alive(self, node_id: str) -> bool:
        """检查节点是否在线"""
        node = self.get_node(node_id)
        if not node:
            return False
        return node.is_alive()
    
    def list_nodes(
        self,
        node_type: Optional[str] = None,
        status: Optional[str] = None,
        alive_only: bool = False,
    ) -> List[RegistrationInfo]:
        """
        列出节点
        
        Args:
            node_type: 按类型过滤
            status: 按状态过滤
            alive_only: 只返回在线节点
        
        Returns:
            List[RegistrationInfo]: 节点列表
        """
        with self._lock:
            result = list(self.nodes.values())
            
            if node_type:
                result = [n for n in result if n.node_type == node_type]
            if status:
                result = [n for n in result if n.status == status]
            if alive_only:
                result = [n for n in result if n.is_alive()]
            
            return result
    
    def find_by_capability(self, capability: str) -> List[RegistrationInfo]:
        """
        按能力查找节点
        
        Args:
            capability: 能力名称
        
        Returns:
            List[RegistrationInfo]: 匹配的节点列表
        """
        with self._lock:
            return [
                n for n in self.nodes.values()
                if capability in n.capabilities and n.is_alive()
            ]
    
    def get_active_transports(self, node_id: str) -> List[TransportConfig]:
        """
        获取节点可用的传输通道（按优先级排序）
        
        Args:
            node_id: 节点ID
        
        Returns:
            List[TransportConfig]: 可用传输通道
        """
        node = self.get_node(node_id)
        if not node:
            return []
        
        available = [t for t in node.transports if t.enabled]
        available.sort(key=lambda t: t.priority)
        return available
    
    def mark_transport_failed(self, node_id: str, transport_type: str, error: str) -> None:
        """
        标记传输通道失败
        
        Args:
            node_id: 节点ID
            transport_type: 传输类型
            error: 错误信息
        """
        node = self.get_node(node_id)
        if not node:
            return
        
        with self._lock:
            for t in node.transports:
                if t.transport_type == transport_type:
                    t.last_error = error
                    t.enabled = False
                    logger.warning(f"Transport {transport_type} disabled for {node_id}: {error}")
                    break
            self._save()
    
    def mark_transport_ok(self, node_id: str, transport_type: str) -> None:
        """
        标记传输通道正常
        
        Args:
            node_id: 节点ID
            transport_type: 传输类型
        """
        node = self.get_node(node_id)
        if not node:
            return
        
        with self._lock:
            for t in node.transports:
                if t.transport_type == transport_type:
                    t.enabled = True
                    t.last_error = None
                    t.last_success_at = datetime.now().isoformat()
                    break
            self._save()
    
    # ==================== 健康检查 ====================
    
    def check_health(self) -> Dict:
        """
        全量健康检查
        
        Returns:
            Dict: 健康状态报告
        """
        with self._lock:
            now = datetime.now()
            report = {
                "total_nodes": len(self.nodes),
                "active": 0,
                "online": 0,
                "offline": 0,
                "suspected": 0,
                "nodes": {},
            }
            
            for node_id, node in self.nodes.items():
                node_health = {
                    "name": node.name,
                    "status": node.status,
                    "last_heartbeat": node.last_heartbeat,
                    "is_alive": node.is_alive(),
                    "transports": len([t for t in node.transports if t.enabled]),
                }
                
                if node.is_alive():
                    report["online"] += 1
                    if node.status == NodeStatus.ACTIVE:
                        report["active"] += 1
                else:
                    # 心跳超时
                    if node.status not in (NodeStatus.OFFLINE, NodeStatus.SUSPECTED):
                        node.status = NodeStatus.SUSPECTED
                        logger.warning(f"Node {node_id} suspected offline (heartbeat timeout)")
                    report["suspected"] += 1
                
                report["nodes"][node_id] = node_health
            
            # 标记长时间未心跳的节点为 offline
            for node_id, node in self.nodes.items():
                try:
                    last = _parse_time(node.last_heartbeat)
                    if (now - last).total_seconds() > node.ttl_seconds * 3:
                        if node.status != NodeStatus.OFFLINE:
                            node.status = NodeStatus.OFFLINE
                            report["offline"] += 1
                            report["suspected"] -= 1
                            logger.warning(f"Node {node_id} marked offline")
                except (ValueError, TypeError):
                    pass
            
            self._save()
            return report
    
    # ==================== 持久化 ====================
    
    def _save(self) -> None:
        """持久化到文件"""
        if not self.storage_path:
            return
        
        try:
            os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
            data = {
                "version": "1.0",
                "saved_at": datetime.now().isoformat(),
                "nodes": {
                    nid: info.to_dict()
                    for nid, info in self.nodes.items()
                },
            }
            # 原子写入：先写临时文件再重命名
            tmp_path = self.storage_path + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            os.replace(tmp_path, self.storage_path)
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")
    
    def _load(self) -> None:
        """从文件加载"""
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for node_id, node_data in data.get("nodes", {}).items():
                self.nodes[node_id] = RegistrationInfo.from_dict(node_data)
            
            logger.info(f"Registry loaded: {len(self.nodes)} nodes from {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to load registry: {e}")
    
    def export_registry(self) -> str:
        """导出注册表为 JSON"""
        with self._lock:
            return json.dumps({
                nid: info.to_dict()
                for nid, info in self.nodes.items()
            }, ensure_ascii=False, indent=2)
    
    def get_statistics(self) -> Dict:
        """获取注册中心统计"""
        with self._lock:
            type_counts = {}
            status_counts = {}
            for node in self.nodes.values():
                type_counts[node.node_type] = type_counts.get(node.node_type, 0) + 1
                status_counts[node.status] = status_counts.get(node.status, 0) + 1
            
            return {
                "total_nodes": len(self.nodes),
                "by_type": type_counts,
                "by_status": status_counts,
                "online": sum(1 for n in self.nodes.values() if n.is_alive()),
            }

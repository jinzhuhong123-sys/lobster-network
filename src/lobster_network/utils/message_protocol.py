"""
消息协议定义 (v1) - 兼容桥接层

.. deprecated:: 0.4.0
   v1 协议已弃用。推荐升级路径：
   - 增强功能（去重、TTL、重试）→ utils.message_protocol_v2.MessageProtocolV2
   - 生产级可靠消息 → messenger.Messenger + messenger.ReliableMessage
   本文件仅保留用于向后兼容，将在 v0.5.0 中移除。

此文件不再包含独立实现，而是桥接到 message_protocol_v2，
将 v1 的 Message / MessageProtocol 映射到 v2 实现。
"""

import warnings as _warnings
_warnings.warn(
    "utils.message_protocol (v1) 已弃用 (v0.4.0)，"
    "请使用 message_protocol_v2 或 messenger.Messenger",
    DeprecationWarning,
    stacklevel=2,
)

from typing import Dict, List, Optional

# 从 v2 导入作为唯一真实实现（Message 完全向后兼容，新增字段均有默认值）
from src.lobster_network.utils.message_protocol_v2 import (
    Message,
    MessageProtocol as _V2MessageProtocol,
)

# Re-export Message so existing ``from .message_protocol import Message`` keeps working
__all__ = ["Message", "MessageProtocol"]


class MessageProtocol:
    """
    消息协议处理器 - v1 兼容桥接

    内部委托给 message_protocol_v2.MessageProtocol，
    保留 v1 的精简 API（无 priority / ttl / confirmed 参数）。
    """

    def __init__(self):
        """初始化消息协议（无持久化）"""
        self._v2 = _V2MessageProtocol(storage_dir=None)

    @property
    def message_history(self) -> List[Message]:
        """兼容旧代码直接访问 .message_history"""
        return self._v2.message_history

    def create_message(
        self,
        from_node: str,
        to_node: str,
        msg_type: str,
        payload: Dict,
        reply_to: Optional[str] = None,
    ) -> Message:
        """
        创建消息

        Args:
            from_node: 发送节点
            to_node: 接收节点
            msg_type: 消息类型
            payload: 消息载荷
            reply_to: 回复的消息ID

        Returns:
            Message: 消息对象
        """
        msg = self._v2.create_message(
            from_node=from_node,
            to_node=to_node,
            msg_type=msg_type,
            payload=payload,
            reply_to=reply_to,
        )
        # v2 对重复消息返回 None；v1 始终返回 Message 对象。
        # 桥接层保持 v1 语义：若被去重则重新创建（极端情况下兜底）。
        if msg is None:
            msg = Message(
                msg_id=f"msg-{__import__('uuid').uuid4().hex[:12]}",
                from_node=from_node,
                to_node=to_node,
                msg_type=msg_type,
                payload=payload,
                reply_to=reply_to,
            )
            self._v2.message_history.append(msg)
        return msg

    def validate_message(self, message: Message) -> bool:
        """
        验证消息

        Args:
            message: 消息对象

        Returns:
            bool: 是否有效
        """
        return self._v2.validate_message(message)

    def get_messages(
        self,
        from_node: Optional[str] = None,
        to_node: Optional[str] = None,
        msg_type: Optional[str] = None,
    ) -> List[Message]:
        """
        获取消息列表

        Args:
            from_node: 发送节点过滤
            to_node: 接收节点过滤
            msg_type: 消息类型过滤

        Returns:
            List[Message]: 消息列表
        """
        return self._v2.get_messages(
            from_node=from_node,
            to_node=to_node,
            msg_type=msg_type,
        )

    def get_statistics(self) -> Dict:
        """
        获取消息统计信息（v1 格式）

        Returns:
            Dict: 统计信息
        """
        v2_stats = self._v2.get_statistics()
        # 返回 v1 精简格式，同时保留 v2 扩展字段
        return {
            "total_messages": v2_stats["total_messages"],
            "type_counts": v2_stats["type_counts"],
        }

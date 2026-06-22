"""
消息协议定义
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Message:
    """小龙虾网络消息"""
    msg_id: str
    from_node: str
    to_node: str
    msg_type: str  # dialogue_trigger|training_task|emergence_report|heartbeat
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    payload: Dict = field(default_factory=dict)
    reply_to: Optional[str] = None
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "msg_id": self.msg_id,
            "from": self.from_node,
            "to": self.to_node,
            "type": self.msg_type,
            "timestamp": self.timestamp,
            "payload": self.payload,
            "reply_to": self.reply_to,
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """从字典创建消息"""
        return cls(
            msg_id=data["msg_id"],
            from_node=data["from"],
            to_node=data["to"],
            msg_type=data["type"],
            timestamp=data.get("timestamp", datetime.now().isoformat()),
            payload=data.get("payload", {}),
            reply_to=data.get("reply_to"),
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        """从JSON字符串创建消息"""
        return cls.from_dict(json.loads(json_str))


class MessageProtocol:
    """消息协议处理器"""
    
    def __init__(self):
        """初始化消息协议"""
        self.message_history: List[Message] = []
    
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
        msg_id = f"msg-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        message = Message(
            msg_id=msg_id,
            from_node=from_node,
            to_node=to_node,
            msg_type=msg_type,
            payload=payload,
            reply_to=reply_to,
        )
        
        self.message_history.append(message)
        return message
    
    def validate_message(self, message: Message) -> bool:
        """
        验证消息
        
        Args:
            message: 消息对象
        
        Returns:
            bool: 是否有效
        """
        required_fields = ["msg_id", "from", "to", "type", "timestamp", "payload"]
        
        data = message.to_dict()
        for field in required_fields:
            if field not in data:
                return False
        
        return True
    
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
        messages = self.message_history
        
        if from_node:
            messages = [m for m in messages if m.from_node == from_node]
        if to_node:
            messages = [m for m in messages if m.to_node == to_node]
        if msg_type:
            messages = [m for m in messages if m.msg_type == msg_type]
        
        return messages
    
    def get_statistics(self) -> Dict:
        """
        获取消息统计信息
        
        Returns:
            Dict: 统计信息
        """
        type_counts = {}
        for msg in self.message_history:
            type_counts[msg.msg_type] = type_counts.get(msg.msg_type, 0) + 1
        
        return {
            "total_messages": len(self.message_history),
            "type_counts": type_counts,
        }

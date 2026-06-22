"""
小龙虾网络主类
"""

from typing import Dict, List, Optional
from .node import Node
from .dialogue import DialogueEngine, DialogueResult
from .emergence import EmergenceDetector
from .world_state import WorldStateManager


class LobsterNetwork:
    """小龙虾网络（因陀罗网拓扑）"""
    
    def __init__(self, emergence_threshold: float = 0.5):
        """
        初始化小龙虾网络
        
        Args:
            emergence_threshold: 涌现阈值
        """
        self.nodes: Dict[str, Node] = {}
        self.dialogue_engine = DialogueEngine(emergence_threshold=emergence_threshold)
        self.emergence_detector = EmergenceDetector(threshold=emergence_threshold)
        self.world_state_manager = WorldStateManager()
    
    def add_node(self, node: Node) -> None:
        """
        添加节点
        
        Args:
            node: 节点对象
        """
        self.nodes[node.node_id] = node
        self.world_state_manager.get_state(node.node_id)
    
    def remove_node(self, node_id: str) -> None:
        """
        移除节点
        
        Args:
            node_id: 节点ID
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
    
    def get_node(self, node_id: str) -> Optional[Node]:
        """
        获取节点
        
        Args:
            node_id: 节点ID
        
        Returns:
            Optional[Node]: 节点对象
        """
        return self.nodes.get(node_id)
    
    def dialogue(self, node_a_id: str, node_b_id: str, trigger: str = "") -> DialogueResult:
        """
        触发两个节点之间的对话
        
        Args:
            node_a_id: 节点A ID
            node_b_id: 节点B ID
            trigger: 触发事件描述
        
        Returns:
            DialogueResult: 对话结果
        """
        node_a = self.nodes.get(node_a_id)
        node_b = self.nodes.get(node_b_id)
        
        if not node_a or not node_b:
            raise ValueError(f"节点不存在: {node_a_id} 或 {node_b_id}")
        
        # 触发对话
        result = self.dialogue_engine.dialogue(node_a, node_b, trigger)
        
        # 检测涌现
        event = self.emergence_detector.detect(result)
        
        # 更新世界状态
        if event:
            self.world_state_manager.update_state(
                node_a_id,
                treasure_id=event.treasure_unlocked,
            )
            self.world_state_manager.update_state(
                node_b_id,
                treasure_id=event.treasure_unlocked,
            )
        
        return result
    
    def get_emergence_statistics(self) -> Dict:
        """获取涌现统计信息"""
        return self.emergence_detector.get_statistics()
    
    def get_network_topology(self) -> Dict:
        """获取网络拓扑"""
        return {
            node_id: {
                "name": node.name,
                "type": node.type,
                "perspective": node.seed["perspective"],
                "world_version": node.current_world["version"],
            }
            for node_id, node in self.nodes.items()
        }
    
    def export_network_state(self) -> str:
        """导出网络状态为JSON字符串"""
        import json
        return json.dumps({
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "emergence_statistics": self.get_emergence_statistics(),
            "world_states": json.loads(self.world_state_manager.export_states()),
        }, ensure_ascii=False, indent=2)

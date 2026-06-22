"""
小龙虾网络单元测试
"""

import sys
import os
import json
import unittest
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.lobster_network.lobster_network import LobsterNetwork
from src.lobster_network.node import Node
from src.lobster_network.dialogue import DialogueEngine, DialogueResult
from src.lobster_network.emergence import EmergenceDetector
from src.lobster_network.world_state import WorldStateManager


class TestNode(unittest.TestCase):
    """Node 节点测试"""
    
    def setUp(self):
        self.node = Node(
            node_id='test-001',
            name='测试节点',
            node_type='agent',
            perspective='测试视角',
            knowledge_base='测试知识库',
            value_orientation='测试价值',
            learning_rate='high',
            capabilities=['test1', 'test2'],
        )
    
    def test_node_creation(self):
        """测试节点创建"""
        self.assertEqual(self.node.node_id, 'test-001')
        self.assertEqual(self.node.name, '测试节点')
        self.assertEqual(self.node.type, 'agent')
        self.assertEqual(self.node.seed['perspective'], '测试视角')
        self.assertEqual(self.node.seed['knowledge_base'], '测试知识库')
        self.assertEqual(self.node.capabilities, ['test1', 'test2'])
    
    def test_node_default_values(self):
        """测试默认值"""
        node = Node(node_id='test-002', name='默认节点')
        self.assertEqual(node.type, 'agent')
        self.assertEqual(node.seed['learning_rate'], 'medium')
        self.assertEqual(node.capabilities, [])
    
    def test_node_to_dict(self):
        """测试序列化为字典"""
        d = self.node.to_dict()
        self.assertIn('node_id', d)
        self.assertIn('name', d)
        self.assertIn('type', d)
        self.assertIn('seed', d)
        self.assertIn('capabilities', d)
        self.assertIn('current_world', d)
        self.assertIn('spawned_at', d)
        self.assertEqual(d['node_id'], 'test-001')
    
    def test_node_to_json(self):
        """测试序列化为 JSON"""
        j = self.node.to_json()
        self.assertIsInstance(j, str)
        parsed = json.loads(j)
        self.assertEqual(parsed['node_id'], 'test-001')
    
    def test_node_from_dict(self):
        """测试从字典反序列化"""
        d = self.node.to_dict()
        node2 = Node.from_dict(d)
        self.assertEqual(node2.node_id, 'test-001')
        self.assertEqual(node2.name, '测试节点')
        self.assertEqual(node2.type, 'agent')
        self.assertEqual(node2.seed['perspective'], '测试视角')
    
    def test_node_update_world(self):
        """测试世界状态更新"""
        self.assertEqual(self.node.current_world['version'], 0)
        self.node.update_world(chunk_id='chunk_1', treasure_id='t1')
        self.assertEqual(self.node.current_world['version'], 1)
        self.assertEqual(len(self.node.current_world['loaded_chunks']), 1)
        self.assertEqual(len(self.node.current_world['unlocked_treasures']), 1)
        
        # 重复更新不会重复添加
        self.node.update_world(chunk_id='chunk_1', treasure_id='t1')
        self.assertEqual(self.node.current_world['version'], 2)
        self.assertEqual(len(self.node.current_world['loaded_chunks']), 1)
    
    def test_node_repr(self):
        """测试 repr"""
        r = repr(self.node)
        self.assertIn('test-001', r)
        self.assertIn('测试节点', r)


class TestDialogueEngine(unittest.TestCase):
    """DialogueEngine 测试"""
    
    def test_dialogue_engine_creation(self):
        """测试对话引擎创建"""
        de = DialogueEngine(emergence_threshold=0.5)
        self.assertEqual(de.emergence_threshold, 0.5)


class TestEmergenceDetector(unittest.TestCase):
    """EmergenceDetector 测试"""
    
    def test_emergence_detector_creation(self):
        """测试涌现检测器创建"""
        ed = EmergenceDetector(threshold=0.5)
        self.assertEqual(ed.threshold, 0.5)


class TestWorldStateManager(unittest.TestCase):
    """WorldStateManager 测试"""
    
    def test_world_state_manager_creation(self):
        """测试世界状态管理器创建"""
        ws = WorldStateManager()
        self.assertIsNotNone(ws)


class TestLobsterNetwork(unittest.TestCase):
    """LobsterNetwork 核心测试"""
    
    def setUp(self):
        self.net = LobsterNetwork(emergence_threshold=0.5)
    
    def test_network_creation(self):
        """测试网络创建"""
        self.assertIsNotNone(self.net)
        self.assertIsNotNone(self.net.dialogue_engine)
        self.assertIsNotNone(self.net.emergence_detector)
        self.assertIsNotNone(self.net.world_state_manager)
        self.assertEqual(len(self.net.nodes), 0)
    
    def test_add_node(self):
        """测试添加节点"""
        node = Node(node_id='n1', name='测试节点', node_type='agent')
        self.net.add_node(node)
        self.assertEqual(len(self.net.nodes), 1)
        self.assertIn('n1', self.net.nodes)
    
    def test_remove_node(self):
        """测试移除节点"""
        node = Node(node_id='n1', name='测试节点')
        self.net.add_node(node)
        self.assertEqual(len(self.net.nodes), 1)
        
        self.net.remove_node('n1')
        self.assertEqual(len(self.net.nodes), 0)
    
    def test_remove_nonexistent_node(self):
        """测试移除不存在的节点"""
        self.net.remove_node('nonexistent')
        self.assertEqual(len(self.net.nodes), 0)
    
    def test_add_multiple_nodes(self):
        """测试添加多个节点"""
        nodes = [
            ('lobster-001', '虾尔', 'agent', '世界地图渲染'),
            ('hermes', '诸葛马', 'coach', '架构师'),
            ('xiaochen', '小陈', 'student', '文档维护'),
        ]
        for nid, name, ntype, pers in nodes:
            self.net.add_node(Node(node_id=nid, name=name, node_type=ntype, perspective=pers))
        
        self.assertEqual(len(self.net.nodes), 3)
        self.assertIn('lobster-001', self.net.nodes)
        self.assertIn('hermes', self.net.nodes)
        self.assertIn('xiaochen', self.net.nodes)
        
        # 验证节点属性
        xiaer = self.net.nodes['lobster-001']
        self.assertEqual(xiaer.name, '虾尔')
        self.assertEqual(xiaer.type, 'agent')
        self.assertEqual(xiaer.seed['perspective'], '世界地图渲染')
    
    def test_node_serialization_roundtrip(self):
        """测试节点序列化往返"""
        node = Node(
            node_id='n1',
            name='测试节点',
            node_type='agent',
            perspective='测试',
            capabilities=['cap1'],
        )
        self.net.add_node(node)
        
        # 序列化
        d = self.net.nodes['n1'].to_dict()
        # 反序列化
        node2 = Node.from_dict(d)
        
        self.assertEqual(node2.node_id, 'n1')
        self.assertEqual(node2.name, '测试节点')
        self.assertEqual(node2.type, 'agent')
    
    def test_network_emergence_threshold(self):
        """测试网络涌现阈值"""
        net2 = LobsterNetwork(emergence_threshold=0.8)
        self.assertEqual(net2.emergence_detector.threshold, 0.8)
    
    def test_world_state_update_via_network(self):
        """测试通过网络更新世界状态"""
        node = Node(node_id='n1', name='测试节点')
        self.net.add_node(node)
        self.net.nodes['n1'].update_world(chunk_id='test_chunk')
        self.assertEqual(self.net.nodes['n1'].current_world['version'], 1)
        self.assertEqual(len(self.net.nodes['n1'].current_world['loaded_chunks']), 1)


class TestIndraNet(unittest.TestCase):
    """IndraNet 因陀罗网测试"""
    
    def test_indra_net_import(self):
        """测试 IndraNet 可导入"""
        from src.network.indra_net import IndraNet, IndraNetNode
        self.assertIsNotNone(IndraNet)
        self.assertIsNotNone(IndraNetNode)
    
    def test_indra_net_creation(self):
        """测试因陀罗网创建"""
        from src.network.indra_net import IndraNet
        net = IndraNet()
        self.assertIsNotNone(net)
        self.assertEqual(len(net.nodes), 0)
    
    def test_indra_net_add_nodes(self):
        """测试添加节点到因陀罗网"""
        from src.network.indra_net import IndraNet, IndraNetNode
        
        net = IndraNet()
        
        node_a = IndraNetNode(
            node_id="xiaochen",
            name="信电大虾",
            node_type="agent",
            perspective="技术栈",
            knowledge_base="代码、文档、技术诊断",
        )
        node_b = IndraNetNode(
            node_id="zhuguma",
            name="诸葛马",
            node_type="coach",
            perspective="教练型",
            knowledge_base="训练计划、验证门控",
        )
        
        net.add_node(node_a)
        net.add_node(node_b)
        
        self.assertEqual(len(net.nodes), 2)
        
        # 自动全互联
        self.assertIn('zhuguma', net.get_connections('xiaochen'))
        self.assertIn('xiaochen', net.get_connections('zhuguma'))
    
    def test_indra_net_statistics(self):
        """测试因陀罗网统计"""
        from src.network.indra_net import IndraNet, IndraNetNode
        
        net = IndraNet()
        
        for i in range(3):
            node = IndraNetNode(
                node_id=f'node_{i}',
                name=f'节点{i}',
                node_type='agent',
                perspective='测试',
                knowledge_base='测试',
            )
            net.add_node(node)
        
        stats = net.get_statistics()
        self.assertEqual(stats['total_nodes'], 3)
        self.assertGreater(stats['total_connections'], 0)


if __name__ == '__main__':
    unittest.main()

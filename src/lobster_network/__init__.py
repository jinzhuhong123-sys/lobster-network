"""
小龙虾网络 - 统一入口
Lobster Network - Unified Entry Point

对话即创造：一人一世界的世界观

v0.5.0 变更:
- 新增: 8维度能力评估引擎 (EightDimEngine)，参考 Clawvard School 评估体系
- 新增: 维度画像 (DimensionProfile)、Clawvard桥接 (ClawvardBridge)
- 新增: 评估维度定义、评分器、改进建议生成器
- 注意: network/node_registry.py 已弃用，请使用 registry.py

v0.4.0 变更:
- 新增: 节点注册中心 (NodeRegistry)、可靠消息 (Messenger)、集成层 (LobsterNetworkWithRegistry)
- 新增: SSH通道v2 (SSHChannelV2)、消息协议v2 (MessageProtocolV2)
"""

# 框架层 (Framework Layer)
from .node import Node
from .dialogue import DialogueEngine, DialogueResult
from .emergence import EmergenceDetector, EmergenceEvent
from .world_state import WorldState, WorldStateManager
from .lobster_network import LobsterNetwork

# 网络层 (Network Layer)
from .network.indra_net import IndraNet, IndraNetNode
from .network.ssh_channel import SSHChannel

# 工具层 (Utility Layer)
from .utils.config import NetworkConfig, ConfigManager
from .utils.logger import LobsterLogger, get_logger
from .utils.message_protocol import Message, MessageProtocol

# 套利层 (Arbitrage Layer)
from .time_arbitrage import (
    TimeArbitrageEngine, ArbitrageType, NodeSpeedProfile,
    ArbitrageOpportunity, ArbitrageResult, ForgettingCurve,
)

# v0.4.0 通信层 (Communication Layer)
from .registry import (
    NodeRegistry, RegistrationInfo, NodeStatus,
    TransportConfig, TransportType,
)
from .messenger import (
    Messenger, ReliableMessage, MessageStatus,
    NFSTransport, FileTransport,
)
from .integration import LobsterNetworkWithRegistry

# v0.4.0 增强模块（可选导入，避免循环依赖）
try:
    from .utils.message_protocol_v2 import (
        Message as MessageV2,
        MessageProtocol as MessageProtocolV2,
    )
    from .network.ssh_channel_v2 import SSHChannel as SSHChannelV2
except ImportError:
    pass  # v2 模块为可选增强

# v0.5.0 8维度评估层 (Assessment Layer) — 可选导入
try:
    from .assessment import (
        EightDimEngine, AssessmentResult,
        DimensionProfile, Dimension,
        ClawvardBridge, PracticeSession,
        DIMENSION_REGISTRY, DIMENSION_DESCRIPTIONS, DIMENSION_WEIGHTS,
    )
except ImportError:
    pass  # assessment 模块为可选增强

__version__ = "0.5.0"
__all__ = [
    # Core
    "Node", "DialogueEngine", "DialogueResult",
    "EmergenceDetector", "EmergenceEvent",
    "WorldState", "WorldStateManager",
    "LobsterNetwork",
    # Network
    "IndraNet", "IndraNetNode", "SSHChannel",
    # Arbitrage
    "TimeArbitrageEngine", "ArbitrageType", "NodeSpeedProfile",
    "ArbitrageOpportunity", "ArbitrageResult", "ForgettingCurve",
    # Utils
    "NetworkConfig", "ConfigManager",
    "LobsterLogger", "get_logger",
    "Message", "MessageProtocol",
    # v0.4.0 Communication Layer
    "NodeRegistry", "RegistrationInfo", "NodeStatus",
    "TransportConfig", "TransportType",
    "Messenger", "ReliableMessage", "MessageStatus",
    "NFSTransport", "FileTransport",
    "LobsterNetworkWithRegistry",
    # v0.5.0 Assessment Layer
    "EightDimEngine", "AssessmentResult",
    "DimensionProfile", "Dimension",
    "ClawvardBridge", "PracticeSession",
    "DIMENSION_REGISTRY", "DIMENSION_DESCRIPTIONS", "DIMENSION_WEIGHTS",
]

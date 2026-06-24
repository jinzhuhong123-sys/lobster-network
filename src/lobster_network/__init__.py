"""
小龙虾网络 - 统一入口
Lobster Network - Unified Entry Point

对话即创造：一人一世界的世界观
"""

__version__ = "0.4.1"

# 框架层 (Framework Layer)
from .node import Node
from .dialogue import DialogueEngine, DialogueResult
from .emergence import EmergenceDetector, EmergenceEvent
from .world_state import WorldState, WorldStateManager
from .lobster_network import LobsterNetwork

# 网络层 (Network Layer)
from .network.indra_net import IndraNet, IndraNetNode
from .network.ssh_channel import SSHChannel
from .network.ssh_channel_v2 import SSHChannel as SSHChannelV2
from .network.ssh_transport import SSHTransport

# 可靠通信层 (Reliable Communication Layer) - v0.4.1 新增
from .registry import NodeRegistry, RegistrationInfo, TransportConfig, NodeStatus
from .messenger import Messenger, ReliableMessage, MessageStatus, MessageAttempt
from .integration import LobsterNetworkWithRegistry

# 工具层 (Utility Layer)
from .utils.config import NetworkConfig, ConfigManager
from .utils.logger import LobsterLogger, get_logger
from .utils.message_protocol_v2 import Message as MessageV2, MessageProtocol as MessageProtocolV2
from .utils.message_protocol import Message as LegacyMessage, MessageProtocol as LegacyMessageProtocol

# 套利层 (Arbitrage Layer)
from .time_arbitrage import (
    TimeArbitrageEngine, ArbitrageType, NodeSpeedProfile,
    ArbitrageOpportunity, ArbitrageResult, ForgettingCurve,
)

# 别名（向后兼容）
Message = MessageV2  # v2 作为默认
MessageProtocol = MessageProtocolV2  # v2 作为默认

__all__ = [
    # Version
    "__version__",
    # Core
    "Node", "DialogueEngine", "DialogueResult",
    "EmergenceDetector", "EmergenceEvent",
    "WorldState", "WorldStateManager",
    "LobsterNetwork",
    # Network
    "IndraNet", "IndraNetNode",
    "SSHChannel", "SSHChannelV2", "SSHTransport",
    # Reliable Communication (v0.4.1)
    "NodeRegistry", "RegistrationInfo", "TransportConfig", "NodeStatus",
    "Messenger", "ReliableMessage", "MessageStatus", "MessageAttempt",
    "LobsterNetworkWithRegistry",
    # Message Protocol (v2 默认)
    "Message", "MessageProtocol",  # v2 (推荐)
    "MessageV2", "MessageProtocolV2",  # v2 显式
    "LegacyMessage", "LegacyMessageProtocol",  # v1 (兼容)
    # Arbitrage
    "TimeArbitrageEngine", "ArbitrageType", "NodeSpeedProfile",
    "ArbitrageOpportunity", "ArbitrageResult", "ForgettingCurve",
    # Utils
    "NetworkConfig", "ConfigManager",
    "LobsterLogger", "get_logger",
]

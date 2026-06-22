"""
小龙虾网络 - 统一入口
Lobster Network - Unified Entry Point

对话即创造：一人一世界的世界观
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

__version__ = "0.3.0"
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
]

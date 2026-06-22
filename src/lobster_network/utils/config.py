"""
配置管理模块
"""

import os
import json
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class NetworkConfig:
    """网络配置"""
    # SSH配置
    ssh_host: str = ""
    ssh_user: str = "admin"
    ssh_port: int = 22
    ssh_key: str = "~/.ssh/id_rsa"
    
    # 共享目录
    shared_dir: str = "/shared/messages"
    
    # 涌现阈值
    emergence_threshold: float = 0.5
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "lobster_network.log"
    
    # 网络配置
    network_name: str = "lobster-network"
    network_version: str = "0.2.0"
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "ssh_host": self.ssh_host,
            "ssh_user": self.ssh_user,
            "ssh_port": self.ssh_port,
            "ssh_key": self.ssh_key,
            "shared_dir": self.shared_dir,
            "emergence_threshold": self.emergence_threshold,
            "log_level": self.log_level,
            "log_file": self.log_file,
            "network_name": self.network_name,
            "network_version": self.network_version,
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> "NetworkConfig":
        """从字典创建配置"""
        return cls(
            ssh_host=data.get("ssh_host", ""),
            ssh_user=data.get("ssh_user", "admin"),
            ssh_port=data.get("ssh_port", 22),
            ssh_key=data.get("ssh_key", "~/.ssh/id_rsa"),
            shared_dir=data.get("shared_dir", "/shared/messages"),
            emergence_threshold=data.get("emergence_threshold", 0.5),
            log_level=data.get("log_level", "INFO"),
            log_file=data.get("log_file", "lobster_network.log"),
            network_name=data.get("network_name", "lobster-network"),
            network_version=data.get("network_version", "0.2.0"),
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> "NetworkConfig":
        """从JSON字符串创建配置"""
        return cls.from_dict(json.loads(json_str))
    
    @classmethod
    def from_file(cls, file_path: str) -> "NetworkConfig":
        """从文件加载配置"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())
    
    def save_to_file(self, file_path: str) -> None:
        """保存配置到文件"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())


class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config: Optional[NetworkConfig] = None):
        """
        初始化配置管理器
        
        Args:
            config: 配置对象，如果为None则使用默认配置
        """
        self.config = config or NetworkConfig()
    
    def get_config(self) -> NetworkConfig:
        """获取配置"""
        return self.config
    
    def update_config(self, **kwargs) -> None:
        """
        更新配置
        
        Args:
            **kwargs: 配置键值对
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
    
    def get_ssh_config(self) -> Dict:
        """获取SSH配置"""
        return {
            "host": self.config.ssh_host,
            "user": self.config.ssh_user,
            "port": self.config.ssh_port,
            "key": self.config.ssh_key,
        }
    
    def get_network_config(self) -> Dict:
        """获取网络配置"""
        return {
            "name": self.config.network_name,
            "version": self.config.network_version,
            "emergence_threshold": self.config.emergence_threshold,
        }
    
    def export_config(self) -> str:
        """导出配置为JSON字符串"""
        return self.config.to_json()
    
    def save_config(self, file_path: str) -> None:
        """保存配置到文件"""
        self.config.save_to_file(file_path)
    
    def load_config(self, file_path: str) -> None:
        """从文件加载配置"""
        self.config = NetworkConfig.from_file(file_path)

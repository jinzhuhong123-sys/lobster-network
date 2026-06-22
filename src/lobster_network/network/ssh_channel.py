"""
SSH通信通道模块
实现跨服务器/跨VPC的双向通信
"""

import os
import subprocess
import json
from typing import Dict, List, Optional
from datetime import datetime


class SSHChannel:
    """SSH通信通道"""
    
    def __init__(
        self,
        remote_host: str,
        remote_user: str = "admin",
        remote_port: int = 22,
        ssh_key: str = "~/.ssh/id_rsa",
        shared_dir: str = "/shared/messages",
    ):
        """
        初始化SSH通道
        
        Args:
            remote_host: 远程服务器地址
            remote_user: 远程用户名
            remote_port: SSH端口
            ssh_key: SSH密钥路径
            shared_dir: 共享消息目录
        """
        self.remote_host = remote_host
        self.remote_user = remote_user
        self.remote_port = remote_port
        self.ssh_key = os.path.expanduser(ssh_key)
        self.shared_dir = shared_dir
        self.to_dir = f"{shared_dir}/to_{remote_host}"
        self.from_dir = f"{shared_dir}/from_{remote_host}"
    
    def setup_directories(self) -> bool:
        """
        创建共享目录
        
        Returns:
            bool: 是否成功
        """
        try:
            os.makedirs(self.to_dir, exist_ok=True)
            os.makedirs(self.from_dir, exist_ok=True)
            
            # 在远程服务器创建目录
            cmd = [
                "ssh", "-i", self.ssh_key, "-p", str(self.remote_port),
                f"{self.remote_user}@{self.remote_host}",
                f"mkdir -p {self.shared_dir}/to_lobster {self.shared_dir}/from_lobster"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"创建目录失败: {e}")
            return False
    
    def send_message(self, message: Dict) -> bool:
        """
        发送消息到远程服务器
        
        Args:
            message: 消息字典
        
        Returns:
            bool: 是否成功
        """
        try:
            # 生成消息文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"msg_{timestamp}.json"
            local_path = f"{self.to_dir}/{filename}"
            remote_path = f"{self.shared_dir}/to_lobster/{filename}"
            
            # 写入本地文件
            with open(local_path, 'w', encoding='utf-8') as f:
                json.dump(message, f, ensure_ascii=False, indent=2)
            
            # 通过SCP发送到远程服务器
            cmd = [
                "scp", "-i", self.ssh_key, "-P", str(self.remote_port),
                local_path,
                f"{self.remote_user}@{self.remote_host}:{remote_path}"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"发送消息失败: {e}")
            return False
    
    def receive_message(self) -> Optional[Dict]:
        """
        从远程服务器接收消息
        
        Returns:
            Optional[Dict]: 消息字典，如果没有消息返回None
        """
        try:
            # 从远程服务器拉取消息
            cmd = [
                "scp", "-i", self.ssh_key, "-P", str(self.remote_port),
                f"{self.remote_user}@{self.remote_host}:{self.shared_dir}/from_lobster/*.json",
                self.from_dir
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return None
            
            # 读取最新消息
            files = sorted([f for f in os.listdir(self.from_dir) if f.endswith('.json')])
            if not files:
                return None
            
            latest_file = files[-1]
            file_path = f"{self.from_dir}/{latest_file}"
            
            with open(file_path, 'r', encoding='utf-8') as f:
                message = json.load(f)
            
            # 删除已读取的消息文件
            os.remove(file_path)
            
            return message
        except Exception as e:
            print(f"接收消息失败: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        测试SSH连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            cmd = [
                "ssh", "-i", self.ssh_key, "-p", str(self.remote_port),
                f"{self.remote_user}@{self.remote_host}",
                "echo 'Connection successful'"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            print(f"连接测试失败: {e}")
            return False
    
    def get_status(self) -> Dict:
        """
        获取通道状态
        
        Returns:
            Dict: 通道状态信息
        """
        return {
            "remote_host": self.remote_host,
            "remote_user": self.remote_user,
            "remote_port": self.remote_port,
            "shared_dir": self.shared_dir,
            "to_dir": self.to_dir,
            "from_dir": self.from_dir,
            "connection_test": self.test_connection(),
        }

"""
日志系统模块
"""

import logging
import os
from datetime import datetime
from typing import Optional


class LobsterLogger:
    """小龙虾网络日志器"""
    
    def __init__(
        self,
        name: str = "lobster_network",
        log_level: str = "INFO",
        log_file: Optional[str] = None,
    ):
        """
        初始化日志器
        
        Args:
            name: 日志器名称
            log_level: 日志级别
            log_file: 日志文件路径，如果为None则只输出到控制台
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, log_level.upper()))
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 控制台handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, log_level.upper()))
            
            # 格式
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
            
            # 文件handler
            if log_file:
                # 确保日志目录存在
                log_dir = os.path.dirname(log_file)
                if log_dir:
                    os.makedirs(log_dir, exist_ok=True)
                
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(getattr(logging, log_level.upper()))
                file_handler.setFormatter(formatter)
                
                self.logger.addHandler(file_handler)
    
    def debug(self, message: str) -> None:
        """记录DEBUG级别日志"""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """记录INFO级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """记录WARNING级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """记录ERROR级别日志"""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """记录CRITICAL级别日志"""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """记录异常日志"""
        self.logger.exception(message)
    
    def log_dialogue(
        self,
        from_node: str,
        to_node: str,
        emergence_score: float,
        new_insight: str,
    ) -> None:
        """
        记录对话日志
        
        Args:
            from_node: 发送节点
            to_node: 接收节点
            emergence_score: 涌现值
            new_insight: 新见解
        """
        self.info(
            f"对话: {from_node} → {to_node} | "
            f"涌现值: {emergence_score:.2f} | "
            f"新见解: {new_insight}"
        )
    
    def log_emergence(
        self,
        event_id: str,
        emergence_score: float,
        treasure_unlocked: Optional[str] = None,
    ) -> None:
        """
        记录涌现事件日志
        
        Args:
            event_id: 事件ID
            emergence_score: 涌现值
            treasure_unlocked: 解锁的宝藏ID
        """
        message = f"涌现事件: {event_id} | 涌现值: {emergence_score:.2f}"
        if treasure_unlocked:
            message += f" | 解锁宝藏: {treasure_unlocked}"
        self.info(message)
    
    def log_ssh_event(
        self,
        event_type: str,
        remote_host: str,
        success: bool,
        message: str = "",
    ) -> None:
        """
        记录SSH事件日志
        
        Args:
            event_type: 事件类型（send|receive|connect|disconnect）
            remote_host: 远程主机
            success: 是否成功
            message: 附加消息
        """
        status = "成功" if success else "失败"
        log_message = f"SSH {event_type}: {remote_host} | 状态: {status}"
        if message:
            log_message += f" | 消息: {message}"
        
        if success:
            self.info(log_message)
        else:
            self.error(log_message)


# 全局日志器实例
_global_logger: Optional[LobsterLogger] = None


def get_logger(
    name: str = "lobster_network",
    log_level: str = "INFO",
    log_file: Optional[str] = None,
) -> LobsterLogger:
    """
    获取全局日志器实例
    
    Args:
        name: 日志器名称
        log_level: 日志级别
        log_file: 日志文件路径
    
    Returns:
        LobsterLogger: 日志器实例
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = LobsterLogger(name, log_level, log_file)
    return _global_logger

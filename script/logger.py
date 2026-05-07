#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
日志模块
提供统一的日志配置和管理
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from script.paths import LOGS_DIR, ensure_dir


# 日志格式
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 日志文件名格式
LOG_FILENAME = "app.log"


def setup_logger(
    name: str = "pyqt-exe-template",
    level: int = logging.INFO,
    log_to_file: bool = True,
    log_to_console: bool = True
) -> logging.Logger:
    """
    设置并返回日志器
    
    Args:
        name: 日志器名称
        level: 日志级别
        log_to_file: 是否写入文件
        log_to_console: 是否输出到控制台
        
    Returns:
        logging.Logger: 配置好的日志器
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 清除现有的 handlers
    logger.handlers.clear()
    
    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    
    # 控制台输出
    if log_to_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 文件输出
    if log_to_file:
        # 确保日志目录存在
        ensure_dir(LOGS_DIR)
        
        # 日志文件路径
        log_file = LOGS_DIR / LOG_FILENAME
        
        file_handler = logging.FileHandler(
            log_file,
            encoding='utf-8',
            mode='a'  # 追加模式
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "pyqt-exe-template") -> logging.Logger:
    """
    获取已配置的日志器
    
    Args:
        name: 日志器名称
        
    Returns:
        logging.Logger: 日志器实例
    """
    return logging.getLogger(name)


# 全局日志器实例
_logger: Optional[logging.Logger] = None


def init_logging() -> logging.Logger:
    """
    初始化全局日志系统
    
    Returns:
        logging.Logger: 全局日志器
    """
    global _logger
    if _logger is None:
        _logger = setup_logger()
    return _logger


def log_info(message: str) -> None:
    """记录 INFO 级别日志"""
    logger = get_logger()
    logger.info(message)


def log_debug(message: str) -> None:
    """记录 DEBUG 级别日志"""
    logger = get_logger()
    logger.debug(message)


def log_warning(message: str) -> None:
    """记录 WARNING 级别日志"""
    logger = get_logger()
    logger.warning(message)


def log_error(message: str) -> None:
    """记录 ERROR 级别日志"""
    logger = get_logger()
    logger.error(message)


def log_exception(message: str) -> None:
    """记录 EXCEPTION 级别日志（包含堆栈信息）"""
    logger = get_logger()
    logger.exception(message)
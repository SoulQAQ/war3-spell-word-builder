#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
路径处理模块
统一处理开发环境和 PyInstaller 打包环境的路径问题
"""

import sys
from pathlib import Path
from typing import Optional


def get_app_dir() -> Path:
    """
    获取应用程序根目录
    
    在开发环境下返回项目根目录
    在 PyInstaller 打包后返回 exe 所在目录
    
    Returns:
        Path: 应用程序根目录
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后的路径
        return Path(sys.executable).resolve().parent
    else:
        # 开发环境路径 - script 目录的上一级
        return Path(__file__).resolve().parent.parent


def get_resource_dir() -> Path:
    """
    获取资源文件目录
    
    在开发环境下返回项目根目录下的 resources
    在 PyInstaller 打包后返回临时解压目录下的 resources
    
    Returns:
        Path: 资源文件目录
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后使用 _MEIPASS 临时目录
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            return Path(meipass) / 'resources'
        else:
            return get_app_dir() / 'resources'
    else:
        # 开发环境
        return get_app_dir() / 'resources'


def get_config_dir() -> Path:
    """
    获取配置文件目录
    
    Returns:
        Path: 配置文件目录
    """
    if getattr(sys, 'frozen', False):
        # 打包后配置在 exe 同级的 config 目录
        return get_app_dir() / 'config'
    else:
        # 开发环境
        return get_app_dir() / 'config'


def get_rundata_dir() -> Path:
    """
    获取运行数据目录
    
    Returns:
        Path: undata 目录
    """
    return get_app_dir() / 'rundata'


def get_logs_dir() -> Path:
    """
    获取日志目录
    
    Returns:
        Path: 日志目录
    """
    return get_rundata_dir() / 'logs'


def get_input_dir() -> Path:
    """
    获取输入目录
    
    Returns:
        Path: 输入目录
    """
    return get_rundata_dir() / 'input'


def get_output_dir() -> Path:
    """
    获取输出目录
    
    Returns:
        Path: 输出目录
    """
    return get_rundata_dir() / 'output'


def resource_path(relative_path: str) -> Path:
    """
    获取资源文件的完整路径
    
    Args:
        relative_path: 相对于 resources 目录的路径
        
    Returns:
        Path: 资源文件的完整路径
    """
    return get_resource_dir() / relative_path


def config_path(relative_path: str) -> Path:
    """
    获取配置文件的完整路径
    
    Args:
        relative_path: 相对于 config 目录的路径
        
    Returns:
        Path: 配置文件的完整路径
    """
    return get_config_dir() / relative_path


def ensure_dir(path: Path) -> Path:
    """
    确保目录存在，不存在则创建
    
    Args:
        path: 目录路径
        
    Returns:
        Path: 目录路径
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def normalize_path(path: str) -> Path:
    """
    将路径字符串标准化为 Path 对象
    
    Args:
        path: 路径字符串
        
    Returns:
        Path: Path 对象
    """
    if not path:
        return get_app_dir()
    return Path(path).resolve()


# 预定义常用路径常量
APP_DIR: Path = get_app_dir()
RESOURCE_DIR: Path = get_resource_dir()
CONFIG_DIR: Path = get_config_dir()
RUNDATA_DIR: Path = get_rundata_dir()
LOGS_DIR: Path = get_logs_dir()
INPUT_DIR: Path = get_input_dir()
OUTPUT_DIR: Path = get_output_dir()
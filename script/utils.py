#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
工具函数模块
提供通用工具函数
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union

from script.paths import APP_DIR


def open_folder(path: Union[str, Path]) -> bool:
    """
    在系统文件管理器中打开文件夹
    
    Args:
        path: 文件夹路径
        
    Returns:
        bool: 是否成功打开
    """
    try:
        path_obj = Path(path)
        if not path_obj.exists():
            path_obj.mkdir(parents=True, exist_ok=True)
        
        if sys.platform == 'win32':
            os.startfile(str(path_obj))
        elif sys.platform == 'darwin':
            subprocess.run(['open', str(path_obj)])
        else:
            subprocess.run(['xdg-open', str(path_obj)])
        return True
    except Exception as e:
        print(f"Failed to open folder: {e}")
        return False


def safe_json_loads(text: str, default: Any = None) -> Any:
    """
    安全地解析 JSON 字符串
    
    Args:
        text: JSON 字符串
        default: 解析失败时的默认返回值
        
    Returns:
        Any: 解析结果或默认值
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError, ValueError):
        return default


def format_json(data: Any, indent: int = 2, ensure_ascii: bool = False) -> str:
    """
    格式化 JSON 数据为字符串
    
    Args:
        data: 要格式化的数据
        indent: 缩进空格数
        ensure_ascii: 是否转义非 ASCII 字符
        
    Returns:
        str: 格式化后的 JSON 字符串
    """
    try:
        return json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)
    except (TypeError, ValueError):
        return str(data)


def current_timestamp(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间戳字符串
    
    Args:
        fmt: 时间格式
        
    Returns:
        str: 格式化的时间戳
    """
    return datetime.now().strftime(fmt)


def current_datetime() -> datetime:
    """
    获取当前 datetime 对象
    
    Returns:
        datetime: 当前时间
    """
    return datetime.now()


def ensure_absolute_path(path: Union[str, Path], base_dir: Optional[Path] = None) -> Path:
    """
    确保路径为绝对路径
    
    Args:
        path: 输入路径
        base_dir: 相对路径的基准目录，默认为应用根目录
        
    Returns:
        Path: 绝对路径
    """
    path_obj = Path(path)
    if path_obj.is_absolute():
        return path_obj
    
    base = base_dir or APP_DIR
    return (base / path_obj).resolve()


def relative_to_app(path: Union[str, Path]) -> str:
    """
    将路径转换为相对于应用根目录的相对路径
    
    Args:
        path: 输入路径
        
    Returns:
        str: 相对路径字符串
    """
    try:
        path_obj = Path(path).resolve()
        return str(path_obj.relative_to(APP_DIR))
    except ValueError:
        return str(path)


def truncate_string(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断字符串
    
    Args:
        text: 原始字符串
        max_length: 最大长度
        suffix: 截断后缀
        
    Returns:
        str: 截断后的字符串
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_bytes(size: int, precision: int = 2) -> str:
    """
    格式化字节数为人类可读格式
    
    Args:
        size: 字节数
        precision: 小数位数
        
    Returns:
        str: 格式化后的字符串
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size_float = float(size)
    
    for unit in units[:-1]:
        if size_float < 1024:
            return f"{size_float:.{precision}f} {unit}"
        size_float /= 1024
    
    return f"{size_float:.{precision}f} {units[-1]}"


def format_duration(seconds: float) -> str:
    """
    格式化时长
    
    Args:
        seconds: 秒数
        
    Returns:
        str: 格式化后的时长字符串
    """
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}h {minutes}m"


def deep_update(base_dict: Dict, update_dict: Dict) -> Dict:
    """
    深度更新字典
    
    Args:
        base_dict: 基础字典
        update_dict: 更新字典
        
    Returns:
        Dict: 更新后的字典
    """
    result = base_dict.copy()
    
    for key, value in update_dict.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_update(result[key], value)
        else:
            result[key] = value
    
    return result
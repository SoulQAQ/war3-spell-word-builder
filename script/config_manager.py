#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
配置管理模块
支持 YAML 格式配置的读写操作
"""

import copy
import sys
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError as exc:
    raise RuntimeError("缺少 PyYAML 依赖，请先执行: pip install pyyaml") from exc

from script.paths import APP_DIR, CONFIG_DIR, ensure_dir


class ConfigManager:
    """配置管理器，负责配置文件的读写和默认值管理"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，默认为 config/setting.yaml
        """
        if config_path is None:
            self.config_path = CONFIG_DIR / 'setting.yaml'
        else:
            self.config_path = Path(config_path)
        
        self.app_dir = APP_DIR
        self._config: Dict[str, Any] = {}
        self._defaults: Dict[str, Any] = self._get_defaults()

    def _get_defaults(self) -> Dict[str, Any]:
        """获取默认配置"""
        return {
            'app': {
                'name': 'war3技能文本生成器',
                'version': '1.0.0',
                'language': 'en-US',
            },
            'window': {
                'width': 1100,
                'height': 720,
                'minimum_width': 900,
                'minimum_height': 600,
                'remember_geometry': True,
                'geometry': '',
                'state': '',
            },
            'network': {
                'timeout': 30,
                'retry_count': 2,
                'default_url': 'https://httpbin.org/get',
            },
            'user_settings': {
                'input_path': './rundata/input',
                'output_path': './rundata/output',
            },
            'features': {
                'enable_logs': True,
                'enable_status_bar': True,
                'enable_modern_style': True,
            },
            'ui': {
                'theme': 'dark',
                'accent_color': '#4F8CFF',
            },
        }

    def load(self) -> Dict[str, Any]:
        """
        加载配置文件
        
        Returns:
            配置字典，合并了默认值和文件配置
        """
        if not self.config_path.exists():
            self._config = copy.deepcopy(self._defaults)
            self.save()
            return self._config

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                file_config = yaml.safe_load(f) or {}
        except Exception:
            file_config = {}

        # 深度合并默认配置和文件配置
        self._config = self._deep_merge(self._defaults, file_config)
        return self._config

    def save(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        保存配置到文件
        
        Args:
            config: 要保存的配置字典，默认保存当前配置
        """
        if config is not None:
            self._config = config

        # 确保目录存在
        ensure_dir(self.config_path.parent)

        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(self._config, f, allow_unicode=True, sort_keys=False)

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值（支持点分隔的嵌套键）
        
        Args:
            key: 配置键，如 'user_settings.input_path'
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def set(self, key: str, value: Any, auto_save: bool = True) -> None:
        """
        设置配置值
        
        Args:
            key: 配置键，如 'user_settings.input_path'
            value: 配置值
            auto_save: 是否自动保存到文件
        """
        keys = key.split('.')
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

        if auto_save:
            self.save()

    def resolve_path(self, path_value: str) -> str:
        """
        将相对路径解析为绝对路径
        
        Args:
            path_value: 路径值（相对或绝对）
            
        Returns:
            绝对路径字符串
        """
        if not path_value:
            return ''

        path_obj = Path(path_value)
        if not path_obj.is_absolute():
            path_obj = (self.app_dir / path_value).resolve()

        return str(path_obj)

    def normalize_path(self, path_value: str) -> str:
        """
        将路径规范化为相对于项目根目录的相对路径
        
        Args:
            path_value: 路径值
            
        Returns:
            相对路径字符串
        """
        if not path_value:
            return ''

        path_obj = Path(path_value)
        if not path_obj.is_absolute():
            path_obj = (self.app_dir / path_value).resolve()
        else:
            path_obj = path_obj.resolve()

        try:
            relative = path_obj.relative_to(self.app_dir)
            return relative.as_posix() or '.'
        except ValueError:
            import os
            return os.path.relpath(path_obj, self.app_dir).replace('\\', '/')

    @staticmethod
    def _deep_merge(base: Dict, override: Dict) -> Dict:
        """深度合并两个字典"""
        result = copy.deepcopy(base)

        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigManager._deep_merge(result[key], value)
            else:
                result[key] = copy.deepcopy(value)

        return result

    def get_all(self) -> Dict[str, Any]:
        """
        获取所有配置
        
        Returns:
            Dict: 配置字典
        """
        return copy.deepcopy(self._config)

    def reload(self) -> Dict[str, Any]:
        """
        重新加载配置文件
        
        Returns:
            Dict: 配置字典
        """
        return self.load()

    def reset_to_defaults(self) -> None:
        """重置为默认配置"""
        self._config = copy.deepcopy(self._defaults)
        self.save()


# 全局配置管理器实例
_config_manager: Optional[ConfigManager] = None


def get_config_manager() -> ConfigManager:
    """获取全局配置管理器实例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
        _config_manager.load()
    return _config_manager

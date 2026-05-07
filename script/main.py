#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyQt EXE Template - 程序入口
主程序启动文件
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
# 这样无论从哪里运行，都能正确导入 script 模块
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from script.paths import APP_DIR, RESOURCE_DIR, resource_path, ensure_dir, LOGS_DIR
from script.logger import init_logging, get_logger
from script.config_manager import get_config_manager


def load_stylesheet(theme: str = 'dark') -> str:
    """
    加载 QSS 样式表

    Args:
        theme: 主题名称，'dark' 或 'light'

    Returns:
        str: 样式表内容
    """
    style_file = 'styles/modern.qss' if theme == 'dark' else 'styles/light.qss'
    qss_path = resource_path(style_file)

    try:
        if qss_path.exists():
            with open(qss_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            print(f"Warning: QSS file not found: {qss_path}")
            return ""
    except Exception as e:
        print(f"Error loading QSS: {e}")
        return ""


def main() -> int:
    """
    应用程序主入口
    
    Returns:
        int: 退出码
    """
    # 确保日志目录存在
    ensure_dir(LOGS_DIR)
    
    # 初始化日志系统
    logger = init_logging()
    logger.info("=" * 50)
    logger.info("war3技能文本生成器 starting...")
    logger.info(f"Application directory: {APP_DIR}")
    logger.info(f"Resource directory: {RESOURCE_DIR}")
    
    try:
        # 创建 QApplication 实例
        app = QApplication(sys.argv)
        
        # 设置应用程序信息
        app.setApplicationName("war3技能文本生成器")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("SoulQAQ")
        
        # 设置默认字体
        font = QFont("Microsoft YaHei UI", 10)
        app.setFont(font)
        
        # 加载配置
        config_manager = get_config_manager()
        config = config_manager.load()
        logger.info("Configuration loaded")

        # 获取主题设置并加载对应样式表
        theme = config_manager.get('ui.theme', 'dark')
        stylesheet = load_stylesheet(theme)
        if stylesheet:
            app.setStyleSheet(stylesheet)
            logger.info(f"Stylesheet loaded successfully (theme: {theme})")
        else:
            logger.warning("No stylesheet loaded, using default style")
        
        # 导入并创建主窗口（延迟导入以加快启动）
        from script.gui import MainWindow
        
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        
        # 启动事件循环
        exit_code = app.exec()
        
        logger.info(f"Application exiting with code: {exit_code}")
        return exit_code
        
    except Exception as e:
        logger.exception(f"Application error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())

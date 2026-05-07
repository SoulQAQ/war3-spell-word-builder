#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
PyQt 主窗口模块
提供应用程序的主界面，包含现代化深色主题 UI（中文版）
"""

import json
import html
import re
import sys
from typing import Optional

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize, QPoint, QObject
from PyQt6.QtGui import QAction, QFont, QIcon, QCursor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QFrame,
    QStackedWidget, QStatusBar, QMenuBar, QToolBar, QMessageBox,
    QProgressBar, QFileDialog, QScrollArea, QSizePolicy, QGroupBox, QGridLayout, QSpinBox,
    QSpacerItem, QButtonGroup, QGraphicsDropShadowEffect, QMenu
)

from script.config_manager import get_config_manager, ConfigManager
from script.network import HttpClient, HttpResponse
from script.utils import format_json, safe_json_loads
from script.logger import get_logger


# ============================================================================
# 预览颜色常量（统一管理，确保一致性）- 参考 Vue 实现
# ============================================================================

class PreviewColors:
    """预览区域颜色常量"""
    # 标题颜色
    TITLE_MAIN = "#FFFFFF"          # 主标题白色
    TITLE_LEVEL = "#33ccff"         # 等级高亮蓝色（Vue: learnLevel）
    TITLE_HOTKEY = "#ffcc00"        # 快捷键黄色（Vue: hotKey）

    # 内容颜色
    DESCRIPTION = "#FFFFFF"         # 描述文本白色
    FEATURE = "#ffcccc"             # 特点粉色（Vue: nature）

    # 技能属性名称颜色（统一绿色）- Vue: property
    ATTR_NAME = "#33cc33"           # 属性名称绿色

    # 属性值颜色
    ATTR_VALUE = "#FFFFFF"          # 属性值白色

    # 等级描述颜色（Vue: learnUpdateLevel）
    LEVEL_NUMBER = "#ff9900"        # 等级数字橙色
    LEVEL_TEXT = "#FFFFFF"          # 等级描述文本白色

    # 分隔线颜色
    SEPARATOR = "#666666"           # 分隔线灰色


# ============================================================================
# 技能属性配置（支持后续扩展为配置文件读取）
# ============================================================================

def get_default_attribute_suggestions() -> list:
    """
    获取默认的技能属性名称建议列表

    Returns:
        list: 属性名称建议列表

    说明:
        后续可通过配置文件扩展，当前返回默认值
    """
    return [
        "法力消耗",
        "施法距离",
        "冷却时间",
        "持续时间",
        "法术范围",
        "吟唱时间",
    ]


# 加载属性建议的占位函数（后续可替换为读取配置文件）
def load_attribute_suggestions() -> list:
    """
    从配置加载技能属性名称建议

    Returns:
        list: 属性名称建议列表

    说明:
        当前返回默认值，后续可扩展为从配置文件读取
    """
    return get_default_attribute_suggestions()


# ============================================================================
# Windows DWM API 支持（用于窗口圆角）
# ============================================================================

if sys.platform == 'win32':
    import ctypes
    from ctypes import wintypes

    # DWM 窗口属性
    DWMWA_WINDOW_CORNER_PREFERENCE = 33

    # 圆角偏好 (Windows 11)
    DWMWCP_DEFAULT = 0
    DWMWCP_ROUND = 2

    # 加载 Windows API
    user32 = ctypes.windll.user32
    dwmapi = ctypes.windll.dwmapi

    dwmapi.DwmSetWindowAttribute.restype = ctypes.c_int
    dwmapi.DwmSetWindowAttribute.argtypes = [wintypes.HWND, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]


# ============================================================================
# 自绘标题栏（VSCode左侧 + Cherry右侧拼接风格）
# ============================================================================

class TitleBarButton(QPushButton):
    """标题栏按钮基类，支持悬停高亮"""

    def __init__(self, text: str = "", parent: Optional[QWidget] = None):
        super().__init__(text, parent)
        self.setFixedHeight(28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("class", "title-menu-btn")


class TitleBar(QWidget):
    """
    自绘标题栏

    布局结构（从左到右）：
    [应用标题] [标题工具栏] [stretch拖拽区] [主题pill] [设置] [窗口控制按钮]
    """

    # 信号
    theme_clicked = pyqtSignal(str)  # 'dark' 或 'light'
    settings_clicked = pyqtSignal()

    # 统一高度常量
    HEIGHT = 36

    def __init__(self, parent: Optional[QMainWindow] = None):
        super().__init__(parent)
        self.parent_window = parent
        self.pressing = False
        self.start_pos = QPoint()
        self._current_theme = 'dark'

        self.setFixedHeight(self.HEIGHT)
        self.setProperty("class", "title-bar")
        self.setAutoFillBackground(True)

        self.setup_ui()

    def setup_ui(self) -> None:
        """设置标题栏布局"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 0, 0)
        layout.setSpacing(0)

        # ========== 应用标题（固定宽度）==========
        self.title_label = QLabel("war3技能文本生成器")
        self.title_label.setProperty("class", "title-text")
        self.title_label.setCursor(Qt.CursorShape.ArrowCursor)
        layout.addWidget(self.title_label)
        layout.addSpacing(12)

        # ========== 标题工具栏（紧凑排列，不拉伸）==========
        self.title_toolbar = self._create_title_toolbar()
        layout.addWidget(self.title_toolbar)

        # ========== 拖拽空白区域（stretch）==========
        layout.addStretch(1)

        # ========== 右侧控制区 ==========
        self.right_controls = self._create_right_controls()
        layout.addWidget(self.right_controls)

        # 初始化按钮状态
        self.update_theme_state('dark')

    # =========================================================================
    # 标题工具栏配置与创建
    # =========================================================================

    def _get_title_toolbar_items(self) -> list:
        """
        获取标题工具栏配置项

        Returns:
            list: 工具栏项配置列表，每项包含：
                - key: 唯一标识
                - text: 显示文本
                - menu_items: 菜单项列表（可选）

        说明：
            此方法返回的配置决定标题工具栏的内容。
            项目基础模板中使用示例菜单，实际项目可覆盖此方法或修改配置。
        """
        return [
            {
                "key": "file",
                "text": "文件(F)",
                "menu_items": [
                    {"text": "新建项目", "shortcut": "Ctrl+N", "callback": "_action_new_project"},
                    {"text": "打开项目", "shortcut": "Ctrl+O", "callback": "_action_open_project"},
                    {"separator": True},
                    {"text": "保存", "shortcut": "Ctrl+S", "callback": "_action_save"},
                    {"text": "另存为...", "shortcut": "Ctrl+Shift+S", "callback": "_action_save_as"},
                    {"separator": True},
                    {"text": "退出", "shortcut": "Alt+F4", "callback": "_on_close"},
                ]
            },
            {
                "key": "edit",
                "text": "编辑(E)",
                "menu_items": [
                    {"text": "撤销", "shortcut": "Ctrl+Z", "callback": "_action_undo"},
                    {"text": "重做", "shortcut": "Ctrl+Y", "callback": "_action_redo"},
                    {"separator": True},
                    {"text": "剪切", "shortcut": "Ctrl+X", "callback": "_action_cut"},
                    {"text": "复制", "shortcut": "Ctrl+C", "callback": "_action_copy"},
                    {"text": "粘贴", "shortcut": "Ctrl+V", "callback": "_action_paste"},
                ]
            },
            {
                "key": "selection",
                "text": "选择(S)",
                "menu_items": [
                    {"text": "全选", "shortcut": "Ctrl+A", "callback": "_action_select_all"},
                    {"text": "取消选择", "shortcut": "", "callback": "_action_deselect"},
                    {"separator": True},
                    {"text": "查找", "shortcut": "Ctrl+F", "callback": "_action_find"},
                    {"text": "替换", "shortcut": "Ctrl+H", "callback": "_action_replace"},
                ]
            },
            {
                "key": "view",
                "text": "查看(V)",
                "menu_items": [
                    {"text": "放大", "shortcut": "Ctrl++", "callback": "_action_zoom_in"},
                    {"text": "缩小", "shortcut": "Ctrl+-", "callback": "_action_zoom_out"},
                    {"text": "重置缩放", "shortcut": "Ctrl+0", "callback": "_action_zoom_reset"},
                    {"separator": True},
                    {"text": "全屏", "shortcut": "F11", "callback": "_action_fullscreen"},
                ]
            },
        ]

    def _create_title_toolbar(self) -> QWidget:
        """
        创建标题工具栏

        Returns:
            QWidget: 包含工具按钮的容器，使用固定宽度策略
        """
        toolbar = QWidget()
        toolbar.setProperty("class", "title-toolbar")
        toolbar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(0, 0, 0, 0)
        toolbar_layout.setSpacing(2)

        for item in self._get_title_toolbar_items():
            btn = self._create_toolbar_button(item)
            toolbar_layout.addWidget(btn)

        return toolbar

    def _create_toolbar_button(self, item: dict) -> QPushButton:
        """
        创建单个工具栏按钮

        Args:
            item: 工具栏项配置

        Returns:
            QPushButton: 配置好的按钮
        """
        text = item.get("text", "")
        btn = QPushButton(text)
        btn.setProperty("class", "title-menu-btn")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFlat(True)
        btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # 计算按钮宽度：文字宽度 + 左右 padding
        text_width = btn.fontMetrics().horizontalAdvance(text)
        btn.setFixedWidth(text_width + 20)
        btn.setFixedHeight(28)

        # 创建菜单
        menu = self._create_menu_from_items(item.get("menu_items", []))
        menu.setParent(self)
        btn.setMenu(menu)

        return btn

    def _create_menu_from_items(self, menu_items: list) -> QMenu:
        """
        根据配置创建菜单

        Args:
            menu_items: 菜单项配置列表

        Returns:
            QMenu: 创建好的菜单
        """
        menu = QMenu(self)

        for item in menu_items:
            if item.get("separator"):
                menu.addSeparator()
                continue

            action = QAction(item.get("text", ""), self)
            shortcut = item.get("shortcut", "")
            if shortcut:
                action.setShortcut(shortcut)

            callback_name = item.get("callback")
            if callback_name and hasattr(self, callback_name):
                action.triggered.connect(getattr(self, callback_name))

            menu.addAction(action)

        return menu

    # =========================================================================
    # 右侧控制区创建
    # =========================================================================

    def _create_right_controls(self) -> QWidget:
        """创建右侧控制区（主题、设置、窗口控制按钮）"""
        controls = QWidget()
        controls.setProperty("class", "title-controls")
        controls.setFixedHeight(self.HEIGHT)

        layout = QHBoxLayout(controls)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        btn_size = self.HEIGHT - 8

        # pill 按钮容器
        pill_container = QFrame()
        pill_container.setProperty("class", "title-pill-container")
        pill_layout = QHBoxLayout(pill_container)
        pill_layout.setContentsMargins(6, 4, 6, 4)
        pill_layout.setSpacing(4)

        # 深色主题按钮
        self.dark_btn = QPushButton()
        self.dark_btn.setProperty("class", "title-pill-btn")
        self.dark_btn.setText("🌙")
        self.dark_btn.setCheckable(True)
        self.dark_btn.setFixedSize(btn_size, btn_size)
        self.dark_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dark_btn.setToolTip("深色主题")
        self.dark_btn.clicked.connect(lambda: self._on_theme_click('dark'))
        pill_layout.addWidget(self.dark_btn)

        # 浅色主题按钮
        self.light_btn = QPushButton()
        self.light_btn.setProperty("class", "title-pill-btn")
        self.light_btn.setText("☀️")
        self.light_btn.setCheckable(True)
        self.light_btn.setFixedSize(btn_size, btn_size)
        self.light_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.light_btn.setToolTip("浅色主题")
        self.light_btn.clicked.connect(lambda: self._on_theme_click('light'))
        pill_layout.addWidget(self.light_btn)

        layout.addWidget(pill_container)

        # 分隔符
        separator1 = QFrame()
        separator1.setProperty("class", "title-separator")
        separator1.setFixedSize(1, int(self.HEIGHT * 0.6))
        layout.addWidget(separator1)
        layout.addSpacing(4)

        # 设置按钮
        self.settings_btn = QPushButton()
        self.settings_btn.setProperty("class", "title-icon-btn")
        self.settings_btn.setText("⚙️")
        self.settings_btn.setFixedSize(btn_size, btn_size)
        self.settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.settings_btn.setToolTip("设置")
        self.settings_btn.clicked.connect(self.settings_clicked)
        layout.addWidget(self.settings_btn)

        # 分隔符
        separator2 = QFrame()
        separator2.setProperty("class", "title-separator")
        separator2.setFixedSize(1, int(self.HEIGHT * 0.6))
        layout.addWidget(separator2)
        layout.addSpacing(4)

        # 窗口控制按钮
        win_btn_size = self.HEIGHT

        self.minimize_btn = QPushButton()
        self.minimize_btn.setProperty("class", "title-win-btn")
        self.minimize_btn.setText("─")
        self.minimize_btn.setFixedSize(win_btn_size, win_btn_size)
        self.minimize_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minimize_btn.setToolTip("最小化")
        self.minimize_btn.clicked.connect(self._on_minimize)
        layout.addWidget(self.minimize_btn)

        self.maximize_btn = QPushButton()
        self.maximize_btn.setProperty("class", "title-win-btn")
        self.maximize_btn.setText("□")
        self.maximize_btn.setFixedSize(win_btn_size, win_btn_size)
        self.maximize_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.maximize_btn.setToolTip("最大化")
        self.maximize_btn.clicked.connect(self._on_maximize)
        layout.addWidget(self.maximize_btn)

        self.close_btn = QPushButton()
        self.close_btn.setProperty("class", "title-win-btn title-close-btn")
        self.close_btn.setText("✕")
        self.close_btn.setFixedSize(win_btn_size, win_btn_size)
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setToolTip("关闭")
        self.close_btn.clicked.connect(self._on_close)
        layout.addWidget(self.close_btn)

        return controls

    # =========================================================================
    # 事件处理与工具方法
    # =========================================================================

    def _on_theme_click(self, theme: str) -> None:
        """主题按钮点击"""
        self.theme_clicked.emit(theme)

    def _on_minimize(self) -> None:
        """最小化窗口"""
        if self.parent_window:
            self.parent_window.showMinimized()

    def _on_maximize(self) -> None:
        """最大化/还原窗口"""
        if self.parent_window:
            if self.parent_window.isMaximized():
                self.parent_window.showNormal()
                self.maximize_btn.setText("□")
                self.maximize_btn.setToolTip("最大化")
            else:
                self.parent_window.showMaximized()
                self.maximize_btn.setText("❐")
                self.maximize_btn.setToolTip("还原")

    def _on_close(self) -> None:
        """关闭窗口"""
        if self.parent_window:
            self.parent_window.close()

    def update_theme_state(self, theme: str) -> None:
        """更新主题按钮状态"""
        self._current_theme = theme
        self.dark_btn.setChecked(theme == 'dark')
        self.light_btn.setChecked(theme == 'light')

    def set_title(self, title: str) -> None:
        """设置标题"""
        self.title_label.setText(title)

    # =========================================================================
    # 菜单动作占位方法（实际项目可替换为真实逻辑）
    # =========================================================================

    def _action_new_project(self): pass
    def _action_open_project(self): pass
    def _action_save(self): pass
    def _action_save_as(self): pass
    def _action_undo(self): pass
    def _action_redo(self): pass
    def _action_cut(self): pass
    def _action_copy(self): pass
    def _action_paste(self): pass
    def _action_select_all(self): pass
    def _action_deselect(self): pass
    def _action_find(self): pass
    def _action_replace(self): pass
    def _action_zoom_in(self): pass
    def _action_zoom_out(self): pass
    def _action_zoom_reset(self): pass
    def _action_fullscreen(self): pass

    # =========================================================================
    # 窗口拖拽处理
    # =========================================================================

    def mousePressEvent(self, event) -> None:
        if self._is_in_drag_area(event.pos()):
            if event.button() == Qt.MouseButton.LeftButton:
                self.pressing = True
                self.start_pos = event.globalPosition().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self.pressing and self.parent_window:
            if self.parent_window.isMaximized():
                self.parent_window.showNormal()
                self.maximize_btn.setText("□")
                self.maximize_btn.setToolTip("最大化")
            end_pos = event.globalPosition().toPoint()
            move = end_pos - self.start_pos
            new_pos = self.parent_window.pos() + move
            self.parent_window.move(new_pos)
            self.start_pos = end_pos
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self.pressing = False
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event) -> None:
        if self._is_in_drag_area(event.pos()):
            self._on_maximize()
        super().mouseDoubleClickEvent(event)

    def _is_in_drag_area(self, pos: QPoint) -> bool:
        """检查位置是否在拖拽区域内"""
        return pos.x() < self.right_controls.geometry().left()


# ============================================================================
# HTTP 请求工作线程
# ============================================================================

class HttpRequestWorker(QThread):
    """HTTP 请求后台工作线程"""
    
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(
        self,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        body: Optional[str] = None,
        timeout: int = 30
    ):
        super().__init__()
        self.method = method.upper()
        self.url = url
        self.headers = headers or {}
        self.body = body
        self.timeout = timeout
        self._is_cancelled = False
    
    def run(self) -> None:
        """执行 HTTP 请求"""
        try:
            client = HttpClient(timeout=self.timeout)
            
            json_data = None
            if self.body and self.method in ('POST', 'PUT', 'PATCH'):
                try:
                    json_data = json.loads(self.body)
                except json.JSONDecodeError:
                    pass
            
            response: HttpResponse
            
            if self.method == 'GET':
                response = client.get(self.url, headers=self.headers, timeout=self.timeout)
            elif self.method == 'POST':
                response = client.post(self.url, json_data=json_data, headers=self.headers, timeout=self.timeout)
            elif self.method == 'PUT':
                response = client.put(self.url, json_data=json_data, headers=self.headers, timeout=self.timeout)
            elif self.method == 'DELETE':
                response = client.delete(self.url, headers=self.headers, timeout=self.timeout)
            else:
                response = client.request(self.method, self.url, headers=self.headers, json_data=json_data, timeout=self.timeout)
            
            if not self._is_cancelled:
                self.finished.emit(response)
                
        except Exception as e:
            if not self._is_cancelled:
                self.error.emit(str(e))
    
    def cancel(self) -> None:
        """取消请求"""
        self._is_cancelled = True


# ============================================================================
# 导航按钮
# ============================================================================

class NavButton(QPushButton):
    """自定义导航按钮"""
    
    def __init__(self, text: str, icon_text: str = "", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setText(f"  {icon_text}  {text}" if icon_text else f"    {text}")
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("class", "nav-button")
        self.setFixedHeight(36)


# ============================================================================
# 卡片组件
# ============================================================================

class CardWidget(QFrame):
    """卡片组件"""
    
    def __init__(self, title: str = "", description: str = "", parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.setProperty("class", "card")
        self.setup_ui(title, description)
    
    def setup_ui(self, title: str, description: str) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(6)
        
        if title:
            title_label = QLabel(title)
            title_label.setProperty("class", "card-title")
            title_label.setFont(QFont("Microsoft YaHei UI", 12, QFont.Weight.Bold))
            layout.addWidget(title_label)
        
        if description:
            desc_label = QLabel(description)
            desc_label.setProperty("class", "card-description")
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)


# ============================================================================
# 技能属性数据类
# ============================================================================

class SkillAttribute:
    """技能属性数据类"""
    def __init__(self, name: str = "", value: str = ""):
        self.name = name
        self.value = value


# ============================================================================
# 技能属性行组件（支持自动补全）
# ============================================================================

class AttributeRowWidget(QWidget):
    """单个技能属性行组件"""

    # 信号：删除按钮点击，内容变化
    delete_clicked = pyqtSignal(object)  # 发送自身引用
    content_changed = pyqtSignal()

    def __init__(self, name: str = "", value: str = "", suggestions: list = None, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.name_input: Optional[QLineEdit] = None
        self.value_input: Optional[QLineEdit] = None
        self._suggestions = suggestions or []
        self._setup_ui(name, value)

    def _setup_ui(self, name: str, value: str) -> None:
        row_layout = QHBoxLayout(self)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(6)

        # 删除按钮
        delete_btn = QPushButton("−")
        delete_btn.setProperty("class", "homepage-attr-delete-btn")
        delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        delete_btn.setFixedSize(22, 22)
        delete_btn.clicked.connect(self._on_delete_clicked)
        row_layout.addWidget(delete_btn)

        # 属性名称输入
        self.name_input = QLineEdit(name)
        self.name_input.setProperty("class", "homepage-input")
        self.name_input.setFixedHeight(24)
        self.name_input.setPlaceholderText("属性名称")
        self.name_input.textChanged.connect(self._on_content_changed)
        row_layout.addWidget(self.name_input, 1)

        # 属性值输入
        self.value_input = QLineEdit(value)
        self.value_input.setProperty("class", "homepage-input")
        self.value_input.setFixedHeight(24)
        self.value_input.setPlaceholderText("数值")
        self.value_input.textChanged.connect(self._on_content_changed)
        row_layout.addWidget(self.value_input, 1)

        # 设置自动补全（在构造时完成，避免生命周期问题）
        self._setup_completer()

    def _setup_completer(self) -> None:
        """设置属性名称自动补全"""
        if self._suggestions and self.name_input:
            from PyQt6.QtWidgets import QCompleter
            completer = QCompleter(self._suggestions)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            self.name_input.setCompleter(completer)

    def _on_delete_clicked(self) -> None:
        """删除按钮点击"""
        self.delete_clicked.emit(self)

    def _on_content_changed(self) -> None:
        """内容变化"""
        self.content_changed.emit()

    def get_attribute(self) -> 'SkillAttribute':
        """获取属性数据"""
        return SkillAttribute(
            self.name_input.text().strip() if self.name_input else "",
            self.value_input.text().strip() if self.value_input else ""
        )


# ============================================================================
# Dashboard 首页
# ============================================================================

class DashboardPage(QWidget):
    """Dashboard 首页"""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.current_mode = "学习"
        self.current_level = "1级"
        self.level_buttons = []
        # 动态技能属性列表
        self.attribute_rows: list[AttributeRowWidget] = []
        # 属性名称建议列表
        self._attr_suggestions = load_attribute_suggestions()
        self.setup_ui()
        self._bind_preview_signals()
        self._rebuild_level_tabs()
        self.refresh_preview()

    def setup_ui(self) -> None:
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        body_wrap = QFrame()
        body_wrap.setProperty("class", "homepage-body-wrap")
        body_layout = QHBoxLayout(body_wrap)
        body_layout.setContentsMargins(10, 10, 10, 10)
        body_layout.setSpacing(10)
        root_layout.addWidget(body_wrap)

        # ========== 左侧预览区（参考Vue: span=9）==========
        left_panel = QFrame()
        left_panel.setProperty("class", "homepage-left-panel")
        left_panel.setFixedWidth(340)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(4, 4, 4, 4)
        left_layout.setSpacing(6)
        body_layout.addWidget(left_panel)

        # 模式切换按钮（参考Vue: el-radio-group）
        mode_row = QHBoxLayout()
        mode_row.setSpacing(0)
        self.mode_learn_btn = self._create_segment_button("学习", checked=True, width=56)
        self.mode_normal_btn = self._create_segment_button("普通", width=56)
        mode_row.addWidget(self.mode_learn_btn)
        mode_row.addWidget(self.mode_normal_btn)
        mode_row.addStretch()
        left_layout.addLayout(mode_row)

        # 等级标签滚动区（参考Vue: el-radio-group）
        level_scroll = QScrollArea()
        level_scroll.setWidgetResizable(True)
        level_scroll.setFrameShape(QFrame.Shape.NoFrame)
        level_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        level_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        level_scroll.setFixedHeight(28)

        self.level_container = QWidget()
        self.level_layout = QHBoxLayout(self.level_container)
        self.level_layout.setContentsMargins(0, 0, 0, 0)
        self.level_layout.setSpacing(0)
        level_scroll.setWidget(self.level_container)
        left_layout.addWidget(level_scroll)

        # 预览内容滚动区 - 内容自适应高度，超出时滚动
        self.preview_scroll = QScrollArea()
        self.preview_scroll.setWidgetResizable(True)
        self.preview_scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.preview_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.preview_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.preview_scroll.setProperty("class", "homepage-preview-scroll")
        self.preview_scroll.setAlignment(Qt.AlignmentFlag.AlignTop)  # 内容对齐顶部

        # 预览卡片（参考Vue: spell-container）- 高度自适应内容
        self.preview_card = QFrame()
        self.preview_card.setProperty("class", "homepage-preview-card")
        # 设置 sizePolicy 让卡片高度随内容增长，不垂直拉伸
        self.preview_card.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        preview_layout = QVBoxLayout(self.preview_card)
        preview_layout.setContentsMargins(10, 8, 10, 8)
        preview_layout.setSpacing(4)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # 内容对齐顶部

        self.preview_output = QLabel()
        self.preview_output.setProperty("class", "homepage-preview-text")
        self.preview_output.setTextFormat(Qt.TextFormat.RichText)
        self.preview_output.setWordWrap(True)
        self.preview_output.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.preview_output.setAutoFillBackground(False)
        # label 高度自适应内容
        self.preview_output.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        preview_layout.addWidget(self.preview_output)
        # 不使用 addStretch，让卡片高度由内容决定

        self.preview_scroll.setWidget(self.preview_card)
        left_layout.addWidget(self.preview_scroll, 1)

        # ========== 右侧表单区（参考Vue: span=14）==========
        right_panel = QFrame()
        right_panel.setProperty("class", "homepage-right-panel")
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(0)
        body_layout.addWidget(right_panel, 1)

        # 表单滚动区
        editor_scroll = QScrollArea()
        editor_scroll.setWidgetResizable(True)
        editor_scroll.setFrameShape(QFrame.Shape.NoFrame)
        editor_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        right_layout.addWidget(editor_scroll, 1)

        editor_wrap = QWidget()
        editor_scroll.setWidget(editor_wrap)
        editor_wrap_layout = QVBoxLayout(editor_wrap)
        editor_wrap_layout.setContentsMargins(0, 0, 0, 0)
        editor_wrap_layout.setSpacing(0)

        editor_card = QFrame()
        editor_card.setProperty("class", "homepage-editor-card")
        editor_card.setMinimumWidth(400)
        editor_layout = QVBoxLayout(editor_card)
        editor_layout.setContentsMargins(16, 12, 16, 12)
        editor_layout.setSpacing(4)
        editor_wrap_layout.addWidget(editor_card, 0, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        editor_layout.addWidget(self._create_section_header("在此填写"))

        # 第一行：名称、快捷键、技能最大级别（参考Vue布局）
        row1 = QHBoxLayout()
        row1.setSpacing(6)
        name_label = self._create_form_label("名称", width=56)
        self.name_input = QLineEdit()
        self.name_input.setProperty("class", "homepage-input")
        self.name_input.setPlaceholderText("技能名称")
        self.name_input.setText("技能名称")
        self.name_input.setFixedHeight(22)
        hotkey_label = self._create_form_label("快捷键", width=40)
        self.hotkey_input = QLineEdit("A")
        self.hotkey_input.setProperty("class", "homepage-input")
        self.hotkey_input.setFixedWidth(40)
        self.hotkey_input.setFixedHeight(22)
        max_level_label = self._create_form_label("最大级别", width=50)
        self.max_level_spin = QSpinBox()
        self.max_level_spin.setProperty("class", "homepage-spin")
        self.max_level_spin.setRange(1, 99)
        self.max_level_spin.setValue(4)
        self.max_level_spin.setFixedWidth(45)
        self.max_level_spin.setFixedHeight(22)
        row1.addWidget(name_label)
        row1.addWidget(self.name_input, 1)
        row1.addWidget(hotkey_label)
        row1.addWidget(self.hotkey_input)
        row1.addWidget(max_level_label)
        row1.addWidget(self.max_level_spin)
        editor_layout.addLayout(row1)

        # 技能描述
        desc_label = self._create_form_label("技能描述", width=56)
        self.skill_desc_input = QTextEdit()
        self.skill_desc_input.setProperty("class", "homepage-textarea")
        self.skill_desc_input.setFixedHeight(40)
        self.skill_desc_input.setPlainText("这是描述")
        desc_row = QHBoxLayout()
        desc_row.setSpacing(6)
        desc_row.addWidget(desc_label)
        desc_row.addWidget(self.skill_desc_input, 1)
        editor_layout.addLayout(desc_row)

        # 特点
        feature_label = self._create_form_label("特点", width=56)
        self.feature_input = QTextEdit()
        self.feature_input.setProperty("class", "homepage-textarea")
        self.feature_input.setFixedHeight(40)
        self.feature_input.setPlainText("无视敌我")
        feature_row = QHBoxLayout()
        feature_row.setSpacing(6)
        feature_row.addWidget(feature_label)
        feature_row.addWidget(self.feature_input, 1)
        editor_layout.addLayout(feature_row)

        # 升级描述
        upgrade_label = self._create_form_label("升级描述", width=56)
        upgrade_col = QVBoxLayout()
        upgrade_col.setSpacing(3)
        self.upgrade_desc_input = QLineEdit()
        self.upgrade_desc_input.setProperty("class", "homepage-input")
        self.upgrade_desc_input.setFixedHeight(22)
        self.upgrade_desc_input.setText("我是描述，属性{a}")
        self.upgrade_values_input = QTextEdit()
        self.upgrade_values_input.setProperty("class", "homepage-textarea")
        self.upgrade_values_input.setFixedHeight(35)
        self.upgrade_values_input.setPlainText("[a=10+6] [1v=4]")
        upgrade_col.addWidget(self.upgrade_desc_input)
        upgrade_col.addWidget(self.upgrade_values_input)
        upgrade_row = QHBoxLayout()
        upgrade_row.setSpacing(6)
        upgrade_row.addWidget(upgrade_label)
        upgrade_row.addLayout(upgrade_col, 1)
        editor_layout.addLayout(upgrade_row)

        # 普通描述
        normal_label = self._create_form_label("普通描述", width=56)
        normal_col = QVBoxLayout()
        normal_col.setSpacing(3)
        self.normal_desc_input = QTextEdit()
        self.normal_desc_input.setProperty("class", "homepage-textarea")
        self.normal_desc_input.setFixedHeight(40)
        self.normal_desc_input.setPlaceholderText("向目标投掷一巨大的魔法锤，对其造成100点伤害并使其3秒内处于眩晕状态。")
        self.normal_values_input = QTextEdit()
        self.normal_values_input.setProperty("class", "homepage-textarea")
        self.normal_values_input.setFixedHeight(35)
        self.normal_values_input.setPlaceholderText("数值")
        normal_col.addWidget(self.normal_desc_input)
        normal_col.addWidget(self.normal_values_input)
        normal_row = QHBoxLayout()
        normal_row.setSpacing(6)
        normal_row.addWidget(normal_label)
        normal_row.addLayout(normal_col, 1)
        editor_layout.addLayout(normal_row)

        editor_layout.addSpacing(4)
        editor_layout.addWidget(self._create_section_header("技能属性"))

        # 技能属性容器
        self.attrs_container = QWidget()
        self.attrs_layout = QVBoxLayout(self.attrs_container)
        self.attrs_layout.setContentsMargins(0, 0, 0, 0)
        self.attrs_layout.setSpacing(3)
        editor_layout.addWidget(self.attrs_container)

        # 添加属性按钮（参考Vue: el-link）
        add_attr_btn = QPushButton("添加...")
        add_attr_btn.setProperty("class", "homepage-link-btn")
        add_attr_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_attr_btn.setFixedHeight(20)
        add_attr_btn.clicked.connect(self._add_attribute_row)
        editor_layout.addWidget(add_attr_btn)

        editor_layout.addStretch()

        # ========== 固定底部按钮栏 ==========
        footer_frame = QFrame()
        footer_frame.setProperty("class", "homepage-footer-bar")
        footer_layout = QHBoxLayout(footer_frame)
        footer_layout.setContentsMargins(10, 8, 10, 8)
        footer_layout.setSpacing(6)
        footer_layout.addStretch()
        self.generate_btn = self._create_action_button("生成", "homepage-action-generate")
        self.restore_default_btn = self._create_action_button("恢复默认", "homepage-action-default")
        self.save_btn = self._create_action_button("保存", "homepage-action-warn")
        footer_layout.addWidget(self.generate_btn)
        footer_layout.addWidget(self.restore_default_btn)
        footer_layout.addWidget(self.save_btn)
        right_layout.addWidget(footer_frame)

        # 初始化默认属性
        self._add_attribute_row("法力消耗", "999")
        self._add_attribute_row("冷却时间", "111")

        # 交互 - 实时预览绑定
        self.mode_learn_btn.clicked.connect(lambda: self._set_mode("学习"))
        self.mode_normal_btn.clicked.connect(lambda: self._set_mode("普通"))
        self.max_level_spin.valueChanged.connect(self._on_max_level_changed)
        self.generate_btn.clicked.connect(self.refresh_preview)
        self.restore_default_btn.clicked.connect(self._reset_defaults)

    def _create_segment_button(self, text: str, checked: bool = False, width: int = 56) -> QPushButton:
        btn = QPushButton(text)
        btn.setProperty("class", "homepage-segment-btn")
        btn.setCheckable(True)
        btn.setChecked(checked)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedSize(width, 24)
        return btn

    def _create_action_button(self, text: str, cls: str) -> QPushButton:
        btn = QPushButton(text)
        btn.setProperty("class", cls)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setFixedHeight(24)
        return btn

    def _create_section_header(self, text: str) -> QWidget:
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 3)
        layout.setSpacing(8)

        line_left = QFrame()
        line_left.setProperty("class", "homepage-section-line")
        line_left.setFrameShape(QFrame.Shape.HLine)
        line_left.setFixedWidth(24)
        layout.addWidget(line_left)

        title = QLabel(text)
        title.setProperty("class", "homepage-section-title")
        title.setFont(QFont("Microsoft YaHei UI", 10, QFont.Weight.Bold))
        layout.addWidget(title)

        line_right = QFrame()
        line_right.setProperty("class", "homepage-section-line")
        line_right.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(line_right, 1)

        return widget

    def _create_form_label(self, text: str, width: int = 56) -> QLabel:
        label = QLabel(text)
        label.setProperty("class", "homepage-form-label")
        label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        label.setFixedWidth(width)
        label.setFont(QFont("Microsoft YaHei UI", 8, QFont.Weight.Bold))
        return label

    def _add_attribute_row(self, name: str = "", value: str = "") -> None:
        """添加一个技能属性行"""
        row_widget = AttributeRowWidget(name, value, self._attr_suggestions, self)
        row_widget.delete_clicked.connect(self._remove_attribute_row)
        row_widget.content_changed.connect(self.refresh_preview)
        self.attrs_layout.addWidget(row_widget)
        self.attribute_rows.append(row_widget)

    def _remove_attribute_row(self, row: AttributeRowWidget) -> None:
        """删除一个技能属性行"""
        if row in self.attribute_rows:
            self.attribute_rows.remove(row)
            self.attrs_layout.removeWidget(row)
            row.deleteLater()
            self.refresh_preview()

    def _get_all_attributes(self) -> list[SkillAttribute]:
        """获取所有技能属性"""
        return [row.get_attribute() for row in self.attribute_rows]

    def _bind_preview_signals(self) -> None:
        """绑定所有输入控件的信号以实现实时预览"""
        # 文本输入实时更新
        self.name_input.textChanged.connect(self.refresh_preview)
        self.hotkey_input.textChanged.connect(self.refresh_preview)
        self.skill_desc_input.textChanged.connect(self.refresh_preview)
        self.feature_input.textChanged.connect(self.refresh_preview)
        self.upgrade_desc_input.textChanged.connect(self.refresh_preview)
        self.upgrade_values_input.textChanged.connect(self.refresh_preview)
        self.normal_desc_input.textChanged.connect(self.refresh_preview)
        self.normal_values_input.textChanged.connect(self.refresh_preview)
        self.max_level_spin.valueChanged.connect(self.refresh_preview)

    def _clear_level_tabs(self) -> None:
        while self.level_layout.count():
            item = self.level_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.level_buttons = []

    def _rebuild_level_tabs(self) -> None:
        self._clear_level_tabs()
        display_levels = min(self.max_level_spin.value(), 20)

        for i in range(display_levels):
            level_text = f"{i + 1}级"
            btn = QPushButton(level_text)
            btn.setProperty("class", "homepage-segment-btn")
            btn.setCheckable(True)
            btn.setChecked(level_text == self.current_level)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedSize(48, 24)
            btn.clicked.connect(lambda _checked=False, text=level_text: self._set_level(text))
            self.level_buttons.append(btn)
            self.level_layout.addWidget(btn)

        self.level_layout.addStretch()

        if display_levels == 0:
            self.current_level = "1级"
        else:
            try:
                current_num = int(self.current_level.replace("级", ""))
            except ValueError:
                current_num = 1
            if current_num > display_levels:
                self.current_level = "1级"

        self._sync_level_btn_state()

    def _sync_level_btn_state(self) -> None:
        for btn in self.level_buttons:
            btn.setChecked(btn.text() == self.current_level)

    def _on_max_level_changed(self, _value: int) -> None:
        self._rebuild_level_tabs()
        self.refresh_preview()

    def _set_mode(self, mode: str) -> None:
        self.current_mode = mode
        self.mode_learn_btn.setChecked(mode == "学习")
        self.mode_normal_btn.setChecked(mode == "普通")
        self.refresh_preview()

    def _set_level(self, level: str) -> None:
        self.current_level = level
        self._sync_level_btn_state()
        self.refresh_preview()

    def _reset_defaults(self) -> None:
        self.name_input.setText("技能名称")
        self.hotkey_input.setText("A")
        self.skill_desc_input.setPlainText("这是描述")
        self.feature_input.setPlainText("无视敌我")
        self.upgrade_desc_input.setText("我是描述，属性{a}")
        self.upgrade_values_input.setPlainText("[a=10+6] [1v=4]")
        self.normal_desc_input.setPlainText("")
        self.normal_values_input.setPlainText("")
        self.max_level_spin.setValue(4)
        # 清除所有属性行
        for row in self.attribute_rows:
            self.attrs_layout.removeWidget(row)
            row.deleteLater()
        self.attribute_rows.clear()
        # 添加默认属性
        self._add_attribute_row("法力消耗", "999")
        self._add_attribute_row("冷却时间", "111")
        self._set_mode("学习")
        self._set_level("1级")

    def _extract_upgrade_values(self, count: int) -> list[int]:
        text = self.upgrade_values_input.toPlainText()
        match = re.search(r"\[\s*a\s*=\s*(\d+)\s*\+\s*(\d+)\s*\]", text)
        if match:
            base = int(match.group(1))
            step = int(match.group(2))
            return [base + step * i for i in range(count)]
        return [10 + 6 * i for i in range(count)]

    def refresh_preview(self) -> None:
        """刷新预览内容 - 参考Vue的spell.vue实现"""
        name = html.escape(self.name_input.text().strip() or "技能名称")
        hotkey = html.escape(self.hotkey_input.text().strip() or "A")
        description = html.escape(self.skill_desc_input.toPlainText().strip())
        feature = html.escape(self.feature_input.toPlainText().strip())
        normal_desc = html.escape(self.normal_desc_input.toPlainText().strip())
        level = html.escape(self.current_level)
        mode = self.current_mode

        # 获取所有技能属性
        attributes = self._get_all_attributes()

        if mode == "学习":
            # 学习模式：显示所有属性（参考Vue: learnPros）
            attr_html_lines = []
            for attr in attributes:
                if attr.name and attr.value:
                    attr_name = html.escape(attr.name)
                    attr_value = html.escape(attr.value)
                    attr_html_lines.append(
                        f'<div><span style="color:{PreviewColors.ATTR_NAME};">{attr_name}：</span>'
                        f'<span style="color:{PreviewColors.ATTR_VALUE};">{attr_value}</span></div>'
                    )
            attr_html = ''.join(attr_html_lines)

            # 等级升级描述
            display_levels = min(self.max_level_spin.value(), 20)
            upgrade_template = self.upgrade_desc_input.text().strip() or "我是描述，属性{a}"
            upgrade_values = self._extract_upgrade_values(display_levels)
            upgrade_lines = []
            for idx, value in enumerate(upgrade_values, start=1):
                line = html.escape(upgrade_template.replace("{a}", str(value)))
                upgrade_lines.append(
                    f'<div><span style="color:{PreviewColors.LEVEL_NUMBER};">{idx}级</span>'
                    f' - {line}。</div>'
                )

            # 学习模式标题（参考Vue）
            title_html = f'<p style="margin-bottom:3px;">学习 <span style="color:{PreviewColors.TITLE_LEVEL};">{level}</span> {name}'
            if hotkey:
                title_html += f' (<span style="color:{PreviewColors.TITLE_HOTKEY};">{hotkey}</span>)'
            title_html += '</p>'

            # 构建预览HTML（参考Vue: spell-container）
            preview_html = f"""
<div style="font-family:'Microsoft YaHei UI'; font-size:12px; line-height:1.6; font-weight:bold;">
  {title_html}
  <hr style="border:none;border-top:1px solid {PreviewColors.SEPARATOR};margin:5px 0;">
  <p style="margin-top:5px;">
    {description}
    {'<br/>' if description else ''}
    {f'<br/><span style="color:{PreviewColors.FEATURE};">{feature}</span><br/>' if feature else ''}
    {'<br/>' + attr_html if attr_html else ''}
    {'<br/>' + ''.join(upgrade_lines) if upgrade_lines else ''}
  </p>
</div>
"""
        else:
            # 普通模式：过滤掉法力消耗（参考Vue: normalPros）
            attr_html_lines = []
            for attr in attributes:
                if attr.name and attr.value and attr.name != "法力消耗":
                    attr_name = html.escape(attr.name)
                    attr_value = html.escape(attr.value)
                    attr_html_lines.append(
                        f'<div><span style="color:{PreviewColors.ATTR_NAME};">{attr_name}：</span>'
                        f'<span style="color:{PreviewColors.ATTR_VALUE};">{attr_value}</span></div>'
                    )
            attr_html = ''.join(attr_html_lines)

            # 普通模式标题（参考Vue）
            level_num = level.replace("级", "")
            title_html = f'<p style="margin-bottom:3px;">{name}'
            if hotkey:
                title_html += f' (<span style="color:{PreviewColors.TITLE_HOTKEY};">{hotkey}</span>)'
            title_html += f' - [<span style="color:{PreviewColors.TITLE_LEVEL};">{level_num}</span>]</p>'

            # 构建预览HTML
            preview_html = f"""
<div style="font-family:'Microsoft YaHei UI'; font-size:12px; line-height:1.6; font-weight:bold;">
  {title_html}
  <hr style="border:none;border-top:1px solid {PreviewColors.SEPARATOR};margin:5px 0;">
  <p style="margin-top:5px;">
    {normal_desc + '。' if normal_desc and not normal_desc.endswith('。') else normal_desc}
    {'<br/>' if normal_desc else ''}
    {f'<br/><span style="color:{PreviewColors.FEATURE};">{feature}</span><br/>' if feature else ''}
    {'<br/>' + attr_html if attr_html else ''}
  </p>
</div>
"""

        self.preview_output.setText(preview_html)


# ============================================================================
# HTTP Client 页面
# ============================================================================

class HttpClientPage(QWidget):
    """HTTP 请求测试页面"""
    
    def __init__(self, config_manager: ConfigManager, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.worker: Optional[HttpRequestWorker] = None
        self.setup_ui()
    
    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 页面标题
        title = QLabel("HTTP 客户端")
        title.setProperty("class", "page-title")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        desc = QLabel("测试 HTTP 请求，支持自定义请求头和请求体")
        desc.setProperty("class", "page-subtitle")
        layout.addWidget(desc)

        layout.addSpacing(8)

        # URL 和 Method 行
        url_layout = QHBoxLayout()

        method_label = QLabel("方法：")
        method_label.setFixedWidth(50)
        url_layout.addWidget(method_label)

        self.method_combo = QComboBox()
        self.method_combo.addItems(['GET', 'POST', 'PUT', 'DELETE'])
        self.method_combo.setFixedWidth(80)
        url_layout.addWidget(self.method_combo)

        url_label = QLabel("URL：")
        url_label.setFixedWidth(35)
        url_layout.addWidget(url_label)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("输入 URL...")
        default_url = self.config_manager.get('network.default_url', 'https://httpbin.org/get')
        self.url_input.setText(default_url)
        url_layout.addWidget(self.url_input)

        layout.addLayout(url_layout)

        # Headers 输入
        headers_label = QLabel("请求头 (JSON)：")
        layout.addWidget(headers_label)

        self.headers_input = QTextEdit()
        self.headers_input.setPlaceholderText('{\n  "Content-Type": "application/json"\n}')
        self.headers_input.setMaximumHeight(50)
        self.headers_input.setFont(QFont("Consolas", 9))
        layout.addWidget(self.headers_input)

        # Body 输入
        self.body_label = QLabel("请求体 (JSON)：")
        layout.addWidget(self.body_label)

        self.body_input = QTextEdit()
        self.body_input.setPlaceholderText('{\n  "key": "value"\n}')
        self.body_input.setMaximumHeight(60)
        self.body_input.setFont(QFont("Consolas", 9))
        layout.addWidget(self.body_input)
        
        # 发送按钮
        btn_layout = QHBoxLayout()
        
        self.send_btn = QPushButton("发送请求")
        self.send_btn.setProperty("class", "primary-button")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.clicked.connect(self.send_request)
        btn_layout.addWidget(self.send_btn)
        
        self.clear_btn = QPushButton("清空")
        self.clear_btn.setProperty("class", "secondary-button")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.clicked.connect(self.clear_response)
        btn_layout.addWidget(self.clear_btn)
        
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # 响应区域
        response_label = QLabel("响应：")
        layout.addWidget(response_label)
        
        # 状态信息行
        status_layout = QHBoxLayout()
        
        self.status_label = QLabel("状态：-")
        self.status_label.setProperty("class", "status-label")
        status_layout.addWidget(self.status_label)
        
        self.time_label = QLabel("耗时：-")
        self.time_label.setProperty("class", "time-label")
        status_layout.addWidget(self.time_label)
        
        status_layout.addStretch()
        layout.addLayout(status_layout)
        
        # 响应内容
        self.response_output = QTextEdit()
        self.response_output.setReadOnly(True)
        self.response_output.setFont(QFont("Consolas", 9))
        self.response_output.setPlaceholderText("响应内容将显示在这里...")
        layout.addWidget(self.response_output)
    
    def send_request(self) -> None:
        """发送 HTTP 请求"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "警告", "请输入 URL")
            return
        
        method = self.method_combo.currentText()
        headers_text = self.headers_input.toPlainText().strip()
        body_text = self.body_input.toPlainText().strip()
        
        headers = {}
        if headers_text:
            headers = safe_json_loads(headers_text, {})
            if headers is None:
                QMessageBox.warning(self, "警告", "请求头 JSON 格式无效")
                return
        
        timeout = self.config_manager.get('network.timeout', 30)
        
        self.send_btn.setEnabled(False)
        self.send_btn.setText("发送中...")
        self.status_label.setText("状态：发送中...")
        
        self.worker = HttpRequestWorker(
            method=method,
            url=url,
            headers=headers,
            body=body_text if method in ('POST', 'PUT', 'PATCH') else None,
            timeout=timeout
        )
        self.worker.finished.connect(self.on_request_finished)
        self.worker.error.connect(self.on_request_error)
        self.worker.start()
    
    def on_request_finished(self, response: HttpResponse) -> None:
        """请求完成回调"""
        self.send_btn.setEnabled(True)
        self.send_btn.setText("发送请求")
        
        status_color = "#22C55E" if response.success else "#EF4444"
        self.status_label.setText(f"状态：{response.status_code}")
        self.status_label.setStyleSheet(f"color: {status_color}; font-weight: bold;")
        
        self.time_label.setText(f"耗时：{response.elapsed_ms:.0f} 毫秒")
        
        if response.data is not None:
            formatted = format_json(response.data)
            self.response_output.setPlainText(formatted)
        else:
            self.response_output.setPlainText(response.text or "(空响应)")
        
        if not response.success:
            self.response_output.append(f"\n\n--- 错误 ---\n{response.message}")
    
    def on_request_error(self, error: str) -> None:
        """请求错误回调"""
        self.send_btn.setEnabled(True)
        self.send_btn.setText("发送请求")
        
        self.status_label.setText("状态：错误")
        self.status_label.setStyleSheet("color: #EF4444; font-weight: bold;")
        self.time_label.setText("耗时：-")
        
        self.response_output.setPlainText(f"请求失败：\n{error}")
    
    def clear_response(self) -> None:
        """清空响应"""
        self.response_output.clear()
        self.status_label.setText("状态：-")
        self.status_label.setStyleSheet("")
        self.time_label.setText("耗时：-")


# ============================================================================
# Settings 页面
# ============================================================================

class SettingsPage(QWidget):
    """设置页面"""

    # 主题切换信号
    theme_changed = pyqtSignal(str)

    def __init__(self, config_manager: ConfigManager, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config_manager = config_manager
        self._theme_updating = False  # 防止循环更新
        self.setup_ui()
        self.load_settings()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 页面标题
        title = QLabel("设置")
        title.setProperty("class", "page-title")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        desc = QLabel("配置应用程序设置")
        desc.setProperty("class", "page-subtitle")
        layout.addWidget(desc)

        layout.addSpacing(8)

        # 外观设置组
        appearance_group = QGroupBox("外观")
        appearance_group.setProperty("class", "settings-group")
        appearance_layout = QVBoxLayout(appearance_group)
        appearance_layout.setSpacing(12)

        # 主题切换标签
        theme_label = QLabel("主题：")
        appearance_layout.addWidget(theme_label)

        # 主题切换按钮容器
        theme_btn_layout = QHBoxLayout()
        theme_btn_layout.setSpacing(10)

        # 创建按钮组（互斥）
        self.theme_btn_group = QButtonGroup(self)
        self.theme_btn_group.setExclusive(True)

        # 深色主题按钮
        self.dark_theme_btn = QPushButton("🌙 深色")
        self.dark_theme_btn.setProperty("class", "theme-btn")
        self.dark_theme_btn.setCheckable(True)
        self.dark_theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.dark_theme_btn.clicked.connect(lambda: self._on_theme_btn_click("dark"))
        self.theme_btn_group.addButton(self.dark_theme_btn, 0)
        theme_btn_layout.addWidget(self.dark_theme_btn)

        # 浅色主题按钮
        self.light_theme_btn = QPushButton("☀️ 浅色")
        self.light_theme_btn.setProperty("class", "theme-btn")
        self.light_theme_btn.setCheckable(True)
        self.light_theme_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.light_theme_btn.clicked.connect(lambda: self._on_theme_btn_click("light"))
        self.theme_btn_group.addButton(self.light_theme_btn, 1)
        theme_btn_layout.addWidget(self.light_theme_btn)

        theme_btn_layout.addStretch()
        appearance_layout.addLayout(theme_btn_layout)

        layout.addWidget(appearance_group)

        # 应用设置组
        app_group = QGroupBox("应用程序")
        app_group.setProperty("class", "settings-group")
        app_layout = QVBoxLayout(app_group)
        app_layout.setSpacing(6)

        # App Name
        name_layout = QHBoxLayout()
        name_label = QLabel("应用名称：")
        name_label.setFixedWidth(85)
        self.name_input = QLineEdit()
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        app_layout.addLayout(name_layout)

        # App Version
        version_layout = QHBoxLayout()
        version_label = QLabel("应用版本：")
        version_label.setFixedWidth(85)
        self.version_input = QLineEdit()
        version_layout.addWidget(version_label)
        version_layout.addWidget(self.version_input)
        app_layout.addLayout(version_layout)

        layout.addWidget(app_group)

        # 网络设置组
        network_group = QGroupBox("网络")
        network_group.setProperty("class", "settings-group")
        network_layout = QVBoxLayout(network_group)
        network_layout.setSpacing(6)

        # Timeout
        timeout_layout = QHBoxLayout()
        timeout_label = QLabel("超时时间(秒)：")
        timeout_label.setFixedWidth(85)
        self.timeout_input = QLineEdit()
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_input)
        network_layout.addLayout(timeout_layout)

        layout.addWidget(network_group)

        # 用户设置组
        user_group = QGroupBox("用户设置")
        user_group.setProperty("class", "settings-group")
        user_layout = QVBoxLayout(user_group)
        user_layout.setSpacing(6)

        # Output Path
        output_layout = QHBoxLayout()
        output_label = QLabel("输出路径：")
        output_label.setFixedWidth(85)
        self.output_input = QLineEdit()
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_output)
        output_layout.addWidget(output_label)
        output_layout.addWidget(self.output_input)
        output_layout.addWidget(browse_btn)
        user_layout.addLayout(output_layout)

        layout.addWidget(user_group)

        layout.addSpacing(12)

        # 保存按钮
        btn_layout = QHBoxLayout()

        self.save_btn = QPushButton("保存设置")
        self.save_btn.setProperty("class", "primary-button")
        self.save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.save_btn)

        self.reset_btn = QPushButton("恢复默认")
        self.reset_btn.setProperty("class", "secondary-button")
        self.reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reset_btn.clicked.connect(self.reset_settings)
        btn_layout.addWidget(self.reset_btn)

        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        layout.addStretch()

    def _on_theme_btn_click(self, theme: str) -> None:
        """主题按钮点击 - 只发射信号，不直接应用主题"""
        if self._theme_updating:
            return
        self.config_manager.set('ui.theme', theme)
        self.theme_changed.emit(theme)

    def update_theme_buttons(self, theme: str) -> None:
        """更新主题按钮状态（由外部调用）"""
        self._theme_updating = True
        try:
            if theme == 'dark':
                self.dark_theme_btn.setChecked(True)
            else:
                self.light_theme_btn.setChecked(True)
        finally:
            self._theme_updating = False

    def load_settings(self) -> None:
        """加载设置"""
        self.name_input.setText(self.config_manager.get('app.name', 'war3技能文本生成器'))
        self.version_input.setText(self.config_manager.get('app.version', '1.0.0'))
        self.timeout_input.setText(str(self.config_manager.get('network.timeout', 30)))
        self.output_input.setText(self.config_manager.get('user_settings.output_path', './rundata/output'))

        # 加载主题设置
        theme = self.config_manager.get('ui.theme', 'dark')
        self.update_theme_buttons(theme)

    def save_settings(self) -> None:
        """保存设置"""
        try:
            self.config_manager.set('app.name', self.name_input.text())
            self.config_manager.set('app.version', self.version_input.text())
            self.config_manager.set('network.timeout', int(self.timeout_input.text()))
            self.config_manager.set('user_settings.output_path', self.output_input.text())

            QMessageBox.information(self, "成功", "设置已保存！")
        except ValueError:
            QMessageBox.warning(self, "警告", "超时时间必须是数字")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置失败：{str(e)}")

    def reset_settings(self) -> None:
        """重置设置"""
        reply = QMessageBox.question(
            self, "确认重置",
            "确定要恢复默认设置吗？",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.config_manager.reset_to_defaults()
            self.load_settings()
            # 重置后通知主题切换
            theme = self.config_manager.get('ui.theme', 'dark')
            self.theme_changed.emit(theme)
            QMessageBox.information(self, "成功", "已恢复默认设置！")

    def browse_output(self) -> None:
        """浏览输出目录"""
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.output_input.setText(folder)


# ============================================================================
# About 页面
# ============================================================================

class AboutPage(QWidget):
    """关于页面"""
    
    def __init__(self, config_manager: ConfigManager, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setup_ui()
    
    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        # 页面标题
        title = QLabel("关于")
        title.setProperty("class", "page-title")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)

        layout.addSpacing(8)
        
        # 项目信息卡片
        info_card = CardWidget("", "")
        
        app_name = self.config_manager.get('app.name', 'war3技能文本生成器')
        app_version = self.config_manager.get('app.version', '1.0.0')
        
        info_text = f"""
<h2>{app_name}</h2>
<p style="color: #94A3B8;">版本 {app_version}</p>
<br>
<p>一个现代化的 PyQt6 桌面应用程序模板，包含：</p>
<ul>
  <li>现代深色主题 UI，QSS 样式</li>
  <li>内置 HTTP 客户端，用于 API 测试</li>
  <li>基于 YAML 的配置管理</li>
  <li>PyInstaller 打包支持</li>
  <li>跨平台兼容</li>
</ul>
<br>
<p><b>技术栈：</b></p>
<p>Python 3.12 | PyQt6 | requests | PyYAML | PyInstaller</p>
<br>
<p><b>GitHub 仓库：</b></p>
<p style="color: #4F8CFF;"><a href="https://github.com/SoulQAQ/pyqt-exe-template" style="color: #4F8CFF;">https://github.com/SoulQAQ/pyqt-exe-template</a></p>
"""
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setOpenExternalLinks(True)
        info_label.setTextFormat(Qt.TextFormat.RichText)
        
        card_layout = info_card.layout()
        card_layout.addWidget(info_label)
        
        layout.addWidget(info_card)
        
        layout.addStretch()


# ============================================================================
# 主窗口
# ============================================================================

class MainWindow(QMainWindow):
    """
    应用程序主窗口

    布局结构（自绘标题栏）：
    ┌─────────────────────────────────────────────────────────┐
    │ [标题文字..................] [🌙] [☀️] | [⚙️]  │ ← 自绘标题栏
    ├──────────┬──────────────────────────────────────────────┤
    │          │                                              │
    │  导航栏  │              内容区                          │
    │ (180px)  │                                              │
    │          │                                              │
    └──────────┴──────────────────────────────────────────────┘
    """

    # 主题切换信号
    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.logger = get_logger()
        self.config_manager = get_config_manager()
        self.config = self.config_manager.load()
        self._current_theme = self.config_manager.get('ui.theme', 'dark')

        # 使用 FramelessWindowHint 实现自绘标题栏
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowMinMaxButtonsHint
        )

        self._init_ui()
        self._init_statusbar()
        self._load_window_state()
        self._connect_signals()

        # Windows 平台下设置窗口圆角
        if sys.platform == 'win32':
            self._setup_window_corners()

        self.logger.info("主窗口初始化完成")

    def _setup_window_corners(self) -> None:
        """设置 Windows 11 窗口圆角"""
        try:
            hwnd = int(self.winId())
            corner_preference = ctypes.c_int(DWMWCP_ROUND)
            dwmapi.DwmSetWindowAttribute(
                hwnd,
                DWMWA_WINDOW_CORNER_PREFERENCE,
                ctypes.byref(corner_preference),
                ctypes.sizeof(corner_preference)
            )
            self.logger.info("窗口圆角设置完成")
        except Exception as e:
            self.logger.warning(f"窗口圆角设置失败: {e}")

    def apply_theme(self, theme: str) -> None:
        """
        应用主题 - 统一入口，同步所有控件状态

        Args:
            theme: 主题名称，'dark' 或 'light'
        """
        self._current_theme = theme
        self.config_manager.set('ui.theme', theme)

        # 加载对应的样式表
        stylesheet = self._load_theme_stylesheet(theme)
        if stylesheet:
            QApplication.instance().setStyleSheet(stylesheet)

        # 同步更新所有主题控件
        if hasattr(self, 'title_bar'):
            self.title_bar.update_theme_state(theme)
        if hasattr(self, 'settings_page'):
            self.settings_page.update_theme_buttons(theme)

        self.theme_changed.emit(theme)
        self.logger.info(f"主题已切换: {theme}")

    def _load_theme_stylesheet(self, theme: str) -> str:
        """加载主题样式表"""
        from script.paths import resource_path

        style_file = 'styles/modern.qss' if theme == 'dark' else 'styles/light.qss'
        qss_path = resource_path(style_file)

        try:
            if qss_path.exists():
                with open(qss_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                self.logger.warning(f"样式文件不存在: {qss_path}")
                return ""
        except Exception as e:
            self.logger.error(f"加载样式表失败: {e}")
            return ""

    def _init_ui(self) -> None:
        """初始化用户界面"""
        # 窗口设置
        app_name = self.config_manager.get('app.name', 'war3技能文本生成器')
        self.setWindowTitle(app_name)

        min_width = self.config_manager.get('window.minimum_width', 900)
        min_height = self.config_manager.get('window.minimum_height', 600)
        self.setMinimumSize(min_width, min_height)

        # 默认大小
        width = self.config_manager.get('window.width', 1100)
        height = self.config_manager.get('window.height', 720)
        self.resize(width, height)

        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局：垂直布局，顶部标题栏 + 下方内容区
        root_layout = QVBoxLayout(central_widget)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ========== 自绘标题栏 ==========
        self.title_bar = TitleBar(self)
        self.title_bar.set_title(app_name)
        root_layout.addWidget(self.title_bar)

        # ========== 顶部主切换栏 ==========
        self._create_top_tabbar(root_layout)

        # ========== 内容区 ==========
        self._create_content_area(root_layout)

    def _create_top_tabbar(self, parent_layout: QVBoxLayout) -> None:
        """创建顶部主切换栏（替代左侧导航）"""
        top_tabs = QFrame()
        top_tabs.setProperty("class", "homepage-top-tabs")

        layout = QHBoxLayout(top_tabs)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.top_edit_btn = QPushButton("✎编辑文本")
        self.top_edit_btn.setProperty("class", "homepage-top-tab")
        self.top_edit_btn.setCheckable(True)
        self.top_edit_btn.setChecked(True)
        self.top_edit_btn.setFixedHeight(44)
        self.top_edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.top_edit_btn)

        self.top_color_btn = QPushButton("⚙色彩")
        self.top_color_btn.setProperty("class", "homepage-top-tab")
        self.top_color_btn.setCheckable(True)
        self.top_color_btn.setFixedHeight(44)
        self.top_color_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.top_color_btn)

        self.top_log_btn = QPushButton("☰更新日志")
        self.top_log_btn.setProperty("class", "homepage-top-tab")
        self.top_log_btn.setCheckable(True)
        self.top_log_btn.setFixedHeight(44)
        self.top_log_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.top_log_btn)

        layout.addStretch()
        parent_layout.addWidget(top_tabs)

    def _create_content_area(self, parent_layout) -> None:
        """创建右侧内容区"""
        self.content_widget = QFrame()
        self.content_widget.setProperty("class", "content-area")

        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # 页面堆栈
        self.page_stack = QStackedWidget()

        # 创建各页面
        self.dashboard_page = DashboardPage()
        self.http_page = HttpClientPage(self.config_manager)
        self.settings_page = SettingsPage(self.config_manager)
        self.about_page = AboutPage(self.config_manager)

        self.page_stack.addWidget(self.dashboard_page)
        self.page_stack.addWidget(self.http_page)
        self.page_stack.addWidget(self.settings_page)
        self.page_stack.addWidget(self.about_page)

        content_layout.addWidget(self.page_stack)

        parent_layout.addWidget(self.content_widget)

    def _init_statusbar(self) -> None:
        """初始化状态栏"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.status_bar.showMessage("就绪")

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFixedWidth(150)
        self.status_bar.addPermanentWidget(self.progress_bar)

    def _load_window_state(self) -> None:
        """加载窗口状态"""
        if self.config_manager.get('window.remember_geometry', True):
            geometry = self.config_manager.get('window.geometry', '')
            if geometry:
                try:
                    import base64
                    self.restoreGeometry(bytes.fromhex(geometry))
                except Exception:
                    pass

    def _save_window_state(self) -> None:
        """保存窗口状态"""
        if self.config_manager.get('window.remember_geometry', True):
            geometry = self.saveGeometry().toHex().data().decode()
            self.config_manager.set('window.geometry', geometry)

    def _connect_signals(self) -> None:
        """连接信号"""
        # 顶部主切换栏
        self.top_edit_btn.clicked.connect(lambda: self._switch_page(0))
        self.top_color_btn.clicked.connect(lambda: self._switch_page(2))
        self.top_log_btn.clicked.connect(lambda: self._switch_page(3))

        # Dashboard 快捷按钮（当前阶段）
        self.dashboard_page.save_btn.clicked.connect(lambda: self.status_bar.showMessage("已保存（界面阶段占位）"))
        self.dashboard_page.generate_btn.clicked.connect(lambda: self.status_bar.showMessage("已更新预览"))

        # 设置页面主题切换
        self.settings_page.theme_changed.connect(self.apply_theme)

        # 标题栏按钮信号
        self.title_bar.theme_clicked.connect(self.apply_theme)
        self.title_bar.settings_clicked.connect(lambda: self._switch_page(2))

    def _switch_page(self, index: int) -> None:
        """切换页面"""
        self.page_stack.setCurrentIndex(index)

        # 更新顶部按钮状态
        self.top_edit_btn.setChecked(index == 0)
        self.top_color_btn.setChecked(index == 2)
        self.top_log_btn.setChecked(index == 3)

        # 更新状态栏
        page_names = ["编辑文本", "HTTP 客户端", "色彩", "更新日志"]
        self.status_bar.showMessage(f"{page_names[index]}")

    def closeEvent(self, event) -> None:
        """窗口关闭事件"""
        self._save_window_state()
        self.logger.info("应用程序关闭")
        event.accept()

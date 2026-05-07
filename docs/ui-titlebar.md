# 自绘标题栏与主题系统

本文档说明 PyQt EXE 模板的自绘标题栏结构、配置方式及主题同步机制。

## 标题栏结构

应用使用自绘标题栏（FramelessWindowHint），布局从左到右：

```
[应用标题] [标题工具栏] [拖拽空白区] [主题切换] [设置] [最小化] [最大化] [关闭]
```

| 区域 | 说明 |
|------|------|
| 应用标题 | 显示应用名称，可配置 |
| 标题工具栏 | VSCode 风格的下拉菜单按钮 |
| 拖拽空白区 | stretch 占位，用于窗口拖拽 |
| 主题切换 | 深色/浅色主题 pill 按钮 |
| 设置按钮 | 跳转到设置页面 |
| 窗口控制 | 最小化、最大化/还原、关闭 |

## 标题工具栏配置

标题工具栏的内容通过 `_get_title_toolbar_items()` 方法配置，支持灵活替换。

### 配置结构

```python
def _get_title_toolbar_items(self) -> list:
    return [
        {
            "key": "file",           # 唯一标识
            "text": "文件(F)",        # 显示文本
            "menu_items": [          # 菜单项列表
                {"text": "新建项目", "shortcut": "Ctrl+N", "callback": "_action_new_project"},
                {"separator": True},
                {"text": "退出", "shortcut": "Alt+F4", "callback": "_on_close"},
            ]
        },
        # 更多工具按钮...
    ]
```

### 菜单项配置

| 字段 | 类型 | 说明 |
|------|------|------|
| text | str | 菜单项显示文本 |
| shortcut | str | 快捷键（可选） |
| callback | str | 回调方法名（字符串形式） |
| separator | bool | 是否为分隔线 |

### 添加自定义工具按钮

在 `script/gui.py` 的 `TitleBar` 类中修改配置：

```python
def _get_title_toolbar_items(self) -> list:
    items = [
        # 基础示例按钮
        {"key": "file", "text": "文件(F)", "menu_items": [...]},
        {"key": "edit", "text": "编辑(E)", "menu_items": [...]},

        # 添加自定义按钮
        {
            "key": "tools",
            "text": "工具(T)",
            "menu_items": [
                {"text": "数据导入", "shortcut": "Ctrl+I", "callback": "_action_import"},
                {"text": "数据导出", "shortcut": "Ctrl+E", "callback": "_action_export"},
            ]
        },
    ]
    return items

# 添加对应的回调方法
def _action_import(self):
    # 导入逻辑
    pass

def _action_export(self):
    # 导出逻辑
    pass
```

### 按钮宽度规则

标题工具栏按钮使用**内容自适应宽度**：

- 使用 `QSizePolicy.Fixed` 策略
- 宽度 = 文字宽度 + 左右 padding（共 20px）
- 不使用 `Expanding` 策略
- stretch 只放在工具栏之后，作为拖拽区域

## 主题同步机制

主题切换使用**统一入口**，确保标题栏和设置页状态同步。

### 切换入口

`MainWindow.apply_theme(theme)` 是唯一主题切换入口：

```python
def apply_theme(self, theme: str) -> None:
    """应用主题 - 统一入口"""
    self._current_theme = theme
    self.config_manager.set('ui.theme', theme)

    # 加载样式表
    stylesheet = self._load_theme_stylesheet(theme)
    QApplication.instance().setStyleSheet(stylesheet)

    # 同步所有主题控件状态
    self.title_bar.update_theme_state(theme)      # 标题栏按钮
    self.settings_page.update_theme_buttons(theme) # 设置页按钮
```

### 切换方式

两种方式触发主题切换，效果相同：

1. **标题栏按钮** - 点击深色/浅色 pill 按钮
2. **设置页面** - 点击主题选择按钮

两种方式都会：
- 更新全局 QSS 样式
- 同步标题栏按钮状态
- 同步设置页按钮状态
- 保存主题配置到 YAML

## 窗口控制按钮

| 按钮 | 功能 | 说明 |
|------|------|------|
| ─ | 最小化 | 最小化窗口到任务栏 |
| □ | 最大化/还原 | 切换窗口最大化状态 |
| ✕ | 关闭 | 关闭窗口 |

### 最大化状态同步

最大化/还原按钮会根据窗口状态切换显示：

```python
def _on_maximize(self) -> None:
    if self.parent_window.isMaximized():
        self.parent_window.showNormal()
        self.maximize_btn.setText("□")
    else:
        self.parent_window.showMaximized()
        self.maximize_btn.setText("❐")
```

## 样式定制

### 深色主题 (modern.qss)

```css
/* 标题工具栏按钮 */
QPushButton[class="title-menu-btn"] {
    background-color: transparent;
    color: #94A3B8;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
}

QPushButton[class="title-menu-btn"]:hover {
    background-color: #334155;
    color: #E2E8F0;
}

/* 窗口控制按钮 */
QPushButton[class="title-win-btn"]:hover {
    background-color: #334155;
}

QPushButton[class="title-close-btn"]:hover {
    background-color: #DC2626;  /* 关闭按钮红色悬停 */
}
```

### 浅色主题 (light.qss)

```css
QPushButton[class="title-menu-btn"] {
    color: #64748B;
}

QPushButton[class="title-menu-btn"]:hover {
    background-color: #F1F5F9;
    color: #1E293B;
}

QPushButton[class="title-close-btn"]:hover {
    background-color: #DC2626;
    color: #FFFFFF;
}
```

## 窗口拖拽

标题栏空白区域支持窗口拖拽：

- 双击：最大化/还原窗口
- 拖拽：移动窗口位置
- 拖拽区域：工具栏之后、右侧控制区之前

## 注意事项

1. **按钮宽度**：不要使用 `QSizePolicy.Expanding`，避免按钮被拉伸
2. **stretch 位置**：只放在工具栏之后，不能放在按钮之间
3. **主题切换**：必须通过 `MainWindow.apply_theme()` 切换，保证同步
4. **菜单样式**：深色/浅色主题的菜单样式需要分别配置

## 相关文件

| 文件 | 说明 |
|------|------|
| `script/gui.py` | TitleBar 类，标题栏实现 |
| `script/main.py` | 主题加载入口 |
| `resources/styles/modern.qss` | 深色主题样式 |
| `resources/styles/light.qss` | 浅色主题样式 |
| `config/setting.yaml` | 主题配置存储 |

---

> 文档版本: 1.0.0  
> 最后更新: 2026-04-30

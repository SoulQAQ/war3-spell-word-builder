# PyQt EXE 模板 - 快速入门指南

> 本模板是一个现代化的 PyQt6 桌面应用程序基础框架，帮助你快速开发 Windows 工具程序。

## 模板能做什么

### ✅ 内置功能

| 功能 | 说明 |
|------|------|
| 现代深色 UI | 无边框窗口设计，紧凑布局，自定义标题栏 |
| 配置管理 | YAML 配置文件，支持应用名称、窗口大小、网络设置等 |
| HTTP 客户端 | 内置请求工具，支持 GET/POST/PUT/DELETE，带重试机制 |
| 日志系统 | 同时输出到控制台和文件，方便调试和追踪 |
| 文件目录 | 自动管理输入/输出/日志目录 |
| EXE 打包 | 一键打包为 Windows 可执行文件 |

### 📦 页面结构

```
┌─────────────────────────────────────────────────────────────────────────┐
│ PyQt EXE 模板  文件(F) 编辑(E) 选择(S) 查看(V)    [🌙][☀️] | [⚙️] [─][□][✕] │ ← 自绘标题栏
├──────────┬──────────────────────────────────────────────────────────────┤
│          │                                                              │
│  首页    │   欢迎使用 PyQt EXE 模板                                      │
│          │                                                              │
│  HTTP    │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │
│  客户端  │   │PyQt6界面│ │HTTP客户端│ │配置管理 │ │EXE打包  │          │
│          │   └─────────┘ └─────────┘ └─────────┘ └─────────┘          │
│  设置    │                                                              │
│          │   快捷操作                                                   │
│  关于    │   [打开配置目录] [打开输出目录] [测试请求]                    │
│          │                                                              │
├──────────┴──────────────────────────────────────────────────────────────┤
│  就绪                                                                    │ ← 状态栏
└─────────────────────────────────────────────────────────────────────────┘
```

### 🎨 标题栏功能

自绘标题栏包含：

| 功能 | 说明 |
|------|------|
| 应用标题 | 显示应用名称 |
| 标题工具栏 | VSCode 风格下拉菜单（文件/编辑/选择/查看） |
| 主题切换 | 深色/浅色主题 pill 按钮 |
| 设置按钮 | 跳转设置页面 |
| 窗口控制 | 最小化、最大化/还原、关闭 |

> 详细说明见 [ui-titlebar.md](ui-titlebar.md)

## 快速开始

### 运行程序

```bash
# 方式一：使用启动脚本（推荐）
start-uv.bat

# 方式二：直接运行 Python
python script/main.py
```

### 目录说明

```
pyqt-exe-template/
├── script/         ← 你的代码放这里
│   ├── main.py     ← 程序入口
│   ├── gui.py      ← UI 界面
│   └── ...         ← 其他模块
├── config/         ← 配置文件
│   └── setting.yaml
├── resources/      ← 资源文件
│   └── styles/     ← QSS 样式
├── rundata/        ← 运行时数据（自动创建）
│   ├── logs/       ← 日志文件
│   ├── input/      ← 输入文件
│   └── output/     ← 输出文件
└── dist/           ← 打包后的 EXE
```

## 内置页面介绍

### 🏠 首页 (Dashboard)

- 欢迎信息和应用介绍
- 功能特性卡片展示
- 快捷操作按钮：打开配置目录、打开输出目录、测试 HTTP

### 🌐 HTTP 客户端

- 支持 GET、POST、PUT、DELETE 方法
- 自定义请求头（JSON 格式）
- 自定义请求体（JSON 格式）
- 显示响应状态码、耗时、格式化 JSON 结果

### ⚙️ 设置

- 应用名称和版本配置
- 网络超时时间设置
- 输出路径配置
- 保存设置 / 恢复默认

### 📖 关于

- 应用信息和版本
- 技术栈说明
- 项目链接

## 配置文件

`config/setting.yaml` 内容：

```yaml
app:
  name: PyQt EXE Template    # 应用名称
  version: 1.0.0             # 版本号

window:
  width: 1100                # 默认宽度
  height: 720                # 默认高度
  minimum_width: 900         # 最小宽度
  minimum_height: 600        # 最小高度

network:
  timeout: 30                # 请求超时(秒)
  retry_count: 2             # 重试次数
  default_url: https://httpbin.org/get

user_settings:
  input_path: ./rundata/input
  output_path: ./rundata/output

ui:
  theme: dark                # 主题
  accent_color: '#4F8CFF'    # 主色调
```

修改配置后重启程序生效。

## 打包为 EXE

```bash
# 运行打包脚本
build.bat

# 输出位置
dist/pyqt-exe-template.exe
```

打包后的 EXE：
- 单文件，无需安装 Python
- 包含所有依赖和资源
- 可独立运行，双击启动

## 基于模板开发新工具

### 1. 复制模板

将整个目录复制到新项目位置，重命名。

### 2. 修改基本信息

编辑 `config/setting.yaml`：
```yaml
app:
  name: 我的工具
  version: 1.0.0
```

编辑 `pyqt-exe-template.spec`（第63行）：
```python
name='my-tool',  # EXE 文件名
```

### 3. 添加新功能页面

在 `script/gui.py` 中：

1. 创建新页面类：
```python
class MyFeaturePage(QWidget):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        # 添加你的 UI 组件...
```

2. 在 MainWindow 中注册页面和导航按钮

### 4. 使用内置模块

```python
# 配置管理
from script.config_manager import get_config_manager
config = get_config_manager()
value = config.get('user_settings.output_path')

# HTTP 请求
from script.network import create_http_client
client = create_http_client(base_url='https://api.example.com')
response = client.get('/data')

# 日志
from script.logger import get_logger
logger = get_logger()
logger.info("操作完成")

# 路径
from script.paths import OUTPUT_DIR, ensure_dir
ensure_dir(OUTPUT_DIR)

# 工具函数
from script.utils import open_folder, format_json
open_folder(OUTPUT_DIR)
```

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.12+ | 运行环境 |
| PyQt6 | 最新 | GUI 框架 |
| requests | 最新 | HTTP 请求 |
| PyYAML | 最新 | 配置文件 |
| PyInstaller | 最新 | EXE 打包 |

## 常见问题

**Q: 如何修改窗口大小？**
A: 编辑 `config/setting.yaml` 中的 `window.width` 和 `window.height`。

**Q: 如何修改主题颜色？**
A: 编辑 `resources/styles/modern.qss`，修改颜色值（如 `#4F8CFF`）。

**Q: 日志文件在哪？**
A: `rundata/logs/app.log`。

**Q: 打包后配置文件在哪？**
A: EXE 同级的 `config/` 目录，可用户修改。

**Q: 如何添加图标？**
A: 替换 `app.ico` 文件，重新打包。

## 更多信息

- 详细架构文档：`docs/architecture.md`
- AI 开发指南：`docs/agent-guide.md`
- 项目仓库：https://github.com/SoulQAQ/pyqt-exe-template
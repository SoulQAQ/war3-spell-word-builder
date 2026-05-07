# PyQt EXE Template

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)

[English](README.md) | [中文](README.zh-CN.md)

一个现代化的 PyQt6 桌面应用程序模板，内置 HTTP 客户端支持、配置管理功能和 PyInstaller 打包能力。

## 项目简介

本项目提供了一个完整的、可用于生产环境的 PyQt6 Windows 桌面应用程序模板。主要特性包括：

- **现代化深色主题 UI** - 使用 QSS 样式的美观专业界面
- **HTTP 客户端集成** - 内置 HTTP 请求测试工具，支持异步请求
- **YAML 配置管理** - 灵活的配置管理系统
- **PyInstaller 就绪** - 轻松打包为 Windows 单文件 EXE
- **清晰的项目结构** - 遵循最佳实践的代码组织

> **注意**：本模板使用 **PyQt6** 作为 UI 框架，不使用 pywebview、Electron 或任何基于 Web 的 UI 方案。

## 功能特性

- ✅ 现代化深色主题，自定义 QSS 样式
- ✅ 侧边导航栏，支持页面切换
- ✅ Dashboard 首页，包含功能卡片和快捷操作
- ✅ HTTP Client 页面，支持 API 测试（GET、POST、PUT、DELETE）
- ✅ Settings 设置页面，支持配置编辑
- ✅ About 关于页面，展示项目信息
- ✅ 后台 HTTP 请求（不阻塞 UI）
- ✅ 基于 YAML 的配置管理
- ✅ 窗口状态持久化
- ✅ 日志系统
- ✅ PyInstaller 打包支持

## 界面预览

> **占位说明**：可通过运行程序截取界面截图后添加。

## 技术栈

| 组件 | 技术 |
|------|------|
| UI 框架 | PyQt6 |
| HTTP 客户端 | requests |
| 配置管理 | PyYAML |
| 打包工具 | PyInstaller |
| 日志系统 | Python logging |
| 样式系统 | QSS (Qt Style Sheets) |

## 项目结构

```
pyqt-exe-template/
├── .gitignore                 # Git 忽略配置
├── app.ico                    # 应用图标
├── logo.png                   # 应用 Logo
├── README.md                  # 英文文档
├── README.zh-CN.md            # 中文文档
├── requirements.txt           # Python 依赖
├── setup.bat                  # 环境安装脚本
├── start.bat                  # 程序启动脚本
├── build.bat                  # 打包脚本
├── pyqt-exe-template.spec     # PyInstaller 配置
├── generate_icons.py          # 图标生成脚本
│
├── config/
│   └── setting.yaml           # 应用配置文件
│
├── script/
│   ├── __init__.py
│   ├── main.py                # 程序入口
│   ├── gui.py                 # 主窗口和 UI
│   ├── config_manager.py      # 配置管理
│   ├── network.py             # HTTP 客户端封装
│   ├── logger.py              # 日志系统
│   ├── paths.py               # 路径处理
│   └── utils.py               # 工具函数
│
├── resources/
│   ├── icons/                 # 图标资源
│   ├── images/                # 图片资源
│   └── styles/
│       └── modern.qss         # QSS 样式表
│
├── rundata/
│   ├── input/                 # 输入数据目录
│   ├── output/                # 输出数据目录
│   └── logs/                  # 日志文件目录
│
└── docs/
    └── architecture.md        # 架构文档
```

## 环境要求

- **操作系统**: Windows 10/11
- **Python**: 3.12（推荐）
- **依赖**: 见 `requirements.txt`

## 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/SoulQAQ/pyqt-exe-template.git
cd pyqt-exe-template
```

### 2. 安装依赖

运行安装脚本：

```bash
setup.bat
```

或手动安装：

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### 3. 生成图标（可选）

如果图标文件不存在，生成占位图标：

```bash
python generate_icons.py
```

### 4. 启动程序

**使用 pip（传统方式）：**
```bash
start.bat
```

**使用 uv（更快）：**
```bash
start-uv.bat
```

或直接运行：

```bash
.venv\Scripts\python script\main.py
```

## 打包 EXE

### 使用 build.bat

```bash
build.bat
```

输出文件：`dist\pyqt-exe-template.exe`

### 手动打包

```bash
.venv\Scripts\pip install pyinstaller
.venv\Scripts\python -m PyInstaller pyqt-exe-template.spec
```

## 配置说明

配置文件位于 `config/setting.yaml`：

```yaml
app:
  name: "PyQt EXE Template"
  version: "1.0.0"
  language: "en-US"

window:
  width: 1100
  height: 720
  minimum_width: 900
  minimum_height: 600

network:
  timeout: 30
  retry_count: 2
  default_url: "https://httpbin.org/get"

user_settings:
  input_path: "./rundata/input"
  output_path: "./rundata/output"
```

## HTTP 请求示例

内置的 HTTP Client 可以测试 API 请求：

1. 导航到 **HTTP Client** 页面
2. 输入 URL（默认：`https://httpbin.org/get`）
3. 选择请求方法（GET、POST、PUT、DELETE）
4. 添加请求头（JSON 格式）
5. 添加请求体（JSON 格式，用于 POST/PUT）
6. 点击 **Send Request**

响应将显示：
- 状态码
- 响应时间
- JSON 格式化的响应内容

## 开发指南

### 添加新页面

1. 在 `gui.py` 中创建新的页面类：
```python
class NewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # 添加 UI 组件
        pass
```

2. 在 `MainWindow` 中添加导航按钮并连接信号

### 自定义样式

编辑 `resources/styles/modern.qss` 来自定义：
- 颜色
- 字体
- 边框
- 按钮样式
- 输入框样式

### 添加新配置项

1. 在 `config_manager.py` 的 `_get_defaults()` 中添加默认值
2. 更新 `config/setting.yaml`

## 打包说明

### PyInstaller 资源路径

打包后，资源文件会被解压到临时目录（`sys._MEIPASS`）。`paths.py` 模块会自动处理：

```python
from script.paths import resource_path
icon_path = resource_path('icons/my_icon.png')
```

### 包含的文件

- `resources/` - 所有 UI 资源
- `config/` - 配置文件
- `app.ico` - 应用图标

### 排除的模块

为减小 EXE 体积，以下模块被排除：
- tkinter
- matplotlib
- numpy
- pandas
- scipy

## 常见问题

### Q: 为什么使用 PyQt6 而不是 pywebview？

PyQt6 提供：
- 原生桌面性能
- 更好的 Windows 集成
- 无需 Web 浏览器依赖
- 对 UI 组件的更多控制

### Q: 如何更换应用图标？

用你自己的图标文件替换 `app.ico`（推荐：256x256 多分辨率 ICO）。

### Q: 如何添加新依赖？

1. 添加到 `requirements.txt`
2. 添加到 `pyqt-exe-template.spec` 的 `hiddenimports`
3. 运行 `setup.bat` 更新环境

## 路线图

- [ ] 多语言支持（i18n）
- [ ] 插件系统
- [ ] 更多 HTTP 功能（认证、文件上传）
- [ ] 深色/浅色主题切换
- [ ] 导出/导入配置

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

## 许可证

本项目采用 **GNU General Public License v3.0** 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 仓库地址

**GitHub**: [https://github.com/SoulQAQ/pyqt-exe-template](https://github.com/SoulQAQ/pyqt-exe-template)

---

使用 PyQt6 用心构建 ❤️
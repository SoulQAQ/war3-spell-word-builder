# PyQt EXE 模板 - AI Agent 开发指南

> 本文档专为 AI Agent 编写，帮助快速理解项目架构，高效开发新工具程序。

## 项目定位

这是一个 **PyQt6 桌面应用程序基础模板**，作为开发其他工具程序的起点。核心特性：
- 现代深色主题 UI，无边框窗口设计
- 模块化架构：配置管理、日志系统、HTTP 客户端、路径处理
- PyInstaller 打包支持，一键生成 Windows EXE

## 目录结构

```
pyqt-exe-template/
├── script/                 # 核心代码目录
│   ├── main.py             # 程序入口，初始化 QApplication
│   ├── gui.py              # 主窗口及所有 UI 组件（~35KB）
│   ├── config_manager.py   # YAML 配置管理，支持嵌套键访问
│   ├── network.py          # HTTP 客户端封装，带重试机制
│   ├── logger.py           # 日志系统，同时输出到控制台和文件
│   ├── paths.py            # 路径处理，兼容开发/打包环境
│   └── utils.py            # 工具函数（JSON、路径、时间格式化等）
├── config/
│   └── setting.yaml        # 主配置文件
├── resources/
│   └── styles/modern.qss   # QSS 样式表（深色主题）
├── rundata/                # 运行时数据（自动创建）
│   ├── logs/               # 日志文件
│   ├── input/              # 输入文件目录
│   └── output/             # 输出文件目录
├── docs/                   # 文档目录
├── pyqt-exe-template.spec  # PyInstaller 打包配置
├── start.bat / start-uv.bat # 启动脚本
└── build.bat               # 打包脚本
```

## 核心模块使用

### 1. 配置管理 (`config_manager.py`)

```python
from script.config_manager import get_config_manager

config = get_config_manager()

# 读取配置（支持点分隔嵌套键）
timeout = config.get('network.timeout', 30)
app_name = config.get('app.name', '默认名称')

# 写入配置（自动保存）
config.set('user_settings.output_path', '/path/to/output')

# 获取所有配置
all_config = config.get_all()

# 重置为默认配置
config.reset_to_defaults()
```

**配置文件结构** (`config/setting.yaml`)：
```yaml
app:
  name: PyQt EXE Template
  version: 1.0.0
window:
  width: 1100
  height: 720
  minimum_width: 900
  minimum_height: 600
network:
  timeout: 30
  retry_count: 2
user_settings:
  input_path: ./rundata/input
  output_path: ./rundata/output
ui:
  theme: dark
  accent_color: '#4F8CFF'
```

### 2. HTTP 客户端 (`network.py`)

```python
from script.network import HttpClient, create_http_client, get_http_client

# 方式一：创建独立客户端
client = create_http_client(base_url='https://api.example.com', timeout=30)

# 发送请求
response = client.get('/users')
response = client.post('/users', json_data={'name': 'test'})
response = client.put('/users/1', json_data={'name': 'updated'})
response = client.delete('/users/1')

# 下载文件
client.download('/files/data.zip', save_path='./output/data.zip')

# 检查响应
if response.success:
    print(f"状态码: {response.status_code}")
    print(f"数据: {response.data}")
    print(f"耗时: {response.elapsed_ms}ms")

# 方式二：使用全局客户端
client = get_http_client()
```

**HttpResponse 结构**：
```python
@dataclass
class HttpResponse:
    success: bool        # 是否成功 (status 200-299)
    status_code: int     # HTTP 状态码
    data: Any            # JSON 解析后的数据
    text: str            # 响应文本
    message: str         # 错误信息
    headers: Dict        # 响应头
    elapsed_ms: float    # 请求耗时(毫秒)
```

### 3. 日志系统 (`logger.py`)

```python
from script.logger import get_logger, init_logging, log_info, log_error

# 获取日志器
logger = get_logger()
logger.info("操作完成")
logger.error("出错了")

# 快捷函数
log_info("信息")
log_error("错误")
log_warning("警告")
log_exception("异常信息")  # 自动包含堆栈

# 日志文件位置: rundata/logs/app.log
```

### 4. 路径处理 (`paths.py`)

```python
from script.paths import (
    APP_DIR,      # 应用根目录
    RESOURCE_DIR, # 资源目录 (resources/)
    CONFIG_DIR,   # 配置目录 (config/)
    LOGS_DIR,     # 日志目录 (rundata/logs/)
    INPUT_DIR,    # 输入目录 (rundata/input/)
    OUTPUT_DIR,   # 输出目录 (rundata/output/)
    resource_path,  # 获取资源文件路径
    ensure_dir      # 确保目录存在
)

# 获取资源文件路径
qss_path = resource_path('styles/modern.qss')

# 确保目录存在
ensure_dir(OUTPUT_DIR)
```

**重要**：路径模块自动处理开发环境与 PyInstaller 打包环境的差异。

### 5. 工具函数 (`utils.py`)

```python
from script.utils import (
    open_folder,       # 在系统文件管理器打开文件夹
    safe_json_loads,   # 安全解析 JSON
    format_json,       # 格式化 JSON 输出
    current_timestamp, # 获取时间戳字符串
    format_bytes,      # 格式化字节数 (1024 → "1.00 KB")
    format_duration,   # 格式化时长 (3661 → "1h 1m")
    ensure_absolute_path,  # 转换为绝对路径
)

# 示例
open_folder(OUTPUT_DIR)
data = safe_json_loads('{"key": "value"}', default={})
print(format_json(data))
print(current_timestamp())  # "2026-04-29 10:30:00"
```

## UI 开发指南

### 主窗口结构 (`gui.py`)

```
MainWindow (QMainWindow)
├── TitleBar (自定义标题栏，含菜单栏 + 窗口按钮)
├── NavWidget (左侧导航栏，固定宽度 180px)
│   └── NavButton (导航按钮，高度 36px)
├── ContentArea (右侧内容区)
│   └── PageStack (QStackedWidget 页面容器)
│       ├── DashboardPage (首页)
│       ├── HttpClientPage (HTTP 客户端)
│       ├── SettingsPage (设置页)
│       └── AboutPage (关于页)
└── StatusBar (状态栏)
```

### 添加新页面步骤

1. **创建页面类** (继承 QWidget)：

```python
class MyNewPage(QWidget):
    def __init__(self, config_manager: ConfigManager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        title = QLabel("页面标题")
        title.setProperty("class", "page-title")
        title.setFont(QFont("Microsoft YaHei UI", 18, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # ... 添加其他组件
        
        layout.addStretch()
```

2. **在 MainWindow 中注册**：

```python
# _create_content_area 方法中
self.my_page = MyNewPage(self.config_manager)
self.page_stack.addWidget(self.my_page)

# _create_navbar 方法中添加导航按钮
self.my_btn = NavButton("新页面")
nav_layout.addWidget(self.my_btn)
self.nav_buttons.append(self.my_btn)

# _connect_signals 方法中连接信号
self.my_btn.clicked.connect(lambda: self._switch_page(4))  # 页面索引

# _switch_page 方法中更新页面名称列表
page_names = ["首页", "HTTP 客户端", "设置", "关于", "新页面"]
```

### 可复用 UI 组件

- **`NavButton`** - 导航按钮，自动样式，可选中状态
- **`CardWidget`** - 卡片组件，带标题和描述
- **`TitleBar`** - 自定义标题栏，含窗口控制按钮

### QSS 样式类名

在 QSS 中通过 `setProperty("class", "xxx")` 应用样式：

| 类名 | 用途 |
|------|------|
| `page-title` | 页面大标题 (18pt bold) |
| `page-subtitle` | 页面副标题 (9pt gray) |
| `section-title` | 区块标题 (12pt bold) |
| `nav-button` | 导航按钮 |
| `primary-button` | 主要按钮 (蓝色) |
| `secondary-button` |次要按钮 (灰色) |
| `action-button` | 操作按钮 |
| `card` | 卡片容器 |
| `card-title` | 卡片标题 |
| `settings-group` | 设置分组框 |

## 常见开发任务

### 修改应用名称/版本

编辑 `config/setting.yaml`：
```yaml
app:
  name: 我的工具
  version: 2.0.0
```

或修改 `config_manager.py` 中的 `_get_defaults()` 方法。

### 修改窗口大小

```yaml
window:
  width: 1200
  height: 800
  minimum_width: 800
  minimum_height: 500
```

### 修改主题颜色

编辑 `resources/styles/modern.qss`：
- 主色调：`#4F8CFF` (蓝色)
- 背景色：`#0F172A` (深蓝黑)
- 卡片背景：`#1E293B`
- 边框色：`#334155`

### 添加 HTTP API 调用

```python
from script.network import create_http_client

client = create_http_client(base_url='https://api.example.com')
response = client.get('/endpoint')

if response.success:
    self.result_display.setText(format_json(response.data))
else:
    QMessageBox.warning(self, "错误", response.message)
```

### 异步 HTTP 请求

参考 `HttpClientPage` 中的 `HttpRequestWorker` (QThread) 实现：

```python
class MyWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def run(self):
        client = create_http_client()
        response = client.get('https://api.example.com/data')
        if response.success:
            self.finished.emit(response.data)
        else:
            self.error.emit(response.message)

# 使用
worker = MyWorker()
worker.finished.connect(self.on_success)
worker.error.connect(self.on_error)
worker.start()
```

## 打包发布

```bash
# 使用 build.bat 打包
./build.bat

# 生成文件位置: dist/pyqt-exe-template.exe
```

打包后的 EXE 会包含：
- 所有 Python 代码
- resources/ 目录（样式、图标）
- config/ 目录（默认配置）
- app.ico 图标

**注意**：打包后的配置文件在 EXE 同级 `config/` 目录，可用户修改。

## 开发新项目流程

1. **复制模板目录** 到新项目位置
2. **修改配置**：
   - `config/setting.yaml` - 应用名称、版本
   - `pyqt-exe-template.spec` - EXE 名称
3. **修改 UI**：
   - 编辑 `gui.py` 添加/删除页面
   - 编辑 `modern.qss` 调整样式
4. **添加功能**：
   - 在 `script/` 下添加新模块
   - 在页面中集成功能
5. **测试运行**：`start-uv.bat` 或 `python script/main.py`
6. **打包发布**：`build.bat`

## 注意事项

- 路径问题始终使用 `paths.py` 中的函数，不要硬编码
- 配置修改后调用 `config.save()` 或使用 `auto_save=True`
- HTTP 请求在 UI 中使用 QThread 异步执行
- QSS 样式通过 `setProperty("class", "xxx")` 应用，不要用 setStyleSheet
- 日志输出到 `rundata/logs/app.log`，打包后依然有效
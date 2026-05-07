# PyQt EXE Template

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](LICENSE)

[English](README.md) | [中文](README.zh-CN.md)

A modern PyQt6 desktop application template with HTTP client support, configuration management, and PyInstaller packaging capability.

## Overview

This project provides a complete, production-ready template for building PyQt6 desktop applications on Windows. It features:

- **Modern Dark Theme UI** - Beautiful, professional-looking interface with QSS styling
- **HTTP Client Integration** - Built-in HTTP request testing tool with async support
- **YAML Configuration** - Flexible configuration management system
- **PyInstaller Ready** - Easy Windows EXE packaging with single-file output
- **Clean Project Structure** - Well-organized codebase following best practices

> **Note**: This template uses **PyQt6** as the UI framework. It does NOT use pywebview, Electron, or any web-based UI solutions.

## Features

- ✅ Modern dark theme with custom QSS styling
- ✅ Navigation sidebar with page switching
- ✅ Dashboard with feature cards and quick actions
- ✅ HTTP Client page for API testing (GET, POST, PUT, DELETE)
- ✅ Settings page with configuration editing
- ✅ About page with project information
- ✅ Background HTTP requests (non-blocking UI)
- ✅ YAML-based configuration management
- ✅ Window state persistence
- ✅ Logging system
- ✅ PyInstaller packaging support

## Screenshots

> **Placeholder**: Screenshots can be added by running the application and capturing the UI.

## Tech Stack

| Component | Technology |
|-----------|------------|
| UI Framework | PyQt6 |
| HTTP Client | requests |
| Configuration | PyYAML |
| Packaging | PyInstaller |
| Logging | Python logging |
| Styling | QSS (Qt Style Sheets) |

## Project Structure

```
pyqt-exe-template/
├── .gitignore                 # Git ignore configuration
├── app.ico                    # Application icon
├── logo.png                   # Application logo
├── README.md                  # English documentation
├── README.zh-CN.md            # Chinese documentation
├── requirements.txt           # Python dependencies
├── setup.bat                  # Environment setup script
├── start.bat                  # Application launcher
├── build.bat                  # Build script
├── pyqt-exe-template.spec     # PyInstaller configuration
├── generate_icons.py          # Icon generation script
│
├── config/
│   └── setting.yaml           # Application configuration
│
├── script/
│   ├── __init__.py
│   ├── main.py                # Application entry point
│   ├── gui.py                 # Main window and UI
│   ├── config_manager.py      # Configuration management
│   ├── network.py             # HTTP client wrapper
│   ├── logger.py              # Logging system
│   ├── paths.py               # Path handling
│   └── utils.py               # Utility functions
│
├── resources/
│   ├── icons/                 # Icon resources
│   ├── images/                # Image resources
│   └── styles/
│       └── modern.qss         # QSS stylesheet
│
├── rundata/
│   ├── input/                 # Input data directory
│   ├── output/                # Output data directory
│   └── logs/                  # Log files directory
│
└── docs/
    └── architecture.md        # Architecture documentation
```

## Requirements

- **Operating System**: Windows 10/11
- **Python**: 3.12 (recommended)
- **Dependencies**: See `requirements.txt`

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/SoulQAQ/pyqt-exe-template.git
cd pyqt-exe-template
```

### 2. Setup Environment

Run the setup script:

```bash
setup.bat
```

Or manually:

```bash
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

### 3. Generate Icons (Optional)

If icons don't exist, generate placeholder icons:

```bash
python generate_icons.py
```

### 4. Run the Application

**Using pip (traditional):**
```bash
start.bat
```

**Using uv (faster):**
```bash
start-uv.bat
```

Or directly:

```bash
.venv\Scripts\python script\main.py
```

## Build EXE

### Using build.bat

```bash
build.bat
```

The output will be: `dist\pyqt-exe-template.exe`

### Manual Build

```bash
.venv\Scripts\pip install pyinstaller
.venv\Scripts\python -m PyInstaller pyqt-exe-template.spec
```

## Configuration

Configuration is stored in `config/setting.yaml`:

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

## HTTP Client Example

The built-in HTTP Client allows you to test API requests:

1. Navigate to **HTTP Client** page
2. Enter URL (default: `https://httpbin.org/get`)
3. Select method (GET, POST, PUT, DELETE)
4. Add headers (JSON format)
5. Add body (JSON format, for POST/PUT)
6. Click **Send Request**

Response will show:
- Status code
- Response time
- JSON-formatted response body

## Development Guide

### Adding New Pages

1. Create a new page class in `gui.py`:
```python
class NewPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Add your UI components
        pass
```

2. Add navigation button and connect signals in `MainWindow`

### Customizing Styles

Edit `resources/styles/modern.qss` to customize:
- Colors
- Fonts
- Borders
- Button styles
- Input fields

### Adding New Configuration

1. Add default value in `config_manager.py` `_get_defaults()`
2. Update `config/setting.yaml`

## Packaging Notes

### PyInstaller Resource Path

When packaged, resources are extracted to a temporary directory (`sys._MEIPASS`). The `paths.py` module handles this automatically:

```python
from script.paths import resource_path
icon_path = resource_path('icons/my_icon.png')
```

### Included Files

- `resources/` - All UI resources
- `config/` - Configuration files
- `app.ico` - Application icon

### Excluded Modules

To reduce EXE size, the following are excluded:
- tkinter
- matplotlib
- numpy
- pandas
- scipy

## FAQ

### Q: Why PyQt6 instead of pywebview?

PyQt6 provides:
- Native desktop performance
- Better integration with Windows
- No web browser dependencies
- More control over UI components

### Q: How to change the application icon?

Replace `app.ico` with your own icon file (recommended: 256x256 multi-resolution ICO).

### Q: How to add new dependencies?

1. Add to `requirements.txt`
2. Add to `hiddenimports` in `pyqt-exe-template.spec`
3. Run `setup.bat` to update environment

## Roadmap

- [ ] Multi-language support (i18n)
- [ ] Plugin system
- [ ] More HTTP features (authentication, file upload)
- [ ] Dark/Light theme toggle
- [ ] Export/Import configuration

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

## Repository

**GitHub**: [https://github.com/SoulQAQ/pyqt-exe-template](https://github.com/SoulQAQ/pyqt-exe-template)

---

Made with ❤️ using PyQt6
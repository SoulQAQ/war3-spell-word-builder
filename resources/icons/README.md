# Icons Directory

This directory is used to store icon resources for the application.

## Usage

Place your icon files (`.ico`, `.png`, `.svg`) here and reference them in your code using:

```python
from script.paths import resource_path

icon_path = resource_path('icons/your_icon.png')
```

## Recommended Formats

- **Application Icon**: `.ico` format (multi-resolution)
- **UI Icons**: `.png` or `.svg` format
- **Recommended Size**: 16x16, 24x24, 32x32, 48x48, 64x64, 128x128, 256x256

# Images Directory

This directory is used to store image resources for the application.

## Usage

Place your image files (`.png`, `.jpg`, `.svg`) here and reference them in your code using:

```python
from script.paths import resource_path

image_path = resource_path('images/your_image.png')
```

## Supported Formats

- PNG (recommended for UI elements)
- JPEG (for photos)
- SVG (for scalable icons)
- GIF (for animations)

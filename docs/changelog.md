# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-XX

### ✨ Added
- Initial release of Image Transformer Pro
- Filters & Effects:
  - Brightness, Contrast, Saturation, Temperature adjustment
  - Artistic filters: Sepia, Emboss, Edge Detection, Vintage, Oil Painting
  - Basic filters: Blur, Sharpen
  - Special effects: Grayscale, Invert, Pixelate, Motion Blur
- Transform & Crop:
  - Resize/Upscale images
  - Crop with aspect ratios: 1:1, 16:9, 4:3, 9:16, 3:4
  - Rotate: 90°, 180°, 270°
  - Mirror: Horizontal, Vertical, Both
- Borders & Frames:
  - Custom border with color and width
  - Rounded corners
  - Drop shadow effect
- Watermark & Copyright:
  - Text watermark with 17+ fonts
  - Image watermark (logo)
  - Auto timestamp with timezone support
  - Shadow and outline effects for text
- Format Conversion:
  - Support JPG, PNG, WEBP
  - PDF to JPG converter
  - Quality adjustment
- Preview:
  - Live preview with zoom/pan
  - Fit to window
  - Verify before save
- Image Info Extraction:
  - File name, size, dimensions
  - Format, color mode
  - File size in KB/MB
  - EXIF data detection
- Modern dark/light theme UI
- Vietnamese and English interface

### 🔧 Technical
- Built with Python 3.12
- GUI: CustomTkinter
- Image processing: Pillow, OpenCV, NumPy, SciPy
- PDF processing: PyMuPDF

### 📦 Distribution
- Windows installer (.exe)
- Portable version (.zip)
- Source code available on GitHub

---

## Version History

- **1.0.0** - Initial Release (2025-01-XX)

---

## How to Update

### From Installer:
1. Download the new installer
2. Run it - it will automatically uninstall the old version
3. Complete the installation

### From Source:
```bash
git pull origin main
pip install -r requirements.txt --upgrade
python app_gui.py
```

---

## Support

If you encounter any issues or have suggestions:
- 📧 Email: truyenthonga@gmail.com
- 🐛 GitHub Issues: https://github.com/Tachibana11111/ImageTransformerPro/issues

---

**Legend:**
- ✨ Added - New features
- 🔧 Changed - Changes in existing functionality
- 🐛 Fixed - Bug fixes
- 🗑️ Removed - Removed features
- 🔒 Security - Security fixes
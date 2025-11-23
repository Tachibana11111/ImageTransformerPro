# 👨‍💻 Image Transformer Pro - Developer Guide

**Version 1.0.0** | Last Updated: January 2025

Complete guide for developers who want to contribute, modify, or understand the codebase.

---

## 📋 Table of Contents

- [Development Setup](#-development-setup)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Core Components](#-core-components)
- [Adding Features](#-adding-features)
- [Building & Distribution](#-building--distribution)
- [Testing](#-testing)
- [Contributing Guidelines](#-contributing-guidelines)
- [Code Style](#-code-style)
- [API Reference](#-api-reference)

---

## 🛠️ Development Setup

### Prerequisites

- **Python 3.12** or higher
- **Git** for version control
- **Visual Studio Code** (recommended) or any IDE
- **Windows 10/11** (for full testing)

### Clone Repository

```bash
git clone https://github.com/Tachibana11111/ImageTransformerPro.git
cd ImageTransformerPro
```

### Create Virtual Environment

```bash
# Create venv
python -m venv venv312

# Activate (Windows)
.\venv312\Scripts\activate

# Activate (Linux/Mac)
source venv312/bin/activate
```

### Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Install development tools (optional)
pip install black flake8 mypy pytest
```

### Verify Installation

```bash
# Run the application
python app_gui.py

# Should open GUI window without errors
```

---

## 📁 Project Structure

```
ImageTransformer/
│
├── src/                          # Source code package
│   ├── __init__.py               # Package initializer
│   └── transformer.py            # Core image processing functions
│
├── assets/                       # Assets and resources
│   ├── icon.ico                  # Application icon
│   └── screenshots/              # Screenshots for README
│
├── docs/                         # Documentation
│   ├── user_guide.md
│   ├── developer_guide.md        # This file
│   └── changelog.md
│
├── installer/                    # Installer files
│   ├── ImageTransformer.iss      # Inno Setup script
│   ├── license.txt
│   ├── readme_before.txt
│   └── readme_after.txt
│
├── .github/                      # GitHub configs
│   ├── workflows/
│   │   └── build.yml             # CI/CD pipeline
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── FUNDING.yml
│
├── app_gui.py                    # Main GUI application
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
├── README.md                     # Project README
├── LICENSE                       # MIT License
└── CHANGELOG.md                  # Version history
```

---

## 🏗️ Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────┐
│                  app_gui.py                         │
│            (GUI Layer - CustomTkinter)              │
│                                                      │
│  - User input handling                              │
│  - UI components (sliders, buttons, etc.)           │
│  - Preview window management                        │
│  - File I/O dialogs                                 │
└──────────────────┬──────────────────────────────────┘
                   │
                   │ calls functions
                   ↓
┌─────────────────────────────────────────────────────┐
│            src/transformer.py                       │
│         (Processing Layer - PIL/OpenCV)             │
│                                                      │
│  - Image loading/saving                             │
│  - Filter algorithms                                │
│  - Transform operations                             │
│  - Watermark generation                             │
│  - PDF processing                                   │
└─────────────────────────────────────────────────────┘
```

### Design Pattern: MVC-like

- **Model:** `src/transformer.py` - Pure functions, no UI
- **View:** `app_gui.py` (UI components) - CustomTkinter widgets
- **Controller:** `app_gui.py` (event handlers) - Button clicks, slider changes

---

## 🔧 Core Components

### 1. app_gui.py

Main GUI application using CustomTkinter.

**Key Classes:**

```python
class ImageTransformerApp(ctk.CTk):
    """Main application window"""
    
    def __init__(self):
        # Initialize UI
        
    def setup_filters_tab(self):
        # Create filters & effects tab
        
    def setup_watermark_tab(self):
        # Create watermark tab
        
    def gather_all_args(self):
        # Collect all user inputs
        
    def run_preview(self):
        # Show preview window
        
    def run_save(self):
        # Save processed image
```

**Important Methods:**

- `create_io_section()` - Input/output file selection
- `create_action_buttons()` - Preview & Save buttons
- `show_preview_window()` - Display preview with zoom/pan
- `gather_all_args()` - Convert UI state to processing args

### 2. src/transformer.py

Core image processing functions.

**Main Functions:**

```python
# File I/O
def open_image(input_path: str) -> Image.Image | None
def save_image(img: Image.Image, output_path: str, quality: int) -> bool

# Filters
def apply_sepia(img: Image.Image) -> Image.Image
def apply_emboss(img: Image.Image) -> Image.Image
def apply_vintage(img: Image.Image) -> Image.Image
def apply_oil_painting(img: Image.Image, radius: int) -> Image.Image

# Adjustments
def adjust_saturation(img: Image.Image, factor: float) -> Image.Image
def adjust_temperature(img: Image.Image, factor: float) -> Image.Image

# Transforms
def crop_to_aspect_ratio(img: Image.Image, ratio: str) -> Image.Image
def mirror_image(img: Image.Image, direction: str) -> Image.Image

# Watermarks
def create_text_watermark(img: Image.Image, text: str, ...) -> Image.Image
def create_timestamp_watermark(img: Image.Image, ...) -> Image.Image

# Processing Pipeline
def apply_transformations(img: Image.Image, args) -> Image.Image
def get_processed_image(args) -> Image.Image | None

# PDF
def process_pdf_to_jpg(input_path: str, output_folder: str, dpi: int) -> bool

# Info
def get_image_info(img_path: str) -> dict
```

---

## ➕ Adding Features

### Example: Add New Filter

**Step 1: Add function in transformer.py**

```python
def apply_grainy_film(img: Image.Image, intensity: float = 0.5) -> Image.Image:
    """Add film grain effect"""
    import numpy as np
    
    img_array = np.array(img)
    noise = np.random.normal(0, 25 * intensity, img_array.shape)
    grainy = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    
    return Image.fromarray(grainy)
```

**Step 2: Add UI control in app_gui.py**

In `setup_filters_tab()`:

```python
# Add checkbox
self.var_grainy = ctk.BooleanVar(value=False)
self.check_grainy = ctk.CTkCheckBox(
    frame_artistic, 
    text="Film Grain", 
    variable=self.var_grainy
)
self.check_grainy.grid(row=7, column=0, padx=10, pady=5, sticky="w")

# Add intensity slider
ctk.CTkLabel(frame_artistic, text="Intensity:").grid(row=7, column=1)
self.slider_grainy_intensity = ctk.CTkSlider(
    frame_artistic, 
    from_=0.1, 
    to=1.0, 
    number_of_steps=90
)
self.slider_grainy_intensity.set(0.5)
self.slider_grainy_intensity.grid(row=7, column=2)
```

**Step 3: Add to gather_all_args()**

```python
def gather_all_args(self):
    # ... existing code ...
    
    grainy_enabled = self.var_grainy.get() if hasattr(self, 'var_grainy') else False
    grainy_intensity = self.slider_grainy_intensity.get() if hasattr(self, 'slider_grainy_intensity') else 0.5
    
    args = Namespace(
        # ... existing args ...
        grainy_enabled=grainy_enabled,
        grainy_intensity=grainy_intensity,
    )
    return args
```

**Step 4: Apply in transformer.py**

In `apply_transformations()`:

```python
def apply_transformations(img: Image.Image, args) -> Image.Image:
    # ... existing transformations ...
    
    if hasattr(args, 'grainy_enabled') and args.grainy_enabled:
        intensity = getattr(args, 'grainy_intensity', 0.5)
        img = apply_grainy_film(img, intensity)
        print(f"  -> Đã áp dụng Film Grain (intensity: {intensity}).")
    
    return img
```

**Step 5: Test**

```bash
python app_gui.py
# Test the new filter
```

---

## 📦 Building & Distribution

### Build EXE with PyInstaller

```bash
# Install PyInstaller
pip install pyinstaller

# Basic build
pyinstaller --onefile --windowed app_gui.py

# With icon and optimizations
pyinstaller --onefile --windowed \
  --icon=assets/icon.ico \
  --name=ImageTransformer \
  --clean \
  app_gui.py

# Output: dist/ImageTransformer.exe
```

### Create Portable Version

```bash
python create_portable.py
# Output: ImageTransformer_Portable_v1.0.0.zip
```

### Build Installer (Inno Setup)

1. Install Inno Setup: https://jrsoftware.org/isdl.php
2. Open `installer/ImageTransformer.iss`
3. Build → Compile
4. Output: `installer_output/ImageTransformer_Setup_v1.0.0.exe`

### GitHub Actions (Automated)

Push a tag to trigger automatic build:

```bash
git tag v1.0.1
git push origin v1.0.1

# GitHub Actions will:
# 1. Build EXE
# 2. Create portable ZIP
# 3. Calculate checksums
# 4. Create GitHub Release
# 5. Upload binaries
```

---

## 🧪 Testing

### Manual Testing

**Test Checklist:**

- [ ] All tabs load without errors
- [ ] Can select input file
- [ ] Can select output file
- [ ] Preview shows correctly
- [ ] All sliders work
- [ ] All filters apply correctly
- [ ] Watermark appears
- [ ] Timestamp shows correct time
- [ ] Can save image
- [ ] Saved image matches preview
- [ ] PDF to JPG works
- [ ] Image info extraction works

### Unit Testing (Future)

Create `tests/test_transformer.py`:

```python
import pytest
from src.transformer import apply_sepia, open_image

def test_apply_sepia():
    """Test sepia filter"""
    img = open_image("test_images/sample.jpg")
    result = apply_sepia(img)
    
    assert result is not None
    assert result.size == img.size
    # More assertions...

def test_open_nonexistent_file():
    """Test error handling"""
    result = open_image("nonexistent.jpg")
    assert result is None
```

Run tests:

```bash
pytest tests/
```

---

## 🤝 Contributing Guidelines

### Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add: amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Commit Message Convention

```
Type: Brief description

Detailed explanation (optional)

Types:
- Add:    New feature
- Fix:    Bug fix
- Update: Modify existing feature
- Remove: Delete code/feature
- Docs:   Documentation only
- Style:  Code formatting
- Test:   Add/update tests
- Chore:  Maintenance tasks

Examples:
Add: film grain filter
Fix: watermark position bug
Update: improve preview performance
Docs: add developer guide
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How did you test this?

## Screenshots
If applicable

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests (if applicable)
```

---

## 🎨 Code Style

### Python Style Guide

Follow **PEP 8** with these specifics:

**Naming:**
```python
# Classes: PascalCase
class ImageProcessor:
    pass

# Functions/methods: snake_case
def process_image():
    pass

# Constants: UPPER_CASE
MAX_IMAGE_SIZE = 4000

# Private: _leading_underscore
def _internal_helper():
    pass
```

**Formatting:**
```python
# Line length: 88 characters (Black default)
# Indentation: 4 spaces
# Quotes: Double quotes for strings

# Good
def apply_filter(img: Image.Image, intensity: float = 1.0) -> Image.Image:
    """Apply filter to image."""
    return img

# Use type hints
def open_image(path: str) -> Image.Image | None:
    """Open image file."""
    try:
        return Image.open(path)
    except Exception:
        return None
```

**Documentation:**
```python
def complex_function(param1: int, param2: str) -> dict:
    """
    One-line summary.
    
    Detailed explanation of what the function does.
    Can span multiple lines.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Dictionary containing results
    
    Raises:
        ValueError: If params are invalid
    
    Example:
        >>> complex_function(42, "test")
        {'result': 'success'}
    """
    pass
```

### Linting & Formatting

```bash
# Install tools
pip install black flake8 isort

# Format code
black app_gui.py src/

# Check style
flake8 app_gui.py src/

# Sort imports
isort app_gui.py src/
```

---

## 📚 API Reference

### transformer.py Functions

#### Image I/O

```python
def open_image(input_path: str) -> Image.Image | None:
    """
    Open image file.
    
    Args:
        input_path: Path to image file
    
    Returns:
        PIL Image object or None if error
    """

def save_image(img: Image.Image, output_path: str, quality: int = 90) -> bool:
    """
    Save image to file.
    
    Args:
        img: PIL Image object
        output_path: Destination path
        quality: JPEG quality (1-100)
    
    Returns:
        True if successful, False otherwise
    """
```

#### Filters

```python
def apply_sepia(img: Image.Image) -> Image.Image:
    """Apply sepia tone filter."""

def apply_emboss(img: Image.Image) -> Image.Image:
    """Apply emboss effect."""

def apply_vintage(img: Image.Image) -> Image.Image:
    """Apply vintage effect (sepia + reduced contrast/brightness)."""

def apply_oil_painting(img: Image.Image, radius: int = 4) -> Image.Image:
    """Apply oil painting effect using OpenCV."""
```

#### Adjustments

```python
def adjust_saturation(img: Image.Image, factor: float) -> Image.Image:
    """
    Adjust color saturation.
    
    Args:
        img: Input image
        factor: 0.0 = grayscale, 1.0 = original, 2.0 = doubled
    """

def adjust_temperature(img: Image.Image, factor: float) -> Image.Image:
    """
    Adjust color temperature.
    
    Args:
        img: Input image
        factor: < 1.0 = cooler, 1.0 = original, > 1.0 = warmer
    """
```

#### Transforms

```python
def crop_to_aspect_ratio(img: Image.Image, ratio: str) -> Image.Image:
    """
    Crop image to specific aspect ratio.
    
    Args:
        img: Input image
        ratio: "1:1", "16:9", "4:3", "9:16", "3:4"
    
    Returns:
        Cropped image
    """

def mirror_image(img: Image.Image, direction: str) -> Image.Image:
    """
    Mirror/flip image.
    
    Args:
        img: Input image
        direction: "Ngang" (horizontal), "Dọc" (vertical), "Cả hai" (both)
    """
```

#### Watermarks

```python
def create_text_watermark(
    img: Image.Image,
    text: str,
    opacity: float,
    position: str,
    font_size: int,
    font_name: str = "arial.ttf",
    text_color_hex: str = "#FFFFFF",
    rotation: int = 0,
    shadow: bool = False,
    outline: bool = False
) -> Image.Image:
    """
    Add text watermark to image.
    
    Args:
        img: Input image (will be converted to RGBA)
        text: Watermark text
        opacity: 0.0-1.0
        position: 'tl', 'tr', 'bl', 'br', 'c'
        font_size: Font size in pixels
        font_name: Font filename
        text_color_hex: Hex color code
        rotation: Rotation angle (0-360)
        shadow: Add shadow effect
        outline: Add outline effect
    
    Returns:
        Image with watermark (RGBA mode)
    """
```

### CustomTkinter Widgets Used

```python
# Main window
ctk.CTk()

# Frames
ctk.CTkFrame()
ctk.CTkScrollableFrame()

# Inputs
ctk.CTkEntry()
ctk.CTkSlider()
ctk.CTkOptionMenu()
ctk.CTkCheckBox()

# Buttons
ctk.CTkButton()

# Labels
ctk.CTkLabel()

# Tabs
ctk.CTkTabview()
```

---

## 🔍 Debugging

### Enable Debug Mode

Add at top of `app_gui.py`:

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Common Issues

**Import Errors:**
```python
# Check if module installed
import sys
print(sys.path)

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**CustomTkinter Not Showing:**
```python
# Ensure main loop is running
if __name__ == "__main__":
    app = ImageTransformerApp()
    app.mainloop()  # Must be called!
```

**Image Processing Errors:**
```python
# Add try-except in transformer.py
def apply_sepia(img: Image.Image) -> Image.Image:
    try:
        # ... processing code ...
        return result
    except Exception as e:
        print(f"Error in apply_sepia: {e}")
        return img  # Return original on error
```

---

## 📖 Resources

### Documentation

- **Pillow:** https://pillow.readthedocs.io/
- **CustomTkinter:** https://github.com/TomSchimansky/CustomTkinter
- **OpenCV:** https://docs.opencv.org/
- **NumPy:** https://numpy.org/doc/
- **PyMuPDF:** https://pymupdf.readthedocs.io/

### Tutorials

- **Image Processing:** https://realpython.com/image-processing-with-the-python-pillow-library/
- **CustomTkinter:** https://youtu.be/VIDEO_ID
- **PyInstaller:** https://realpython.com/pyinstaller-python/

---

## 📞 Contact

### For Developers

- 💬 **Discussions:** [GitHub Discussions](https://github.com/Tachibana11111/ImageTransformerPro/discussions)
- 📧 **Email:** truyenthonga@gmail.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/Tachibana11111/ImageTransformerPro/issues)

---

<div align="center">

**Happy Coding! 🚀**

[⬆ Back to top](#-image-transformer-pro---developer-guide)

</div>

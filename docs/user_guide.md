# 📖 Image Transformer Pro - User Guide

**Version 1.0.0** | Last Updated: January 2025

Welcome to Image Transformer Pro! This guide will help you get started and make the most of all features.

---

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Interface Overview](#-interface-overview)
- [Features Guide](#-features-guide)
  - [Filters & Effects](#filters--effects)
  - [Transform & Crop](#transform--crop)
  - [Borders & Frames](#borders--frames)
  - [Watermark & Copyright](#watermark--copyright)
  - [Format Conversion](#format-conversion)
  - [Image Info](#image-info)
- [Tips & Tricks](#-tips--tricks)
- [Keyboard Shortcuts](#-keyboard-shortcuts)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)

---

## 💿 Installation

### Method 1: Installer (Recommended)

1. **Download** `ImageTransformerPro_Setup_v1.0.0.exe`
2. **Run** the installer
3. Follow the setup wizard:
   - Choose language 
   - Read and accept license
   - Select installation folder
   - Choose to create desktop shortcut
4. Click **Install**
5. Launch the application

### Method 2: Portable Version

1. **Download** `ImageTransformerPro_Portable_v1.0.0.zip`
2. **Extract** to any folder (USB drive, Desktop, etc.)
3. **Run** `Image Transformer Pro.exe`
4. No installation required!

---

## 🚀 Quick Start

### Basic Workflow

```
1. Select Input Image → 2. Apply Effects → 3. Preview → 4. Save
```

### Step-by-Step:

1. **Open the application**
2. **Navigate to any tab** (e.g., "Filters & Effects")
3. **Click "Browse"** next to "Input file"
4. **Select your image** (JPG, PNG, WEBP)
5. **Adjust settings** (sliders, dropdowns, checkboxes)
6. **Click "PREVIEW"** (blue button) to see result
7. **In preview window:**
   - Zoom: Use slider or mouse wheel
   - Pan: Click and drag
   - Fit: Click "Fit to window"
8. **Click "SAVE IMAGE"** if satisfied
9. **Choose output location** and filename
10. **Done!** 🎉

---

## 🎨 Features Guide

### Filters & Effects

#### 1. Basic Adjustments

**Brightness (0.1 - 2.0)**
- `< 1.0` = Darker
- `= 1.0` = Original
- `> 1.0` = Brighter
- **Tip:** Adjust brightness BEFORE contrast

**Contrast (0.1 - 2.0)**
- `< 1.0` = Less contrast (flatter)
- `= 1.0` = Original
- `> 1.0` = More contrast (sharper)

**Saturation (0.0 - 2.0)**
- `0.0` = Grayscale
- `1.0` = Original
- `2.0` = Very vibrant
- **Tip:** Use 0.8-0.9 for vintage look

**Temperature (0.5 - 1.5)**
- `< 1.0` = Cooler (blue tint)
- `= 1.0` = Original
- `> 1.0` = Warmer (yellow/red tint)

#### 2. Artistic Filters

 **Sepia** - Brownish vintage tone : Old photos, nostalgic feel 
 **Emboss** - 3D raised effect : Artistic designs 
 **Edge Detection** - Outline only : Line art, sketches 
 **Vintage** - Aged photo look : Retro aesthetic 
 **Oil Painting** - Painterly effect : Artistic portraits 

#### 3. Special Effects

**Motion Blur**
- Creates directional blur
- Angle: 0-360° (0° = horizontal)
- Use for: Speed effect, dynamic images

**Grayscale**
- Converts to black and white
- Removes all color

**Invert**
- Reverses colors (negative effect)
- Black ↔ White, Red ↔ Cyan

**Pixelate (2-50)**
- Creates retro pixel art effect
- Higher value = larger blocks
- **Tip:** Use 10-20 for best results

---

### Transform & Crop

#### Resize/Upscale

**Format:** `WIDTHxHEIGHT`

**Examples:**
```
1920x1080  →  Full HD
1280x720   →  HD
800x600    →  Standard
3840x2160  →  4K
```

**Tips:**
- Maintain aspect ratio for best quality
- Use for: Social media sizes, prints, thumbnails

#### Crop Aspect Ratios

**1:1** : Instagram posts, profile pictures 
**16:9** : YouTube thumbnails, presentations 
**4:3** : Traditional photos, displays 
**9:16** : Instagram Stories, TikTok 
**3:4** : Portrait photos 

**How it works:**
- Automatically crops from center
- Keeps maximum area with desired ratio

#### Rotate

**90°** : Quarter turn clockwise 
**180°** : Upside down 
**270°** : Quarter turn counter-clockwise 
**Horizontal** : Mirror left-right 
**Vertical** : Flip top-bottom 

#### Mirror (Symmetry)

- **Horizontal:** Creates left-right reflection
- **Vertical:** Creates top-bottom reflection
- **Both:** Combines both effects

---

### Borders & Frames

#### Border

**Width:** 0-50 pixels
**Color:** Click "Choose color" to select

**Examples:**
```
5px white border   →  Subtle frame
20px black border  →  Bold frame
10px #FFD700       →  Gold border
```

#### Rounded Corners

**Radius:** 0-100 pixels

- `0` = Sharp corners (rectangle)
- `20` = Slightly rounded
- `50` = Very rounded
- `100+` = Circular edges

**Note:** Creates transparent areas (PNG output recommended)

#### Drop Shadow

**Offset:** Distance from image (0-30px)
**Blur:** Shadow softness (0-30)
**Color:** Shadow color (default: black)

**Tips:**
- Offset 10, Blur 10 = Natural shadow
- Large offset + blur = Floating effect
- Gray color = Softer shadow

---

### Watermark & Copyright

#### Text Watermark

**Fonts Available:**
- Arial, Arial Bold
- Times New Roman, Times Bold
- Calibri, Calibri Bold
- Verdana, Verdana Bold
- Georgia, Georgia Bold
- Tahoma, Tahoma Bold
- Trebuchet MS
- Impact
- Consolas, Consolas Bold
- Comic Sans MS

**Settings:**

**Font Size:** 10-150
- Recommend: 30-50 for most images

**Opacity:** 0.1-1.0
- `0.3-0.5` = Subtle (recommended)
- `0.7-0.9` = Visible but not intrusive
- `1.0` = Fully opaque

**Position:**
- **br** = Bottom Right (default)
- **bl** = Bottom Left
- **tr** = Top Right
- **tl** = Top Left
- **c** = Center

**Rotation:** 0-360°
- `0°` = Horizontal
- `45°` = Diagonal
- `90°` = Vertical

**Effects:**
- **Shadow:** Adds depth
- **Outline:** Makes text readable on any background

**Tips:**
```
Light background → Use dark text
Dark background  → Use white text
Mixed background → Use outline + shadow
```

#### Image Watermark (Logo)

**Supported formats:** PNG (with transparency), JPG

**Size:** 5-50% of image width
- Recommend: 10-20%

**Tips:**
- Use PNG with transparent background
- Position in corner (not center)
- Lower opacity (0.5-0.7) for subtlety

#### Timestamp

**Format:** `DD/MM/YYYY (TIMEZONE), HH:MM:SS`

**Example:** `23/01/2025 (ICT), 14:30:45`

**Timezones:**
- **Asia/Ho_Chi_Minh** - Vietnam (ICT)
- **Asia/Bangkok** - Thailand
- **Asia/Tokyo** - Japan
- **UTC** - Universal Time

**Use cases:**
- Proof of time (legal documents)
- Event photos
- Security cameras
- Before/after comparisons

---

### Format Conversion

#### Image Format Conversion

**Input:** JPG, PNG, WEBP
**Output:** JPG, PNG, WEBP

**Quality:** 1-100
- `100` = Best quality, largest file
- `90` = Excellent (recommended)
- `70-80` = Good balance
- `< 50` = Visible compression

**File Size Comparison:**
```
Same image:
PNG:  5.2 MB
JPG:  1.8 MB (quality 90)
WEBP: 1.2 MB (quality 90)
```

**Recommendations:**
- **PNG:** For graphics, text, transparency
- **JPG:** For photos, fast loading
- **WEBP:** For web, smallest size

#### PDF to JPG

**DPI (Dots Per Inch):**
- `72` = Screen quality
- `150` = Standard print
- `300` = High quality print (recommended)
- `600` = Professional printing

**Output:**
- One JPG per page
- Named: `filename_page_1.jpg`, `filename_page_2.jpg`, etc.

---

### Image Info

Extract detailed information about any image:

**Information Provided:**
- Filename
- Dimensions (width × height)
- Aspect ratio
- Format (JPG, PNG, etc.)
- Color mode (RGB, RGBA, Grayscale)
- File size (KB and MB)
- EXIF data presence

**Use cases:**
- Check image size before upload
- Verify format
- Get dimensions for design
- Check if image has metadata

---

## 💡 Tips & Tricks

### For Best Results

1. **Always preview before saving**
   - Zoom in to check details
   - Verify watermark placement

2. **Work in order:**
   ```
   Crop → Brightness/Contrast → Filters → Watermark → Save
   ```

3. **Use high-quality source images**
   - Garbage in = Garbage out
   - Can't add detail that isn't there

4. **Save originals**
   - Keep backup of original images
   - Edits are permanent after save

5. **Experiment with combinations**
   - Multiple filters can be applied
   - Try different opacity levels

### Common Workflows

**Social Media Posting:**
```
1. Crop to 1:1 (Instagram) or 16:9 (YouTube)
2. Increase saturation slightly (1.1-1.2)
3. Add text watermark with your handle
4. Save as JPG, quality 90
```

**Professional Documentation:**
```
1. Ensure good lighting in source
2. Increase contrast slightly (1.1-1.2)
3. Add timestamp
4. Save as PNG for maximum quality
```

**Artistic Photos:**
```
1. Apply Vintage or Sepia filter
2. Reduce saturation (0.8-0.9)
3. Add slight vignette (can be done with borders)
4. Save as JPG
```

**Web Optimization:**
```
1. Resize to web dimensions (1200x800 max)
2. Convert to WEBP
3. Quality 80-85
4. Result: Fast loading, good quality
```

---

## ⌨️ Keyboard Shortcuts

### In Main Window

`Ctrl + O` : Open file 
`Ctrl + S` : Save file 
`Ctrl + P` : Preview 
`F11` : Toggle fullscreen 
`Esc` : Cancel/Close 

### In Preview Window

`Mouse Wheel` ; Zoom in/out 
`Left Click + Drag` : Pan image 
`Ctrl + 0` : Reset zoom (100%) 
`F` : Fit to window 
`Esc` : Close preview 

---

## 🔧 Troubleshooting

### Cannot Open Image

**Problem:** Error message when trying to open file

**Solutions:**
1. Check file format (must be JPG, PNG, or WEBP)
2. Ensure file is not corrupted
3. Try opening in another program first
4. Check file permissions

### Preview Window Shows Black/White Screen

**Problem:** Preview shows blank or incorrect colors

**Solutions:**
1. Close and reopen preview
2. Try different filters
3. Check original image is valid
4. Restart application

### Watermark Not Visible

**Problem:** Added watermark but can't see it

**Solutions:**
1. **Check opacity** - Must be > 0.3 to be visible
2. **Check color** - White on white won't show
3. **Zoom in** - Might be too small
4. Enable shadow or outline effects

### App Runs Slowly

**Problem:** Application is laggy or slow

**Solutions:**
1. Close other programs
2. Process smaller images (< 4000x4000)
3. Reduce preview quality
4. Check available RAM

### Font Not Working

**Problem:** Selected font doesn't appear correctly

**Solutions:**
1. Use default fonts (Arial, Times)
2. Install missing fonts to `C:\Windows\Fonts\`
3. Restart application after installing fonts

### Cannot Save File

**Problem:** Error when trying to save

**Solutions:**
1. Check disk space
2. Ensure output folder exists
3. Check write permissions
4. Don't use special characters in filename
5. Try saving to Desktop first

---

## ❓ FAQ

### General

**Q: Is it free?**
A: Yes, 100% free and open source under MIT License.

**Q: Does it work offline?**
A: Yes, no internet connection needed.

**Q: Can I use it commercially?**
A: Yes, MIT License allows commercial use.

**Q: Which formats are supported?**
A: Input: JPG, PNG, WEBP, PDF
   Output: JPG, PNG, WEBP

**Q: Can I batch process multiple images?**
A: Not in v1.0.0, but planned for v1.1.0 (Q2 2025)

### Features

**Q: Can I undo changes?**
A: No undo in v1.0.0. Always preview before saving!

**Q: Maximum image size?**
A: No hard limit, but recommend < 4000x4000 for performance.

**Q: Does it compress images?**
A: Only when saving JPG/WEBP with quality < 100.

**Q: Can I add multiple watermarks?**
A: Yes! Text + Image + Timestamp all at once.

**Q: Does it remove EXIF data?**
A: Yes, processed images have no EXIF metadata.

### Technical

**Q: What's the quality slider do?**
A: Controls JPG/WEBP compression (1=smallest, 100=best quality)

**Q: Why is my output file large?**
A: Use quality 80-90 instead of 100, or convert to WEBP

**Q: Can I edit the source code?**
A: Yes! It's open source. See [Developer Guide](developer_guide.md)

**Q: How do I update?**
A: Download new installer, it will replace old version.

---

## 📞 Need More Help?

### Contact Support

- 📧 **Email:** truyenthonga@gmail.com
- 🐛 **Bug Reports:** [GitHub Issues](https://github.com/Tachibana11111/ImageTransformerPro/issues)
- 💬 **Questions:** [GitHub Discussions](https://github.com/Tachibana11111/ImageTransformerPro/discussions)

### Documentation

- 📖 **User Guide:** You're reading it!
- 👨‍💻 **Developer Guide:** [developer_guide.md](docs/developer_guide.md)
- 📝 **Changelog:** [CHANGELOG.md](docs/changelog.md)

---

<div align="center">

**Made with ❤️ by [Tachibana11111](https://github.com/Tachibana11111)**

[⬆ Back to top](#-image-transformer-pro---user-guide)

</div>
import os
import numpy as np
from PIL import Image, ImageChops, ImageEnhance, ImageFilter, ImageDraw, ImageFont, ImageOps
import fitz
from typing import List, Tuple
from datetime import datetime
import pytz
import cv2
from scipy import ndimage

def open_image(input_path: str) -> Image.Image | None:
    try:
        img = Image.open(input_path).convert('RGB')
        return img
    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file tại đường dẫn: {input_path}")
        return None
    except Exception as e:
        print(f"LỖI khi mở file ảnh {input_path}: {e}")
        return None

def save_image(img: Image.Image, output_path: str, quality: int = 90) -> bool:
    try:
        if img.mode == 'RGBA':
            print("  -> Chuyển đổi ảnh RGBA sang RGB để lưu...")
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3]) 
            img = background

        ext = os.path.splitext(output_path)[1].lower()
        
        if ext in ['.jpg', '.jpeg']:
            img.save(output_path, 'JPEG', quality=quality)
        elif ext == '.webp':
            img.save(output_path, 'WEBP', quality=quality)
        else:
            img.save(output_path)
            
        print(f"Đã lưu thành công tại: {output_path}")
        return True
    except Exception as e:
        print(f"LỖI khi lưu file ảnh: {e}")
        return False

def process_pdf_to_jpg(input_path: str, output_folder: str, dpi: int = 300) -> bool:
    try:
        pdf_document = fitz.open(input_path)
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            
        zoom = dpi / 72
        matrix = fitz.Matrix(zoom, zoom)

        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap(matrix=matrix)
            
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            output_file = os.path.join(output_folder, f"{base_name}_page_{page_num+1}.jpg")
            
            pix.save(output_file)
            print(f"  -> Đã tạo: {output_file}")
            
        print(f"Đã chuyển đổi PDF ({len(pdf_document)} trang) sang JPG thành công.")
        return True
    except Exception as e:
        print(f"LỖI khi xử lý PDF: {e}")
        return False

def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return (255, 255, 255)

def apply_sepia(img: Image.Image) -> Image.Image:
    img_array = np.array(img)
    sepia_filter = np.array([[0.393, 0.769, 0.189],
                             [0.349, 0.686, 0.168],
                             [0.272, 0.534, 0.131]])
    sepia_img = img_array @ sepia_filter.T
    sepia_img = np.clip(sepia_img, 0, 255).astype(np.uint8)
    return Image.fromarray(sepia_img)

def apply_emboss(img: Image.Image) -> Image.Image:
    return img.filter(ImageFilter.EMBOSS)

def apply_edge_detection(img: Image.Image) -> Image.Image:
    return img.filter(ImageFilter.FIND_EDGES)

def apply_vintage(img: Image.Image) -> Image.Image:
    img = apply_sepia(img)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(0.8)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.9)
    return img

def apply_oil_painting(img: Image.Image, radius: int = 4) -> Image.Image:
    try:
        img_array = np.array(img)
        img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        oil = cv2.xphoto.oilPainting(img_cv, radius, 1)
        oil_rgb = cv2.cvtColor(oil, cv2.COLOR_BGR2RGB)
        return Image.fromarray(oil_rgb)
    except:
        return img.filter(ImageFilter.MedianFilter(size=3))

def adjust_saturation(img: Image.Image, factor: float) -> Image.Image:
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)

def adjust_temperature(img: Image.Image, factor: float) -> Image.Image:
    img_array = np.array(img).astype(np.float32)
    if factor > 1.0:  
        img_array[:, :, 0] = np.clip(img_array[:, :, 0] * factor, 0, 255)
        img_array[:, :, 1] = np.clip(img_array[:, :, 1] * (1 + (factor - 1) * 0.5), 0, 255)
    else: 
        img_array[:, :, 2] = np.clip(img_array[:, :, 2] * (2 - factor), 0, 255)
    return Image.fromarray(img_array.astype(np.uint8))

def apply_motion_blur(img: Image.Image, size: int = 15, angle: int = 0) -> Image.Image:
    img_array = np.array(img)
    
    kernel = np.zeros((size, size))
    kernel[int((size - 1) / 2), :] = np.ones(size)
    kernel = kernel / size
    kernel = ndimage.rotate(kernel, angle, reshape=False)
    blurred = np.zeros_like(img_array)
    for i in range(3):
        blurred[:, :, i] = ndimage.convolve(img_array[:, :, i], kernel)
    
    return Image.fromarray(blurred.astype(np.uint8))

def add_border(img: Image.Image, border_width: int, border_color: str) -> Image.Image:
    color = hex_to_rgb(border_color)
    return ImageOps.expand(img, border=border_width, fill=color)

def add_rounded_corners(img: Image.Image, radius: int) -> Image.Image:
    img = img.convert("RGBA")
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    
    result = Image.new('RGBA', img.size, (255, 255, 255, 0))
    result.paste(img, (0, 0), mask)
    return result

def add_shadow(img: Image.Image, offset: int = 10, blur: int = 10, color: str = "#000000") -> Image.Image:
    img = img.convert("RGBA")
    
    shadow_color = hex_to_rgb(color) + (128,) 
    shadow = Image.new('RGBA', (img.width + offset * 2, img.height + offset * 2), (255, 255, 255, 0))
    shadow_img = Image.new('RGBA', img.size, shadow_color)
    shadow.paste(shadow_img, (offset, offset))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    shadow.paste(img, (0, 0), img)
    return shadow

def crop_to_aspect_ratio(img: Image.Image, ratio: str) -> Image.Image:
    ratios = {
        "1:1": 1.0,
        "16:9": 16/9,
        "4:3": 4/3,
        "9:16": 9/16,
        "3:4": 3/4
    }
    
    if ratio not in ratios:
        return img
    
    target_ratio = ratios[ratio]
    width, height = img.size
    current_ratio = width / height
    
    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))
    
    return img

def mirror_image(img: Image.Image, direction: str) -> Image.Image:
    if direction == "Ngang":
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "Dọc":
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    elif direction == "Cả hai":
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    return img

def create_text_watermark(img: Image.Image, text: str, opacity: float, position: str, 
                         font_size: int, font_name: str = "arial.ttf", 
                         text_color_hex: str = "#FFFFFF", rotation: int = 0,
                         shadow: bool = False, outline: bool = False) -> Image.Image:
    img_rgba = img.convert("RGBA") if img.mode != 'RGBA' else img.copy() 
    text_layer = Image.new('RGBA', img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_layer)
    
    try:
        font = ImageFont.truetype(font_name, size=font_size)
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", size=font_size)
        except IOError:
            font = ImageFont.load_default()
    
    rgb_color = hex_to_rgb(text_color_hex)
    text_color = (*rgb_color, int(opacity * 255))
    
    try:
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_width = int(draw.textlength(text, font=font))
        text_height = font_size
    
    img_width, img_height = img_rgba.size
    padding = 10
    
    if position == 'tl':
        x, y = padding, padding
    elif position == 'tr':
        x, y = img_width - text_width - padding, padding
    elif position == 'bl':
        x, y = padding, img_height - text_height - padding
    elif position == 'br':
        x, y = img_width - text_width - padding, img_height - text_height - padding
    elif position == 'c':
        x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
    else:
        x, y = padding, padding
    
    if shadow:
        shadow_color = (0, 0, 0, int(opacity * 128))
        draw.text((x + 2, y + 2), text, font=font, fill=shadow_color)
    
    if outline:
        outline_color = (0, 0, 0, int(opacity * 255))
        for adj_x in [-1, 0, 1]:
            for adj_y in [-1, 0, 1]:
                if adj_x != 0 or adj_y != 0:
                    draw.text((x + adj_x, y + adj_y), text, font=font, fill=outline_color)
    draw.text((x, y), text, font=font, fill=text_color)
    
    if rotation != 0:
        text_layer = text_layer.rotate(rotation, expand=False, center=(x + text_width // 2, y + text_height // 2))
    img_rgba = Image.alpha_composite(img_rgba, text_layer)
    return img_rgba

def create_timestamp_watermark(img: Image.Image, opacity: float, position: str, 
                              font_size: int, font_name: str = "arial.ttf", 
                              text_color_hex: str = "#FFFFFF",
                              timezone: str = "Asia/Ho_Chi_Minh") -> Image.Image:
    img_rgba = img.convert("RGBA") if img.mode != 'RGBA' else img.copy() 
    draw = ImageDraw.Draw(img_rgba)
    
    try:
        font = ImageFont.truetype(font_name, size=font_size)
    except IOError:
        try:
            font = ImageFont.truetype("arial.ttf", size=font_size)
        except IOError:
            font = ImageFont.load_default()
    
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)
        tz_abbr = now.strftime('%Z')
    except:
        now = datetime.now()
        tz_abbr = "LOCAL"
    
    date_str = now.strftime('%d/%m/%Y')
    time_str = now.strftime('%H:%M:%S')
    timestamp_text = f"{date_str} ({tz_abbr}), {time_str}"
    
    rgb_color = hex_to_rgb(text_color_hex)
    text_color = (*rgb_color, int(opacity * 255))
    img_width, img_height = img_rgba.size
    
    try:
        text_bbox = draw.textbbox((0, 0), timestamp_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        text_width = int(draw.textlength(timestamp_text, font=font))
        text_height = font_size
    
    padding = 10
    
    if position == 'tl':
        x, y = padding, padding
    elif position == 'tr':
        x, y = img_width - text_width - padding, padding
    elif position == 'bl':
        x, y = padding, img_height - text_height - padding
    elif position == 'br':
        x, y = img_width - text_width - padding, img_height - text_height - padding
    elif position == 'c':
        x, y = (img_width - text_width) // 2, (img_height - text_height) // 2
    else:
        x, y = padding, padding
    
    draw.text((x, y), timestamp_text, font=font, fill=text_color)
    return img_rgba

def apply_transformations(img: Image.Image, args) -> Image.Image:
    if hasattr(args, 'crop_ratio') and args.crop_ratio and args.crop_ratio != "None":
        img = crop_to_aspect_ratio(img, args.crop_ratio)
        print(f"  -> Đã crop ảnh theo tỷ lệ {args.crop_ratio}.")
    
    if args.resize:
        try:
            width, height = map(int, args.resize.lower().split('x'))
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            print(f"  -> Đã resize/upscale ảnh thành {width}x{height}.")
        except Exception as e:
            print(f"LỖI: Định dạng resize không hợp lệ. {e}")
    
    if hasattr(args, 'mirror') and args.mirror and args.mirror != "None":
        img = mirror_image(img, args.mirror)
        print(f"  -> Đã mirror ảnh ({args.mirror}).")
    
    if args.brightness is not None and args.brightness != 1.0:
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(args.brightness)
        print(f"  -> Đã điều chỉnh độ sáng (Factor: {args.brightness}).")

    if args.contrast is not None and args.contrast != 1.0:
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(args.contrast)
        print(f"  -> Đã điều chỉnh độ tương phản (Factor: {args.contrast}).")
    
    if hasattr(args, 'saturation') and args.saturation is not None and args.saturation != 1.0:
        img = adjust_saturation(img, args.saturation)
        print(f"  -> Đã điều chỉnh độ bão hòa (Factor: {args.saturation}).")
    
    if hasattr(args, 'temperature') and args.temperature is not None and args.temperature != 1.0:
        img = adjust_temperature(img, args.temperature)
        print(f"  -> Đã điều chỉnh nhiệt độ màu (Factor: {args.temperature}).")

    if args.filter == 'Làm mờ':
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        print("  -> Đã áp dụng Bộ lọc Làm mờ (Gaussian Blur).")
    elif args.filter == 'Làm nét':
        img = img.filter(ImageFilter.SHARPEN)
        print("  -> Đã áp dụng Bộ lọc Làm nét (Sharpen).")
    
    if hasattr(args, 'artistic_filter') and args.artistic_filter and args.artistic_filter != "Không":
        if args.artistic_filter == 'Nâu đỏ':
            img = apply_sepia(img)
            print("  -> Đã áp dụng bộ lọc Sepia.")
        elif args.artistic_filter == 'Dập nổi':
            img = apply_emboss(img)
            print("  -> Đã áp dụng hiệu ứng Emboss.")
        elif args.artistic_filter == 'edge_detection':
            img = apply_edge_detection(img)
            print("  -> Đã áp dụng Edge Detection.")
        elif args.artistic_filter == 'Cổ điển':
            img = apply_vintage(img)
            print("  -> Đã áp dụng hiệu ứng Vintage.")
        elif args.artistic_filter == 'Sơn dầu':
            img = apply_oil_painting(img)
            print("  -> Đã áp dụng hiệu ứng Oil Painting.")
    
    if hasattr(args, 'motion_blur') and args.motion_blur:
        angle = getattr(args, 'motion_blur_angle', 0)
        img = apply_motion_blur(img, size=15, angle=angle)
        print(f"  -> Đã áp dụng Motion Blur (góc: {angle}°).")

    if args.grayscale:
        img = img.convert('L').convert('RGB')
        print("  -> Đã chuyển ảnh sang đen trắng.")

    if hasattr(args, 'invert') and args.invert:
        img = ImageChops.invert(img)
        print("  -> Đã áp dụng Đảo màu (Invert).")

    if args.pixelate_size and args.pixelate_size > 0:
        try:
            size = img.size
            small_size = (size[0] // args.pixelate_size, size[1] // args.pixelate_size)
            img = img.resize(small_size, Image.Resampling.NEAREST)
            img = img.resize(size, Image.Resampling.NEAREST)
            print(f"  -> Đã áp dụng pixel hóa (block size: {args.pixelate_size}).")
        except Exception as e:
            print(f"CẢNH BÁO: Lỗi pixel hóa: {e}")

    if args.rotate:
        if args.rotate == '90':
            img = img.transpose(Image.ROTATE_90)
            print("  -> Đã xoay ảnh 90 độ.")
        elif args.rotate == '180':
            img = img.transpose(Image.ROTATE_180)
            print("  -> Đã xoay ảnh 180 độ.")
        elif args.rotate == '270':
            img = img.transpose(Image.ROTATE_270)
            print("  -> Đã xoay ảnh 270 độ.")
        elif args.rotate == 'Xoay ngang':
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
            print("  -> Đã lật ảnh theo chiều ngang.")
        elif args.rotate == 'Xoay dọc':
            img = img.transpose(Image.FLIP_TOP_BOTTOM)
            print("  -> Đã lật ảnh theo chiều dọc.")
    
    if hasattr(args, 'border_width') and args.border_width > 0:
        border_color = getattr(args, 'border_color', '#000000')
        img = add_border(img, args.border_width, border_color)
        print(f"  -> Đã thêm viền (width: {args.border_width}, color: {border_color}).")
    
    if hasattr(args, 'rounded_radius') and args.rounded_radius > 0:
        img = add_rounded_corners(img, args.rounded_radius)
        print(f"  -> Đã bo góc (radius: {args.rounded_radius}).")
    
    if hasattr(args, 'shadow_enabled') and args.shadow_enabled:
        offset = getattr(args, 'shadow_offset', 10)
        blur = getattr(args, 'shadow_blur', 10)
        color = getattr(args, 'shadow_color', '#000000')
        img = add_shadow(img, offset, blur, color)
        print(f"  -> Đã thêm đổ bóng.")
    
    if args.watermark_text and args.watermark_text != "":
        font_name = getattr(args, 'watermark_font', 'arial.ttf')
        text_color = getattr(args, 'watermark_text_color', '#FFFFFF')
        rotation = getattr(args, 'watermark_rotation', 0)
        shadow = getattr(args, 'watermark_shadow', False)
        outline = getattr(args, 'watermark_outline', False)
        
        img = create_text_watermark(
            img, 
            args.watermark_text, 
            args.watermark_opacity, 
            args.watermark_position, 
            args.watermark_font_size,
            font_name,
            text_color_hex=text_color,
            rotation=rotation,
            shadow=shadow,
            outline=outline
        )
        print(f"  -> Đã thêm chữ Watermark: '{args.watermark_text}' tại vị trí {args.watermark_position.upper()}.")
    
    if args.watermark_image_path and os.path.exists(args.watermark_image_path):
        try:
            watermark_img = Image.open(args.watermark_image_path).convert("RGBA")
            
            if img.mode != 'RGBA':
                 img = img.convert("RGBA")

            img_width, img_height = img.size
            wm_width, wm_height = watermark_img.size
            
            if args.watermark_image_size and args.watermark_image_size > 0:
                new_width = int(img_width * (args.watermark_image_size / 100))
                
                if wm_width > 0:
                    w_percent = (new_width / float(wm_width))
                    new_height = int((float(wm_height) * float(w_percent)))
                    watermark_img = watermark_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    wm_width, wm_height = watermark_img.size
                    print(f"  -> Đổi kích cỡ ảnh Watermark thành {wm_width}x{wm_height} ({args.watermark_image_size}% chiều rộng).")
            
            if args.watermark_opacity < 1.0:
                 alpha = watermark_img.getchannel('A')
                 alpha = ImageEnhance.Brightness(alpha).enhance(args.watermark_opacity)
                 watermark_img.putalpha(alpha)

            position = args.watermark_position
            padding = 10
            x, y = 0, 0
            
            if position == 'tl':
                x = padding
                y = padding
            elif position == 'tr':
                x = img_width - wm_width - padding
                y = padding
            elif position == 'bl':
                x = padding
                y = img_height - wm_height - padding
            elif position == 'br':
                x = img_width - wm_width - padding
                y = img_height - wm_height - padding
            elif position == 'c':
                x = (img_width - wm_width) // 2
                y = (img_height - wm_height) // 2

            img.paste(watermark_img, (x, y), mask=watermark_img) 
            print(f"  -> Đã thêm ảnh Watermark từ: {args.watermark_image_path} tại vị trí {position.upper()}.")
            
        except Exception as e:
            print(f"CẢNH BÁO: Không thể thêm ảnh Watermark: {e}")
    
    if hasattr(args, 'timestamp_enabled') and args.timestamp_enabled:
        font_name = getattr(args, 'timestamp_font', 'arial.ttf')
        text_color = getattr(args, 'timestamp_text_color', '#FFFFFF')
        font_size = getattr(args, 'timestamp_font_size', 30)
        opacity = getattr(args, 'timestamp_opacity', 0.7)
        position = getattr(args, 'timestamp_position', 'br')
        timezone = getattr(args, 'timestamp_timezone', 'Asia/Ho_Chi_Minh')
        
        img = create_timestamp_watermark(
            img,
            opacity,
            position,
            font_size,
            font_name,
            text_color_hex=text_color,
            timezone=timezone
        )
        print(f"  -> Đã thêm Timestamp tại vị trí {position.upper()}.")
    
    return img

def get_processed_image(args) -> Image.Image | None:
    if args.command == 'pdf2jpg':
        print("LỖI: Không thể xem trước file PDF.")
        return None
    
    img = open_image(args.input_path)
    if not img:
        return None
    
    img = apply_transformations(img, args)
    
    return img

def transform_image(args) -> bool:
    if args.command == 'pdf2jpg':
        return process_pdf_to_jpg(args.input_path, args.output_folder, args.dpi)

    try:
        img = open_image(args.input_path)
        if not img:
            return False
        img = apply_transformations(img, args)
        return save_image(img, args.output_path, quality=args.quality)
        
    except Exception as e:
        print(f"LỖI không thể xử lý ảnh: {e}")
        return False

def get_image_info(img_path: str) -> dict:
    try:
        img = Image.open(img_path)
        file_size = os.path.getsize(img_path) / 1024  
        
        info = {
            'filename': os.path.basename(img_path),
            'format': img.format,
            'mode': img.mode,
            'size': img.size,
            'width': img.width,
            'height': img.height,
            'file_size_kb': round(file_size, 2),
            'file_size_mb': round(file_size / 1024, 2),
            'aspect_ratio': f"{img.width}:{img.height}",
        }
        
        if hasattr(img, '_getexif') and img._getexif():
            info['has_exif'] = True
        else:
            info['has_exif'] = False
        
        return info
    except Exception as e:
        return {'error': str(e)}



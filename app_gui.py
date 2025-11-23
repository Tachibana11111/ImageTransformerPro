import customtkinter as ctk
from tkinter import filedialog, messagebox, colorchooser
import os
from src import transformer
from argparse import Namespace 
from PIL import ImageTk, Image
import json

class ImageTransformerApp(ctk.CTk): 
    def __init__(self):
        super().__init__()
        
        self.current_theme = "Dark"
        self.title("Image Transformer Pro")
        self.geometry("1270x720")
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")
        
        self.input_file = ctk.StringVar()
        self.output_file = ctk.StringVar()
        self.selected_text_color = "#FFFFFF"
        self.selected_timestamp_color = "#FFFFFF"
        self.selected_border_color = "#000000"
        self.selected_shadow_color = "#000000"
        self.preview_image: Image.Image | None = None
        self.preview_window: ctk.CTkToplevel | None = None
        self.create_settings_menu()
        self.tab_view = ctk.CTkTabview(self, width=880)
        self.tab_view.pack(padx=10, pady=10, fill="both", expand=True)
        self.tab_view.add("Bộ lọc & Hiệu ứng")
        self.tab_view.add("Biến đổi & Cắt xén")
        self.tab_view.add("Viền & Khung")
        self.tab_view.add("Đóng dấu bản quyền")
        self.tab_view.add("Định dạng & PDF")
        self.tab_view.add("Trích xuất thông tin hình ảnh")
        self.setup_filters_tab()
        self.setup_transform_tab()
        self.setup_border_tab()
        self.setup_watermark_tab()
        self.setup_format_tab()
        self.setup_info_tab()

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            try:
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            except ValueError:
                return (255, 255, 255) 
        return (255, 255, 255)

    def _get_text_color_for_bg(self, hex_bg_color: str) -> str:
        if not hex_bg_color:
            return "#000000"
        rgb = self._hex_to_rgb(hex_bg_color)
        luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255
        if luminance > 0.6: 
            return "#000000" 
        else:
            return "#FFFFFF"

    def create_settings_menu(self):
        self.settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.settings_frame.pack(fill="x", padx=20)
        self.label_theme = ctk.CTkLabel(self.settings_frame, text="Giao diện:")
        self.label_theme.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_theme = ctk.CTkOptionMenu(
            self.settings_frame, 
            values=["Dark", "Light"], 
            command=self.change_appearance_mode_event
        )
        self.optionmenu_theme.set("Dark")
        self.optionmenu_theme.grid(row=0, column=1, padx=(0, 20), pady=5, sticky="w")
        self.settings_frame.grid_columnconfigure(2, weight=1)

    def change_appearance_mode_event(self, new_mode: str):
        ctk.set_appearance_mode(new_mode)
        self.current_theme = new_mode

    def browse_file(self, file_type="image"):
        if file_type == "image":
            filetypes = (("Image files", "*.jpg *.jpeg *.png *.webp"), ("All files", "*.*"))
            title = "Chọn File Ảnh Đầu Vào"
        elif file_type == "pdf":
            filetypes = (("PDF files", "*.pdf"), ("All files", "*.*"))
            title = "Chọn File PDF Đầu Vào"
        file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if file_path:
            self.preview_image = None
        return file_path
    
    def browse_save_location(self, entry_widget, default_ext=".jpg"):
        file_path = filedialog.asksaveasfilename(
            defaultextension=default_ext,
            title="Chọn Vị Trí Lưu File Đầu Ra",
            initialdir=os.path.join(os.getcwd(), 'output') 
        )
        if file_path:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, file_path)
            
    def browse_folder(self, title="Chọn Thư Mục"):
        folder_path = filedialog.askdirectory(title=title)
        return folder_path

    def setup_filters_tab(self):
        tab = self.tab_view.tab("Bộ lọc & Hiệu ứng")
        tab.grid_columnconfigure(0, weight=1)
        
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", padx=10, pady=10, expand=True)
        scroll.grid_columnconfigure(0, weight=1)

        frame_io = self.create_io_section(scroll)
        frame_io.pack(fill="x", padx=10, pady=10)
        
        frame_basic = ctk.CTkFrame(scroll)
        frame_basic.pack(fill="x", padx=10, pady=10)
        frame_basic.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_basic, text="Độ sáng (0.1-2.0):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.slider_brightness_f = ctk.CTkSlider(frame_basic, from_=0.1, to=2.0, number_of_steps=190)
        self.slider_brightness_f.set(1.0)
        self.slider_brightness_f.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_basic, text="Độ tương phản (0.1-2.0):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.slider_contrast_f = ctk.CTkSlider(frame_basic, from_=0.1, to=2.0, number_of_steps=190)
        self.slider_contrast_f.set(1.0)
        self.slider_contrast_f.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_basic, text="Độ bão hòa (0.0-2.0):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.slider_saturation = ctk.CTkSlider(frame_basic, from_=0.0, to=2.0, number_of_steps=200)
        self.slider_saturation.set(1.0)
        self.slider_saturation.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_basic, text="Nhiệt độ màu (0.5-1.5):").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.slider_temperature = ctk.CTkSlider(frame_basic, from_=0.5, to=1.5, number_of_steps=100)
        self.slider_temperature.set(1.0)
        self.slider_temperature.grid(row=5, column=1, padx=10, pady=5, sticky="ew")
        
        frame_artistic = ctk.CTkFrame(scroll)
        frame_artistic.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_artistic, text="Chọn bộ lọc:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_artistic = ctk.CTkOptionMenu(frame_artistic, 
            values=["Không", "Nâu đỏ", "Dập nổi", "edge_detection", "Cổ điển", "Sơn dầu"])
        self.optionmenu_artistic.set("Không")
        self.optionmenu_artistic.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_artistic, text="Làm mờ/Làm nét:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_filter_f = ctk.CTkOptionMenu(frame_artistic, values=["Không", "Làm mờ", "Làm nét"])
        self.optionmenu_filter_f.set("Không")
        self.optionmenu_filter_f.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        self.var_motion_blur = ctk.BooleanVar(value=False)
        self.check_motion_blur = ctk.CTkCheckBox(frame_artistic, text="Motion Blur", variable=self.var_motion_blur)
        self.check_motion_blur.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_artistic, text="Góc Motion Blur:").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.slider_motion_angle = ctk.CTkSlider(frame_artistic, from_=0, to=360, number_of_steps=72)
        self.slider_motion_angle.set(0)
        self.slider_motion_angle.grid(row=3, column=2, padx=10, pady=5, sticky="ew")

        self.var_grayscale_f = ctk.BooleanVar(value=False)
        self.check_grayscale_f = ctk.CTkCheckBox(frame_artistic, text="Đen Trắng", variable=self.var_grayscale_f)
        self.check_grayscale_f.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        
        self.var_invert_f = ctk.BooleanVar(value=False)
        self.check_invert_f = ctk.CTkCheckBox(frame_artistic, text="Đảo màu", variable=self.var_invert_f)
        self.check_invert_f.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_artistic, text="Pixel hóa (0-50):").grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.slider_pixelate_f = ctk.CTkSlider(frame_artistic, from_=0, to=50, number_of_steps=50)
        self.slider_pixelate_f.set(0)
        self.slider_pixelate_f.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        frame_artistic.grid_columnconfigure(2, weight=1)

        self.create_action_buttons(scroll)

    def setup_transform_tab(self):
        tab = self.tab_view.tab("Biến đổi & Cắt xén")
        tab.grid_columnconfigure(0, weight=1)
        
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", padx=10, pady=10, expand=True)
        scroll.grid_columnconfigure(0, weight=1)
        
        frame_io = self.create_io_section(scroll)
        frame_io.pack(fill="x", padx=10, pady=10)
        
        frame_resize = ctk.CTkFrame(scroll)
        frame_resize.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_resize, text="Resize (WxH):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_resize_t = ctk.CTkEntry(frame_resize, width=150, placeholder_text="800x600")
        self.entry_resize_t.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_resize, text="Crop theo tỷ lệ:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_crop_ratio = ctk.CTkOptionMenu(frame_resize, 
            values=["Không", "1:1", "16:9", "4:3", "9:16", "3:4"])
        self.optionmenu_crop_ratio.set("Không")
        self.optionmenu_crop_ratio.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        frame_rotate = ctk.CTkFrame(scroll)
        frame_rotate.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame_rotate, text="Xoay:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_rotate_t = ctk.CTkOptionMenu(frame_rotate, 
            values=["Không", "90", "180", "270", "Xoay ngang", "Xoay dọc"])
        self.optionmenu_rotate_t.set("Không")
        self.optionmenu_rotate_t.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_rotate, text="Mirror (Đối xứng):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_mirror = ctk.CTkOptionMenu(frame_rotate, 
            values=["Không", "Ngang", "Dọc", "Cả hai"])
        self.optionmenu_mirror.set("Không")
        self.optionmenu_mirror.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.create_action_buttons(scroll)

    def setup_border_tab(self):
        tab = self.tab_view.tab("Viền & Khung")
        tab.grid_columnconfigure(0, weight=1)
        
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", padx=10, pady=10, expand=True)
        scroll.grid_columnconfigure(0, weight=1)
        
        frame_io = self.create_io_section(scroll)
        frame_io.pack(fill="x", padx=10, pady=10)
        
        frame_border = ctk.CTkFrame(scroll)
        frame_border.pack(fill="x", padx=10, pady=10)
        frame_border.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_border, text="Độ dày viền (0-50px):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.slider_border_width = ctk.CTkSlider(frame_border, from_=0, to=50, number_of_steps=50)
        self.slider_border_width.set(0)
        self.slider_border_width.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_border, text="Màu viền:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.btn_border_color = ctk.CTkButton(frame_border, text="Chọn màu", width=100,
                                              fg_color=self.selected_border_color,
                                              command=self.choose_border_color)
        self.btn_border_color.grid(row=1, column=3, padx=10, pady=5)
        
        ctk.CTkLabel(frame_border, text="Bo góc (0-100px):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.slider_rounded = ctk.CTkSlider(frame_border, from_=0, to=100, number_of_steps=100)
        self.slider_rounded.set(0)
        self.slider_rounded.grid(row=2, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        
        self.var_shadow = ctk.BooleanVar(value=False)
        self.check_shadow = ctk.CTkCheckBox(frame_border, text="Bật đổ bóng", variable=self.var_shadow)
        self.check_shadow.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_border, text="Offset:").grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.slider_shadow_offset = ctk.CTkSlider(frame_border, from_=0, to=30, number_of_steps=30)
        self.slider_shadow_offset.set(10)
        self.slider_shadow_offset.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_border, text="Độ mờ:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.slider_shadow_blur = ctk.CTkSlider(frame_border, from_=0, to=30, number_of_steps=30)
        self.slider_shadow_blur.set(10)
        self.slider_shadow_blur.grid(row=4, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_border, text="Màu bóng:").grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.btn_shadow_color = ctk.CTkButton(frame_border, text="Chọn màu", width=100,
                                              fg_color=self.selected_shadow_color,
                                              command=self.choose_shadow_color)
        self.btn_shadow_color.grid(row=4, column=3, padx=10, pady=5)
        self.create_action_buttons(scroll)

    def choose_border_color(self):
        color = colorchooser.askcolor(initialcolor=self.selected_border_color, title="Chọn màu viền")
        if color[1]:
            self.selected_border_color = color[1]
            text_color = self._get_text_color_for_bg(self.selected_border_color)
            self.btn_border_color.configure(fg_color=self.selected_border_color, text_color=text_color)

    def choose_shadow_color(self):
        color = colorchooser.askcolor(initialcolor=self.selected_shadow_color, title="Chọn màu bóng")
        if color[1]:
            self.selected_shadow_color = color[1]
            text_color = self._get_text_color_for_bg(self.selected_shadow_color)
            self.btn_shadow_color.configure(fg_color=self.selected_shadow_color, text_color=text_color)

    def setup_watermark_tab(self):
        tab = self.tab_view.tab("Đóng dấu bản quyền")
        tab.grid_columnconfigure(0, weight=1)
        
        scroll = ctk.CTkScrollableFrame(tab)
        scroll.pack(fill="both", padx=10, pady=10, expand=True)
        scroll.grid_columnconfigure(0, weight=1)
        
        frame_io = self.create_io_section(scroll)
        frame_io.pack(fill="x", padx=10, pady=10)

        frame_wm_text = ctk.CTkFrame(scroll)
        frame_wm_text.pack(fill="x", padx=10, pady=10)
        frame_wm_text.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(frame_wm_text, text="Nội dung:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_wm_text = ctk.CTkEntry(frame_wm_text, placeholder_text="Nhập text watermark...")
        self.entry_wm_text.grid(row=1, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_wm_text, text="Cỡ chữ:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.slider_wm_font_size = ctk.CTkSlider(frame_wm_text, from_=10, to=150, number_of_steps=110)
        self.slider_wm_font_size.set(40)
        self.slider_wm_font_size.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_wm_text, text="Độ mờ:").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.slider_wm_opacity = ctk.CTkSlider(frame_wm_text, from_=0.1, to=1.0, number_of_steps=90)
        self.slider_wm_opacity.set(0.5)
        self.slider_wm_opacity.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_wm_text, text="Vị trí:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_wm_position = ctk.CTkOptionMenu(frame_wm_text, 
            values=["br (Dưới phải)", "bl (Dưới trái)", "tr (Trên phải)", "tl (Trên trái)", "c (Giữa)"])
        self.optionmenu_wm_position.set("br (Dưới phải)")
        self.optionmenu_wm_position.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_wm_text, text="Phông chữ:").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        self.optionmenu_wm_font = ctk.CTkOptionMenu(frame_wm_text, 
            values=[
                    "arial.ttf (Arial)",
                    "arialbd.ttf (Arial Bold)",
                    "times.ttf (Times New Roman)",
                    "timesbd.ttf (Times Bold)",
                    "calibri.ttf (Calibri)",
                    "calibrib.ttf (Calibri Bold)",
                    "verdana.ttf (Verdana)",
                    "verdanab.ttf (Verdana Bold)",
                    "georgia.ttf (Georgia)",
                    "georgiab.ttf (Georgia Bold)",
                    "tahoma.ttf (Tahoma)",
                    "tahomabd.ttf (Tahoma Bold)",
                    "trebuc.ttf (Trebuchet MS)",
                    "impact.ttf (Impact)",
                    "consola.ttf (Consolas)",
                    "consolab.ttf (Consolas Bold)",
                    "comic.ttf (Comic Sans MS)"])
        self.optionmenu_wm_font.set("arial.ttf")
        self.optionmenu_wm_font.grid(row=3, column=3, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_wm_text, text="Màu chữ:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.btn_wm_color = ctk.CTkButton(frame_wm_text, text="Chọn màu", width=100,
                                          fg_color=self.selected_text_color,
                                          command=self.choose_text_color)
        self.btn_wm_color.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_wm_text, text="Xoay (độ):").grid(row=4, column=2, padx=10, pady=5, sticky="w")
        self.slider_wm_rotation = ctk.CTkSlider(frame_wm_text, from_=0, to=360, number_of_steps=72)
        self.slider_wm_rotation.set(0)
        self.slider_wm_rotation.grid(row=4, column=3, padx=10, pady=5, sticky="ew")
        
        self.var_wm_shadow = ctk.BooleanVar(value=False)
        self.check_wm_shadow = ctk.CTkCheckBox(frame_wm_text, text="Đổ bóng", variable=self.var_wm_shadow)
        self.check_wm_shadow.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        
        self.var_wm_outline = ctk.BooleanVar(value=False)
        self.check_wm_outline = ctk.CTkCheckBox(frame_wm_text, text="Viền ngoài", variable=self.var_wm_outline)
        self.check_wm_outline.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        
        frame_wm_img = ctk.CTkFrame(scroll)
        frame_wm_img.pack(fill="x", padx=10, pady=10)
        frame_wm_img.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_wm_img, text="Ảnh logo:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_wm_image = ctk.CTkEntry(frame_wm_img, placeholder_text="Đường dẫn logo...")
        self.entry_wm_image.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        btn_browse_logo = ctk.CTkButton(frame_wm_img, text="Duyệt", width=80,
                                        command=lambda: self.entry_wm_image.insert(0, self.browse_file("image")))
        btn_browse_logo.grid(row=1, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(frame_wm_img, text="Kích thước (% ảnh):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.slider_wm_img_size = ctk.CTkSlider(frame_wm_img, from_=5, to=50, number_of_steps=45)
        self.slider_wm_img_size.set(15)
        self.slider_wm_img_size.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        frame_timestamp = ctk.CTkFrame(scroll)
        frame_timestamp.pack(fill="x", padx=10, pady=10)
        frame_timestamp.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_timestamp, text="NHÃN THỜI GIAN", font=ctk.CTkFont(weight="bold", size=14)).grid(
            row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        self.var_timestamp = ctk.BooleanVar(value=False)
        self.check_timestamp = ctk.CTkCheckBox(frame_timestamp, text="Hiển thị thời gian", variable=self.var_timestamp)
        self.check_timestamp.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_timestamp, text="Cỡ chữ:").grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.slider_ts_font_size = ctk.CTkSlider(frame_timestamp, from_=10, to=80, number_of_steps=70)
        self.slider_ts_font_size.set(30)
        self.slider_ts_font_size.grid(row=1, column=2, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(frame_timestamp, text="Vị trí:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_ts_position = ctk.CTkOptionMenu(frame_timestamp, 
            values=["br (Dưới phải)", "bl (Dưới trái)", "tr (Trên phải)", "tl (Trên trái)", "c (Giữa)"])
        self.optionmenu_ts_position.set("bl (Dưới trái)")
        self.optionmenu_ts_position.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(frame_timestamp, text="Màu:").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        self.btn_ts_color = ctk.CTkButton(frame_timestamp, text="Chọn màu", width=100,
                                          fg_color=self.selected_timestamp_color,
                                          command=self.choose_timestamp_color)
        self.btn_ts_color.grid(row=2, column=3, padx=10, pady=5)
        
        ctk.CTkLabel(frame_timestamp, text="Múi giờ:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.optionmenu_ts_timezone = ctk.CTkOptionMenu(frame_timestamp, 
            values=["Asia/Ho_Chi_Minh", "Asia/Bangkok", "Asia/Tokyo", "UTC"])
        self.optionmenu_ts_timezone.set("Asia/Ho_Chi_Minh")
        self.optionmenu_ts_timezone.grid(row=3, column=1, columnspan=3, padx=10, pady=5, sticky="ew")
        self.create_action_buttons(scroll)

    def choose_text_color(self):
        color = colorchooser.askcolor(initialcolor=self.selected_text_color, title="Chọn màu chữ")
        if color[1]:
            self.selected_text_color = color[1]
            text_color = self._get_text_color_for_bg(self.selected_text_color)
            self.btn_wm_color.configure(fg_color=self.selected_text_color, text_color=text_color)

    def choose_timestamp_color(self):
        color = colorchooser.askcolor(initialcolor=self.selected_timestamp_color, title="Chọn màu timestamp")
        if color[1]:
            self.selected_timestamp_color = color[1]
            text_color = self._get_text_color_for_bg(self.selected_timestamp_color)
            self.btn_ts_color.configure(fg_color=self.selected_timestamp_color, text_color=text_color)

    def setup_format_tab(self):
        tab = self.tab_view.tab("Định dạng & PDF")
        tab.grid_columnconfigure(0, weight=1)
        
        frame_main = ctk.CTkFrame(tab)
        frame_main.pack(fill="both", padx=10, pady=10, expand=True)
        frame_main.grid_columnconfigure(1, weight=1)

        frame_format = ctk.CTkFrame(frame_main)
        frame_format.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        frame_format.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_format, text="CHUYỂN ĐỔI ĐỊNH DẠNG", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        ctk.CTkLabel(frame_format, text="File đầu vào:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_format_input = ctk.CTkEntry(frame_format, width=300)
        self.entry_format_input.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        btn_browse_fmt_in = ctk.CTkButton(frame_format, text="Duyệt", width=80,
                                          command=lambda: self.entry_format_input.insert(0, self.browse_file("image")))
        btn_browse_fmt_in.grid(row=1, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(frame_format, text="File đầu ra:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_format_output = ctk.CTkEntry(frame_format, width=300, placeholder_text="output.webp")
        self.entry_format_output.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        btn_browse_fmt_out = ctk.CTkButton(frame_format, text="Lưu...", width=80,
                                           command=lambda: self.browse_save_location(self.entry_format_output, ".webp"))
        btn_browse_fmt_out.grid(row=2, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(frame_format, text="Chất lượng (1-100):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.slider_format_quality = ctk.CTkSlider(frame_format, from_=1, to=100, number_of_steps=99)
        self.slider_format_quality.set(90)
        self.slider_format_quality.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        
        btn_run_format = ctk.CTkButton(frame_format, text="CHUYỂN ĐỔI", height=40,
                                       command=self.run_format_conversion)
        btn_run_format.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        frame_pdf = ctk.CTkFrame(frame_main)
        frame_pdf.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        frame_pdf.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_pdf, text="PDF sang ảnh", font=ctk.CTkFont(weight="bold")).grid(
            row=0, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        ctk.CTkLabel(frame_pdf, text="File PDF:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_pdf_input = ctk.CTkEntry(frame_pdf, width=300)
        self.entry_pdf_input.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        btn_browse_pdf = ctk.CTkButton(frame_pdf, text="Duyệt", width=80,
                                       command=lambda: self.entry_pdf_input.insert(0, self.browse_file("pdf")))
        btn_browse_pdf.grid(row=1, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(frame_pdf, text="Thư mục lưu:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_pdf_output = ctk.CTkEntry(frame_pdf, width=300)
        self.entry_pdf_output.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        btn_browse_pdf_out = ctk.CTkButton(frame_pdf, text="Duyệt", width=80,
                                           command=lambda: self.entry_pdf_output.insert(0, self.browse_folder("Chọn thư mục lưu")))
        btn_browse_pdf_out.grid(row=2, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(frame_pdf, text="DPI:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.entry_pdf_dpi = ctk.CTkEntry(frame_pdf, width=100)
        self.entry_pdf_dpi.insert(0, "300")
        self.entry_pdf_dpi.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        btn_run_pdf = ctk.CTkButton(frame_pdf, text="CHUYỂN ĐỔI PDF", height=40,
                                    command=self.run_pdf_to_jpg)
        btn_run_pdf.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    def run_format_conversion(self):
        input_path = self.entry_format_input.get()
        output_path = self.entry_format_output.get()
        quality = int(self.slider_format_quality.get())
        
        if not input_path or not output_path:
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin!")
            return
        
        try:
            img = transformer.open_image(input_path)
            if img and transformer.save_image(img, output_path, quality):
                messagebox.showinfo("Thành công", f"Đã chuyển đổi thành công!\nLưu tại: {output_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def run_pdf_to_jpg(self):
        input_path = self.entry_pdf_input.get()
        output_folder = self.entry_pdf_output.get()
        dpi = self.entry_pdf_dpi.get()
        
        if not input_path or not output_folder or not dpi.isdigit():
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin hợp lệ!")
            return
        
        try:
            success = transformer.process_pdf_to_jpg(input_path, output_folder, int(dpi))
            if success:
                messagebox.showinfo("Thành công", f"Đã chuyển đổi PDF thành công!\nLưu tại: {output_folder}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")

    def setup_info_tab(self):
        tab = self.tab_view.tab("Trích xuất thông tin hình ảnh")
        tab.grid_columnconfigure(0, weight=1)
        
        frame_main = ctk.CTkFrame(tab)
        frame_main.pack(fill="both", padx=10, pady=10, expand=True)
        frame_main.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_main, text="Chọn ảnh:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_info_input = ctk.CTkEntry(frame_main, width=400)
        self.entry_info_input.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        btn_browse_info = ctk.CTkButton(frame_main, text="Duyệt", width=80,
                                        command=lambda: self.entry_info_input.insert(0, self.browse_file("image")))
        btn_browse_info.grid(row=1, column=2, padx=10, pady=5)
        
        btn_run_info = ctk.CTkButton(frame_main, text="XEM THÔNG TIN", height=40,
                                     command=self.run_show_info)
        btn_run_info.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
        
        self.text_info_result = ctk.CTkTextbox(frame_main, height=400, font=ctk.CTkFont(family="Courier", size=12))
        self.text_info_result.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        frame_main.grid_rowconfigure(3, weight=1)

    def run_show_info(self):
        input_path = self.entry_info_input.get()
        if not input_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn ảnh!")
            return
        try:
            info = transformer.get_image_info(input_path)
            
            if 'error' in info:
                self.text_info_result.delete("1.0", "end")
                self.text_info_result.insert("1.0", f"LỖI: {info['error']}")
                return
            result_text = ""
            result_text += f"Tên file:   {info['filename']}\n"
            result_text += f"Kích thước: {info['width']} x {info['height']} pixels\n"
            result_text += f"Tỷ lệ:      {info['aspect_ratio']}\n"
            result_text += f"Định dạng:  {info['format']}\n"
            result_text += f"Chế độ màu: {info['mode']}\n"
            result_text += f"Dung lượng: {info['file_size_kb']} KB ({info['file_size_mb']} MB)\n"
            result_text += f"EXIF Data:  {'Có' if info['has_exif'] else 'Không'}\n"
            
            self.text_info_result.delete("1.0", "end")
            self.text_info_result.insert("1.0", result_text)
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {e}")
    
    def create_io_section(self, parent):
        frame_io = ctk.CTkFrame(parent)
        frame_io.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(frame_io, text="File đầu vào:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.entry_input = ctk.CTkEntry(frame_io, width=400)
        self.entry_input.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        btn_browse_in = ctk.CTkButton(frame_io, text="Duyệt", width=80,
                                      command=lambda: (self.entry_input.delete(0, "end"), 
                                                       self.entry_input.insert(0, self.browse_file("image"))))
        btn_browse_in.grid(row=1, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(frame_io, text="File đầu ra:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entry_output = ctk.CTkEntry(frame_io, width=400, placeholder_text="output/result.jpg")
        self.entry_output.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        btn_browse_out = ctk.CTkButton(frame_io, text="Lưu...", width=80,
                                       command=lambda: self.browse_save_location(self.entry_output, ".jpg"))
        btn_browse_out.grid(row=2, column=2, padx=10, pady=5)
        
        ctk.CTkLabel(frame_io, text="Chất lượng (1-100):").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.slider_quality = ctk.CTkSlider(frame_io, from_=1, to=100, number_of_steps=99)
        self.slider_quality.set(90)
        self.slider_quality.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky="ew")
        return frame_io

    def create_action_buttons(self, parent):
        frame_buttons = ctk.CTkFrame(parent, fg_color="transparent")
        frame_buttons.pack(fill="x", padx=10, pady=20)
        frame_buttons.grid_columnconfigure((0, 1), weight=1)
        
        btn_preview = ctk.CTkButton(frame_buttons, text="XEM TRƯỚC", height=50,
                                    command=self.run_preview,
                                    font=ctk.CTkFont(size=14, weight="bold"))
        btn_preview.grid(row=0, column=0, padx=5, pady=0, sticky="ew")
        
        btn_save = ctk.CTkButton(frame_buttons, text="LƯU ẢNH", height=50,
                                command=self.run_save,
                                font=ctk.CTkFont(size=14, weight="bold"))
        btn_save.grid(row=0, column=1, padx=5, pady=0, sticky="ew")

    def gather_all_args(self) -> Namespace | None:
        input_file = self.entry_input.get()
        output_file = self.entry_output.get()
        
        if not input_file:
            messagebox.showerror("Lỗi", "Vui lòng chọn File Đầu Vào.")
            return None
        
        resize_val = self.entry_resize_t.get() if hasattr(self, 'entry_resize_t') and self.entry_resize_t.get() else None
        quality_val = int(self.slider_quality.get())
        
        brightness_val = round(self.slider_brightness_f.get(), 2) if hasattr(self, 'slider_brightness_f') else 1.0
        contrast_val = round(self.slider_contrast_f.get(), 2) if hasattr(self, 'slider_contrast_f') else 1.0
        saturation_val = round(self.slider_saturation.get(), 2) if hasattr(self, 'slider_saturation') else 1.0
        temperature_val = round(self.slider_temperature.get(), 2) if hasattr(self, 'slider_temperature') else 1.0
        
        artistic_filter_val = self.optionmenu_artistic.get() if hasattr(self, 'optionmenu_artistic') else "None"
        filter_val = self.optionmenu_filter_f.get() if hasattr(self, 'optionmenu_filter_f') and self.optionmenu_filter_f.get() != "None" else None
        
        motion_blur_val = self.var_motion_blur.get() if hasattr(self, 'var_motion_blur') else False
        motion_angle_val = int(self.slider_motion_angle.get()) if hasattr(self, 'slider_motion_angle') else 0
        
        grayscale_val = self.var_grayscale_f.get() if hasattr(self, 'var_grayscale_f') else False
        invert_val = self.var_invert_f.get() if hasattr(self, 'var_invert_f') else False
        pixelate_val = int(self.slider_pixelate_f.get()) if hasattr(self, 'slider_pixelate_f') else 0
        if pixelate_val < 2: pixelate_val = None
        
        crop_ratio_val = self.optionmenu_crop_ratio.get() if hasattr(self, 'optionmenu_crop_ratio') else "None"
        rotate_val = self.optionmenu_rotate_t.get() if hasattr(self, 'optionmenu_rotate_t') else "Không"
        if rotate_val == "Không": rotate_val = None
        
        mirror_val = self.optionmenu_mirror.get() if hasattr(self, 'optionmenu_mirror') else "None"
        
        border_width_val = int(self.slider_border_width.get()) if hasattr(self, 'slider_border_width') else 0
        border_color_val = self.selected_border_color
        rounded_val = int(self.slider_rounded.get()) if hasattr(self, 'slider_rounded') else 0
        
        shadow_enabled_val = self.var_shadow.get() if hasattr(self, 'var_shadow') else False
        shadow_offset_val = int(self.slider_shadow_offset.get()) if hasattr(self, 'slider_shadow_offset') else 10
        shadow_blur_val = int(self.slider_shadow_blur.get()) if hasattr(self, 'slider_shadow_blur') else 10
        shadow_color_val = self.selected_shadow_color
        
        wm_text_val = self.entry_wm_text.get() if hasattr(self, 'entry_wm_text') else ""
        wm_font_size_val = int(self.slider_wm_font_size.get()) if hasattr(self, 'slider_wm_font_size') else 40
        wm_opacity_val = round(self.slider_wm_opacity.get(), 2) if hasattr(self, 'slider_wm_opacity') else 0.5
        wm_position_val = self.optionmenu_wm_position.get().split(' ')[0] if hasattr(self, 'optionmenu_wm_position') else 'br'
        wm_font_val = self.optionmenu_wm_font.get().split(' ')[0] if hasattr(self, 'optionmenu_wm_font') else 'arial.ttf'
        wm_color_val = self.selected_text_color
        wm_rotation_val = int(self.slider_wm_rotation.get()) if hasattr(self, 'slider_wm_rotation') else 0
        wm_shadow_val = self.var_wm_shadow.get() if hasattr(self, 'var_wm_shadow') else False
        wm_outline_val = self.var_wm_outline.get() if hasattr(self, 'var_wm_outline') else False
        
        wm_image_val = self.entry_wm_image.get() if hasattr(self, 'entry_wm_image') else ""
        wm_img_size_val = int(self.slider_wm_img_size.get()) if hasattr(self, 'slider_wm_img_size') else 15
        
        timestamp_enabled_val = self.var_timestamp.get() if hasattr(self, 'var_timestamp') else False
        ts_font_size_val = int(self.slider_ts_font_size.get()) if hasattr(self, 'slider_ts_font_size') else 30
        ts_position_val = self.optionmenu_ts_position.get().split(' ')[0] if hasattr(self, 'optionmenu_ts_position') else 'bl'
        ts_color_val = self.selected_timestamp_color
        ts_timezone_val = self.optionmenu_ts_timezone.get() if hasattr(self, 'optionmenu_ts_timezone') else 'Asia/Ho_Chi_Minh'
        
        args = Namespace(
            command='process',
            input_path=input_file,
            output_path=output_file,
            resize=resize_val,
            quality=quality_val,
            
            brightness=brightness_val,
            contrast=contrast_val,
            saturation=saturation_val,
            temperature=temperature_val,
            
            artistic_filter=artistic_filter_val,
            filter=filter_val,
            
            motion_blur=motion_blur_val,
            motion_blur_angle=motion_angle_val,
            
            grayscale=grayscale_val,
            invert=invert_val,
            pixelate_size=pixelate_val,
            
            crop_ratio=crop_ratio_val,
            rotate=rotate_val,
            mirror=mirror_val,
            
            border_width=border_width_val,
            border_color=border_color_val,
            rounded_radius=rounded_val,
            
            shadow_enabled=shadow_enabled_val,
            shadow_offset=shadow_offset_val,
            shadow_blur=shadow_blur_val,
            shadow_color=shadow_color_val,
            
            watermark_text=wm_text_val,
            watermark_font_size=wm_font_size_val,
            watermark_opacity=wm_opacity_val,
            watermark_position=wm_position_val,
            watermark_font=wm_font_val,
            watermark_text_color=wm_color_val,
            watermark_rotation=wm_rotation_val,
            watermark_shadow=wm_shadow_val,
            watermark_outline=wm_outline_val,
            watermark_image_path=wm_image_val,
            watermark_image_size=wm_img_size_val,
            
            timestamp_enabled=timestamp_enabled_val,
            timestamp_font_size=ts_font_size_val,
            timestamp_position=ts_position_val,
            timestamp_text_color=ts_color_val,
            timestamp_timezone=ts_timezone_val,
            timestamp_font=wm_font_val,
            timestamp_opacity=0.7
        )
        return args

    def run_preview(self):
        args = self.gather_all_args()
        if args is None:
            return
        
        print("Bắt đầu xử lý xem trước...")
        try:
            img_result = transformer.get_processed_image(args)
            if img_result:
                self.preview_image = img_result
                self.show_preview_window(self.preview_image)
            else:
                messagebox.showerror("Lỗi", "Không thể xử lý ảnh. Kiểm tra console.")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Có lỗi khi xử lý ảnh: {e}")
            print(f"Chi tiết lỗi: {e}")
            import traceback
            traceback.print_exc()

    def run_save(self):
        if self.preview_image is None:
            messagebox.showerror("Lỗi", "Vui lòng 'Xem Trước' ảnh trước khi lưu.")
            return
        output_file = self.entry_output.get()
        if not output_file:
            messagebox.showerror("Lỗi", "Vui lòng chọn Đường dẫn File Đầu Ra để lưu.")
            return
        quality_val = int(self.slider_quality.get())
        
        print(f"Bắt đầu lưu ảnh tới: {output_file}")
        try:
            success = transformer.save_image(self.preview_image, output_file, quality_val)
            if success:
                messagebox.showinfo("Thành công", f"Đã lưu ảnh thành công tại:\n{output_file}")
            else:
                messagebox.showerror("Thất bại", "Lưu ảnh thất bại. Kiểm tra console.")
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", f"Có lỗi xảy ra khi lưu: {e}")

    def show_preview_window(self, pil_image: Image.Image):
        if self.preview_window is not None and self.preview_window.winfo_exists():
            self.preview_window.destroy()
    
        self.preview_window = ctk.CTkToplevel(self)
        self.preview_window.title("Xem Trước Ảnh")
        self.preview_window.attributes("-topmost", True)
        self.preview_window.geometry("1000x800")
       
        self.zoom_scale = 1.0
        self.min_zoom = 0.1
        self.max_zoom = 5.0
        self.original_image = pil_image.copy()
        self.auto_fit = False
    
        self.canvas = ctk.CTkCanvas(self.preview_window, bg="gray20", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.drag_data = {"x": 0, "y": 0, "item": None}
        self.update_preview_image()
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)
        self.preview_window.bind("<Configure>", self.on_window_resize)
      
        control_frame = ctk.CTkFrame(self.preview_window, fg_color="transparent")
        control_frame.pack(fill="x", padx=10, pady=10)

        self.zoom_label = ctk.CTkLabel(control_frame, 
                                    text=f"Zoom: {int(self.zoom_scale * 100)}%",
                                    font=ctk.CTkFont(size=14, weight="bold"))
        self.zoom_label.pack(side="left", padx=10)
    
        self.zoom_slider = ctk.CTkSlider(
            control_frame,
            from_=self.min_zoom * 100,  
            to=self.max_zoom * 100,      
            number_of_steps=490,
            command=self.on_zoom_slider_change,
            width=400
        )
        self.zoom_slider.set(self.zoom_scale * 100)  
        self.zoom_slider.pack(side="left", padx=10, fill="x", expand=True)

        btn_fit = ctk.CTkButton(
            control_frame, 
            text=" Vừa với cửa sổ",
            command=self.fit_to_window,
            width=120,
            fg_color="#1f6aa5"
        )
        btn_fit.pack(side="left", padx=5)
        btn_reset = ctk.CTkButton(control_frame, text="Reset Zoom (100%)", 
                              command=self.reset_zoom, width=100)
        btn_reset.pack(side="left", pady=10)
        self.preview_window.grab_set()
        self.preview_window.focus()
        self.preview_window.after(100, self.fit_to_window)

    def fit_to_window(self):
        if not hasattr(self, 'preview_window') or not self.preview_window.winfo_exists():
            return
        self.auto_fit = False  
    
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
    
        if canvas_width <= 1:
            canvas_width = 980
        if canvas_height <= 1:
            canvas_height = 720
    
        padding = 20
        available_width = canvas_width - padding
        available_height = canvas_height - padding
        img_width = self.original_image.width
        img_height = self.original_image.height
        zoom_width = available_width / img_width
        zoom_height = available_height / img_height
        fit_zoom = min(zoom_width, zoom_height)
        fit_zoom = max(self.min_zoom, min(self.max_zoom, fit_zoom))
        self.zoom_scale = fit_zoom
        if hasattr(self, 'zoom_slider'):
            try:
                if self.zoom_slider.winfo_exists():
                    self.zoom_slider.set(fit_zoom * 100)
            except:
                pass
        self.update_preview_image()
    
    def on_window_resize(self, event):
        if not hasattr(self, 'preview_window') or event.widget != self.preview_window:
            return
        if not self.preview_window.winfo_exists():
            return
        if self.auto_fit:
            self.preview_window.after(100, self.fit_to_window)

    def on_zoom_slider_change(self, value):
        self.auto_fit = False
        new_zoom = float(value) / 100.0
        old_coords = None
        if self.drag_data.get("item"):
            try:
                old_coords = self.canvas.coords(self.drag_data["item"])
            except:
                pass
        old_zoom = self.zoom_scale
        self.zoom_scale = new_zoom
        self.update_preview_image()
    
        if old_coords and len(old_coords) >= 2 and old_zoom > 0:
           try:
               canvas_width = self.canvas.winfo_width() or 980
               canvas_height = self.canvas.winfo_height() or 720
               canvas_center_x = canvas_width / 2
               canvas_center_y = canvas_height / 2
               zoom_ratio = new_zoom / old_zoom
               dx = old_coords[0] - canvas_center_x
               dy = old_coords[1] - canvas_center_y
               new_x = canvas_center_x + dx * zoom_ratio
               new_y = canvas_center_y + dy * zoom_ratio
               self.canvas.coords(self.drag_data["item"], new_x, new_y)
           except:
              pass  

    def update_preview_image(self):
        if not hasattr(self, 'preview_window') or not self.preview_window.winfo_exists():
            return
        new_width = int(self.original_image.width * self.zoom_scale)
        new_height = int(self.original_image.height * self.zoom_scale)
        resized_img = self.original_image.copy()
        resized_img = resized_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo_image = ImageTk.PhotoImage(resized_img)
        self.canvas.delete("all")
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
    
        if canvas_width <= 1:
            canvas_width = 980
            canvas_height = 720
        x = canvas_width // 2
        y = canvas_height // 2
    
        self.drag_data["item"] = self.canvas.create_image(x, y, image=self.photo_image, anchor="center")
        if hasattr(self, 'zoom_label'):
            try:
                if self.zoom_label.winfo_exists():
                    self.zoom_label.configure(text=f"Zoom: {int(self.zoom_scale * 100)}%")
            except:
                pass

    def on_drag_start(self, event):
         self.drag_data["x"] = event.x
         self.drag_data["y"] = event.y

    def on_drag_motion(self, event):
        if self.drag_data["item"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.canvas.move(self.drag_data["item"], dx, dy)
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def reset_zoom(self):
         if not hasattr(self, 'preview_window') or not self.preview_window.winfo_exists():
             return
         self.auto_fit = False
         self.zoom_scale = 1.0
         if hasattr(self, 'zoom_slider'):
              try:
                  if self.zoom_slider.winfo_exists():
                      self.zoom_slider.set(100)
              except:
                  pass
         self.update_preview_image()

if __name__ == "__main__":
    app = ImageTransformerApp()
    app.mainloop()
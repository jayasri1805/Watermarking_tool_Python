import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🖋️ Multi-Language Image Watermark Tool")
        self.root.geometry("1320x820")
        self.root.configure(bg="#ECEFF1")

        self.image_path = None
        self.watermarked_img = None
        self.font_color = "#000000"
        self.wm_image_path = None

        # Language to font mapping
        self.languages = {
            "English": "arial.ttf",
            "Tamil": "Latha.ttf",
            "Telugu": "NotoSansTelugu-Regular.ttf"
        }

        self.setup_ui()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#263238")
        header.pack(fill="x")
        tk.Label(header, text="🖋️ Multi-Language Watermark Tool",
                 fg="white", bg="#263238",
                 font=("Segoe UI", 18, "bold")).pack(pady=8)

        content = tk.Frame(self.root, bg="#ECEFF1")
        content.pack(fill="both", expand=True, padx=15, pady=15)
        content.columnconfigure((0,1,2), weight=1)

        # LEFT PANEL
        left = tk.LabelFrame(content, text="Text Watermark Settings",
                             bg="#ECEFF1", fg="#37474F",
                             font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        left.grid(row=0, column=0, sticky="nsew", padx=5)

        ttk.Button(left, text="📁 Upload Main Image", command=self.upload_image).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(left, text="Watermark Type:", bg="#ECEFF1").grid(row=1, column=0, sticky="w")
        self.wm_type = tk.StringVar(value="text")
        ttk.Combobox(left, textvariable=self.wm_type,
                     values=["text", "image"], state="readonly", width=20).grid(row=1, column=1, pady=5, sticky="e")

        tk.Label(left, text="Language:", bg="#ECEFF1").grid(row=2, column=0, sticky="w")
        self.lang_var = tk.StringVar(value="English")
        lang_cb = ttk.Combobox(left, textvariable=self.lang_var,
                               values=list(self.languages.keys()), state="readonly", width=20)
        lang_cb.grid(row=2, column=1, pady=5, sticky="e")
        lang_cb.bind("<<ComboboxSelected>>", self.update_language)

        tk.Label(left, text="Text:", bg="#ECEFF1").grid(row=3, column=0, sticky="w")
        self.text_entry = tk.Entry(left, width=25, font=("Arial", 12))
        self.text_entry.grid(row=3, column=1, pady=5)

        tk.Label(left, text="Rotation Angle (°):", bg="#ECEFF1").grid(row=4, column=0, sticky="w")
        self.angle = tk.IntVar(value=0)
        tk.Entry(left, textvariable=self.angle, width=10).grid(row=4, column=1, pady=5, sticky="e")

        tk.Label(left, text="Opacity (0–255):", bg="#ECEFF1").grid(row=5, column=0, sticky="w")
        self.opacity = tk.IntVar(value=180)
        tk.Entry(left, textvariable=self.opacity, width=10).grid(row=5, column=1, pady=5, sticky="e")

        ttk.Button(left, text="🎨 Choose Color", command=self.choose_color).grid(row=6, column=0, columnspan=2, pady=10)

        tk.Label(left, text="Position:", bg="#ECEFF1").grid(row=7, column=0, sticky="w")
        self.position = tk.StringVar(value="bottom-right")
        ttk.Combobox(left, textvariable=self.position,
                     values=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                     state="readonly", width=20).grid(row=7, column=1, pady=5, sticky="e")

        # CENTER PANEL
        center = tk.LabelFrame(content, text="Image Watermark Settings",
                               bg="#ECEFF1", fg="#37474F",
                               font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        center.grid(row=0, column=1, sticky="nsew", padx=5)

        ttk.Button(center, text="🖼️ Upload Watermark Image", command=self.upload_watermark_image).pack(pady=8)

        tk.Label(center, text="Image Size (%)", bg="#ECEFF1").pack(anchor="w")
        self.wm_img_size = tk.IntVar(value=25)
        tk.Entry(center, textvariable=self.wm_img_size, width=10).pack(pady=3)

        tk.Label(center, text="Opacity (0–255)", bg="#ECEFF1").pack(anchor="w")
        self.wm_img_opacity = tk.IntVar(value=150)
        tk.Entry(center, textvariable=self.wm_img_opacity, width=10).pack(pady=3)

        ttk.Button(center, text="👁️ Preview", command=self.preview_watermark).pack(pady=12)
        ttk.Button(center, text="💾 Save Image", command=self.save_image).pack(pady=6)

        # RIGHT PANEL
        right = tk.LabelFrame(content, text="Output Preview",
                              bg="#ECEFF1", fg="#37474F",
                              font=("Segoe UI", 12, "bold"), padx=10, pady=10)
        right.grid(row=0, column=2, sticky="nsew", padx=5)

        self.preview_border = tk.Frame(right, bg="#FFFFFF", bd=3, relief="ridge")
        self.preview_border.pack(pady=10)
        self.canvas = tk.Label(self.preview_border, bg="white")
        self.canvas.pack()

    def update_language(self, event=None):
        lang = self.lang_var.get()
        if lang == "Tamil":
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, "வணக்கம்")
            self.text_entry.config(font=("Noto Sans Tamil", 12))
        elif lang == "Telugu":
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, "నమస్తే")
            self.text_entry.config(font=("Noto Sans Telugu", 12))
        else:
            self.text_entry.delete(0, tk.END)
            self.text_entry.insert(0, "Hello World")
            self.text_entry.config(font=("Arial", 12))

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.font_color = color

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.tiff")])
        if path:
            self.image_path = path
            messagebox.showinfo("Success", "Main image uploaded successfully!")

    def upload_watermark_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if path:
            self.wm_image_path = path
            messagebox.showinfo("Success", "Watermark image uploaded.")

    def find_font_file(self, font_name):
        if os.path.isfile(font_name):
            return font_name
        win_fonts = os.path.join("C:\\Windows\\Fonts", font_name)
        linux_fonts = os.path.join("/usr/share/fonts", font_name)
        if os.path.isfile(win_fonts):
            return win_fonts
        if os.path.isfile(linux_fonts):
            return linux_fonts
        return None  # Return None so we can fall back safely

    def apply_text_watermark(self, base):
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt)

        font_file = self.find_font_file(self.languages.get(self.lang_var.get(), "arial.ttf"))

        # Dynamic font size based on image width
        if base.width < 500:
            font_px = 20
        elif base.width < 1000:
            font_px = 40
        elif base.width < 2000:
            font_px = 60
        else:
            font_px = 80

        try:
            if font_file:
                font = ImageFont.truetype(font_file, font_px, layout_engine=ImageFont.LAYOUT_RAQM)
            else:
                raise FileNotFoundError
        except Exception:
            font = ImageFont.load_default()

        text = self.text_entry.get()
        bbox = draw.textbbox((0, 0), text, font=font)
        text_size = (bbox[2] - bbox[0], bbox[3] - bbox[1])

        x, y = self.get_position(base.size, text_size)
        draw.text((x, y), text, font=font,
                  fill=self.hex_to_rgba(self.font_color, self.opacity.get()))

        rotated = txt.rotate(self.angle.get(), expand=1)
        return Image.alpha_composite(base.convert("RGBA"), rotated)

    def apply_image_watermark(self, base):
        if not self.wm_image_path:
            return base

        watermark = Image.open(self.wm_image_path).convert("RGBA")
        scale = self.wm_img_size.get() / 100
        new_size = (int(base.size[0] * scale), int(base.size[1] * scale))
        watermark = watermark.resize(new_size)

        x, y = self.get_position(base.size, watermark.size)
        alpha = watermark.split()[3]
        alpha = alpha.point(lambda p: p * (self.wm_img_opacity.get() / 255))
        watermark.putalpha(alpha)

        base.paste(watermark, (x, y), watermark)
        return base

    def get_position(self, base_size, wm_size):
        pos = self.position.get()
        w, h = base_size
        tw, th = wm_size
        positions = {
            "top-left": (10, 10),
            "top-right": (w - tw - 10, 10),
            "bottom-left": (10, h - th - 10),
            "bottom-right": (w - tw - 10, h - th - 10),
            "center": ((w - tw) // 2, (h - th) // 2)
        }
        return positions.get(pos, (w - tw - 10, h - th - 10))

    def hex_to_rgba(self, hex_color, alpha):
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        return (r, g, b, alpha)

    def preview_watermark(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first.")
            return

        base_img = Image.open(self.image_path).convert("RGBA")
        if self.wm_type.get() == "text":
            result = self.apply_text_watermark(base_img)
        else:
            result = self.apply_image_watermark(base_img)

        self.watermarked_img = result
        preview_img = result.copy()
        preview_img.thumbnail((500, 500))
        tk_img = ImageTk.PhotoImage(preview_img)
        self.canvas.configure(image=tk_img)
        self.canvas.image = tk_img

    def save_image(self):
        if self.watermarked_img is None:
            messagebox.showerror("Error", "Preview the watermark first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".png",
                                            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            self.watermarked_img.convert("RGB").save(path)
            messagebox.showinfo("Saved", "Watermarked image saved!")

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")
    app = WatermarkApp(root)
    root.mainloop() 
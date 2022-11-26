import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from PIL import Image, ImageTk, ImageDraw, ImageFont


class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.image = None
        self.combined_image = None
        self.FONT_NAME = "Courier"
        self.title("Image Watermarking")
        self.config(padx=50, pady=50)
        self.canvas = Canvas(width=500, height=500, highlightthickness=0)
        self.canvas.grid(row=1, column=1, rowspan=8, padx=20)
        self.default_img = PhotoImage(file="No_image.png")
        upload_button = Button(text="Add image", command=self.add_image, font=(self.FONT_NAME, 10, "bold"))
        upload_button.grid(row=9, column=1, pady=20)
        self.img_frame = self.canvas.create_image(250, 250, image=self.default_img)
        self.slider_label = Label(text="Size:", font=(self.FONT_NAME, 10, "bold"))
        self.save_button = Button(text="Save", command=self.save, font=(self.FONT_NAME, 10, "bold"))
        current_value = DoubleVar()
        self.slider = Scale(from_=10, to=100, orient='horizontal', variable=current_value)
        self.watermark_label = Label(text="Watermark Text:", font=(self.FONT_NAME, 10, "bold"))
        self.watermark_input = Entry()

    def preview_watermark(self, pos):
        original_image = Image.Image.convert(self.image.copy(), "RGBA")
        width, height = self.image.size
        watermark_text = self.watermark_input.get()
        font = ImageFont.truetype('arial.ttf', size=int(self.slider.get()))
        watermark_text_size = font.getsize(watermark_text)
        watermarks_image = Image.new('RGBA', self.image.size, (255, 255, 255, 0))
        watermarks_draw = ImageDraw.Draw(watermarks_image)
        textwidth = watermark_text_size[0]
        text_image = Image.new('RGBA', watermark_text_size, (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_image)
        text_draw.text((0, 0), watermark_text, (255, 255, 255, 129), font=font)
        rotated_text_image = text_image.rotate(45, expand=True, fillcolor=(0, 0, 0, 0))

        x_padding = int(self.slider.get() * 1.5)
        y_padding = int(self.slider.get() * 1.5)

        match pos:
            case 1:
                watermarks_draw.text((x_padding, height - y_padding), watermark_text, (255, 255, 255, 129), font=font)
                self.combined_image = Image.alpha_composite(original_image, watermarks_image)
            case 2:
                watermarks_draw.text((width - x_padding - textwidth, height - y_padding), watermark_text,
                                     (255, 255, 255, 129),
                                     font=font)
                self.combined_image = Image.alpha_composite(original_image, watermarks_image)
            case 3:
                watermarks_draw.text((x_padding, y_padding), watermark_text, (255, 255, 255, 129), font=font)
                self.combined_image = Image.alpha_composite(original_image, watermarks_image)
            case 4:
                watermarks_draw.text((width - x_padding - textwidth, y_padding), watermark_text, (255, 255, 255, 129),
                                     font=font)
                self.combined_image = Image.alpha_composite(original_image, watermarks_image)
            case 5:
                x_start = 0
                for y in range(0, height, y_padding):
                    x = x_start
                    while x < width:
                        watermarks_draw.text((x, y), watermark_text, (255, 255, 255, 129), font=font)
                        x = x + textwidth + x_padding
                    x_start -= (textwidth + x_padding) * 1.5
                self.combined_image = Image.alpha_composite(original_image, watermarks_image)
            case 6:
                x_start = 0
                for y in range(0, height, y_padding + rotated_text_image.size[1]):
                    x = x_start
                    while x < width:
                        watermarks_image.paste(rotated_text_image, (int(x), int(y)))
                        x = x + textwidth + x_padding
                    x_start -= (textwidth + x_padding) * 1.5
                self.combined_image = Image.alpha_composite(original_image, watermarks_image)
            case _:
                self.combined_image = original_image
        im = ImageTk.PhotoImage(self.combined_image.resize((500, 500), Image.Resampling.LANCZOS))
        label = Label(image=im)
        label.image = im
        self.canvas.itemconfig(self.img_frame, image=im)
        self.save_button.grid(row=9, column=2, columnspan=2, pady=20, sticky='NEWS')

    def add_image(self):
        file_path = fd.askopenfilename()
        self.image = Image.open(file_path)
        im = ImageTk.PhotoImage(self.image.resize((500, 500), Image.Resampling.LANCZOS))
        label = Label(image=im)
        label.image = im  # keep a reference!
        self.canvas.itemconfig(self.img_frame, image=im)

        self.watermark_label.grid(row=2, column=2, pady=20)
        self.watermark_input.grid(row=2, column=3, sticky="EW")

        self.slider_label.grid(row=3, column=2, sticky='EW')
        self.slider.grid(row=3, column=3, sticky='EW')

        position_label = Label(text="------ Position ------", font=(self.FONT_NAME, 10, "bold"))
        position_label.grid(row=4, column=2, columnspan=2, pady=20)

        bl_button = Button(text="Bottom Left", command=lambda: self.preview_watermark(1),
                           font=(self.FONT_NAME, 10, "bold"))
        br_button = Button(text="Bottom Right", command=lambda: self.preview_watermark(2),
                           font=(self.FONT_NAME, 10, "bold"))
        tl_button = Button(text="Top Left", command=lambda: self.preview_watermark(3), font=(self.FONT_NAME, 10, "bold"))
        tr_button = Button(text="Top Right", command=lambda: self.preview_watermark(4), font=(self.FONT_NAME, 10, "bold"))
        horizontal_repeat = Button(text="Horizontal Repeat", command=lambda: self.preview_watermark(5),
                                   font=(self.FONT_NAME, 10, "bold"))
        diagonal_repeat = Button(text="Diagonal Repeat", command=lambda: self.preview_watermark(6),
                                 font=(self.FONT_NAME, 10, "bold"))

        bl_button.grid(row=5, column=2, sticky='NEWS')
        br_button.grid(row=5, column=3, sticky='NEWS')
        tl_button.grid(row=6, column=2, sticky='NEWS')
        tr_button.grid(row=6, column=3, sticky='NEWS')
        horizontal_repeat.grid(row=7, column=2, sticky='NEWS')
        diagonal_repeat.grid(row=7, column=3, sticky='NEWS')

    def save(self):
        file = fd.asksaveasfile(mode='wb', defaultextension=".png")
        if file:
            self.combined_image.save(file)



app = WatermarkApp()
app.mainloop()

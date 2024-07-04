import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel
from PIL import ImageTk, Image, ImageDraw
import asyncio
from controllers.image_editing_controller import ImageEditingController

class ImageEditingWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Image Editing")
        self.geometry("1000x800")
        self.controller = ImageEditingController(self)
        self.create_widgets()
        self.rect = None
        self.start_x = None
        self.start_y = None
        self.canvas_image = None

    def create_widgets(self):
        api_key_frame = tk.Frame(self)
        api_key_frame.pack(pady=10)

        tk.Label(api_key_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W)
        self.api_key_entry = tk.Entry(api_key_frame, width=40)
        self.api_key_entry.grid(row=0, column=1)

        upload_button = tk.Button(self, text="Upload Image", command=self.upload_image)
        upload_button.pack(pady=10)

        prompt_frame = tk.Frame(self)
        prompt_frame.pack(pady=10)

        tk.Label(prompt_frame, text="Crop your image and input User Prompt:").grid(row=0, column=0, sticky=tk.W)
        self.prompt_entry = tk.Entry(prompt_frame, width=40)
        self.prompt_entry.grid(row=0, column=1)

        self.canvas = tk.Canvas(self, cursor="cross")
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

        edit_button = tk.Button(self, text="Edit", command=lambda: asyncio.run(self.controller.edit_image()))
        edit_button.pack(pady=10)

        self.result_label = tk.Label(self)
        self.result_label.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if file_path:
            self.controller.set_image_path(file_path)
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas_image = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red')

    def on_mouse_drag(self, event):
        curX, curY = (event.x, event.y)
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        pass

    def get_mask(self):
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        mask = Image.new("L", self.image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rectangle([x1, y1, x2, y2], fill=255)
        return mask

    def show_image_in_new_window(self, image):
        new_window = Toplevel(self)
        new_window.title("Edited Image")

        img = ImageTk.PhotoImage(image)
        label = tk.Label(new_window, image=img)
        label.image = img  # keep a reference!
        label.pack()

        # 드롭다운 메뉴 추가
        menubar = tk.Menu(new_window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=lambda: self.save_image(image))
        menubar.add_cascade(label="File", menu=filemenu)
        new_window.config(menu=menubar)

    def save_image(self, image):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if file_path:
            try:
                image.save(file_path)
                messagebox.showinfo("Save", "Image saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")
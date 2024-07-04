import tkinter as tk
from tkinter import messagebox, filedialog
import asyncio
import requests
from io import BytesIO
from PIL import Image, ImageTk
from controllers.image_ai_controller import interact_with_gpt

class ImageAIWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Image AI")
        self.geometry("400x400")
        self.api_key = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        # API 키 입력 필드
        api_key_label = tk.Label(self, text="OpenAI API Key:")
        api_key_label.pack(pady=10)
        api_key_entry = tk.Entry(self, textvariable=self.api_key, width=40)
        api_key_entry.pack()

        # 텍스트 입력 필드
        text_label = tk.Label(self, text="생성할 이미지 입력 텍스트:")
        text_label.pack(pady=10)
        self.text_entry = tk.Entry(self, width=40)
        self.text_entry.pack()

        # 편집 옵션 선택
        options_frame = tk.Frame(self)
        options_frame.pack(pady=10)

        tk.Label(options_frame, text="Generating Options:").grid(row=0, column=0, sticky=tk.W)
        self.option_var = tk.StringVar(value="")
        tk.Radiobutton(options_frame, text="vivid", variable=self.option_var, value="vivid").grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(options_frame, text="natural", variable=self.option_var, value="natural").grid(row=2, column=0, sticky=tk.W)

        # 생성 버튼
        generate_button = tk.Button(self, text="Generate", command=self.generate_image)
        generate_button.pack(pady=10)

        # URL 표시 영역
        url_frame = tk.Frame(self)
        url_frame.pack(pady=10)

        self.url_label = tk.Label(url_frame, text="여기에 생성된 이미지 URL이 표시됩니다.", wraplength=350)
        self.url_label.pack(side=tk.LEFT)

        # Copy 버튼
        copy_button = tk.Button(url_frame, text="Copy", command=self.copy_url)
        copy_button.pack(side=tk.LEFT, padx=10)

    def generate_image(self):
        if not self.api_key:
            tk.messagebox.showwarning("경고", "OpenAI API 키를 입력하세요.")
            return

        if not self.text_entry:
            tk.messagebox.showwarning("경고", "생성할 이미지 입력 텍스트를 입력하세요.")
            return

        if not self.option_var.get():
            tk.messagebox.showwarning("경고", "Generating Options를 선택하세요.")
            return

        async def generate_image_async():
            api_key = self.api_key.get()
            user_input = self.text_entry.get()
            generating_option = self.option_var.get()
            image_url = await interact_with_gpt(api_key, user_input, generating_option)
            self.url_label.config(text=image_url)
            await self.display_image(image_url)
            self.option_var.set("")  # 옵션값 초기화

        asyncio.run(generate_image_async())

    async def display_image(self, image_url):
        # 이미지를 표시할 새 창 생성
        image_window = tk.Toplevel(self)
        image_window.title("Generated Image")

        # 드롭다운 메뉴 추가
        menubar = tk.Menu(image_window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save", command=lambda: self.save_image(img))
        menubar.add_cascade(label="File", menu=filemenu)
        image_window.config(menu=menubar)

        # 이미지 로드 및 표시
        response = requests.get(image_url)
        img_data = response.content
        img = Image.open(BytesIO(img_data))
        photo = ImageTk.PhotoImage(img)

        label = tk.Label(image_window, image=photo)
        label.pack()

        # 이미지 참조 유지
        label.image = photo

    def save_image(self, image):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if file_path:
            try:
                image.save(file_path)
                messagebox.showinfo("Save", "Image saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {str(e)}")

    def copy_url(self):
        url = self.url_label.cget("text")
        self.clipboard_clear()
        self.clipboard_append(url)



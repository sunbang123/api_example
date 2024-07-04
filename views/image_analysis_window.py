import tkinter as tk
from tkinter import filedialog
from controllers.image_analysis_controller import ImageAnalysisController

class ImageAnalysisWindow(tk.Toplevel):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller if controller else ImageAnalysisController()
        self.create_widgets()
        self.title("Google Cloud API Image Analyzer")


    def create_widgets(self):
        self.upload_json_button = tk.Button(self, text="JSON 토큰 업로드", command=self.upload_json_token)
        self.upload_json_button.pack(pady=10)

        self.json_label = tk.Label(self, text="")
        self.json_label.pack(pady=5)

        self.upload_image_button = tk.Button(self, text="이미지 업로드", command=self.upload_image)
        self.upload_image_button.pack(pady=10)

        self.image_label = tk.Label(self, text="")
        self.image_label.pack(pady=5)

        self.api_key_label = tk.Label(self, text="OpenAI API Key 입력:")
        self.api_key_label.pack(pady=5)
        
        self.api_key_entry = tk.Entry(self)
        self.api_key_entry.pack(pady=5)

        self.analyze_button = tk.Button(self, text="분석하기", command=self.analyze_image)
        self.analyze_button.pack(pady=10)

        self.result_text = tk.Text(self)
        self.result_text.pack(pady=10)

    def upload_json_token(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.controller.set_token_path(file_path)
            self.json_label.config(text=f"JSON 토큰: {file_path}")

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpge")])
        if file_path:
            self.controller.set_image_path(file_path)
            self.image_label.config(text=f"이미지: {file_path}")

    def analyze_image(self):
        api_key = self.api_key_entry.get()
        if api_key:
            self.controller.set_openai_key(api_key)
        else:
            self.result_text.insert(tk.END, "Please enter an OpenAI API key.\n")
            return

        result = self.controller.analyze_image()
        self.result_text.insert(tk.END, result)

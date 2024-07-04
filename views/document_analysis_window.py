import tkinter as tk
from tkinter import filedialog
from controllers.document_analysis_controller import DocumentAnalysisController
import asyncio

class DocumentAnalysisWindow(tk.Toplevel):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller if controller else DocumentAnalysisController()
        self.create_widgets()

    def create_widgets(self):
        self.upload_json_button = tk.Button(self, text="Upload JSON Token", command=self.upload_json_token)
        self.upload_json_button.pack(pady=10)

        self.json_label = tk.Label(self, text="")
        self.json_label.pack(pady=5)

        self.upload_document_button = tk.Button(self, text="Upload Document", command=self.upload_document)
        self.upload_document_button.pack(pady=10)

        self.document_label = tk.Label(self, text="")
        self.document_label.pack(pady=5)

        self.api_key_label = tk.Label(self, text="Enter OpenAI API Key:")
        self.api_key_label.pack(pady=5)

        self.api_key_entry = tk.Entry(self)
        self.api_key_entry.pack(pady=5)

        self.analyze_button = tk.Button(self, text="Analyze", command=self.analyze_document)
        self.analyze_button.pack(pady=10)

        self.result_text = tk.Text(self)
        self.result_text.pack(pady=10)

    def upload_json_token(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
        if file_path:
            self.controller.set_token_path(file_path)
            self.json_label.config(text=f"JSON Token: {file_path}")

    def upload_document(self):
        file_path = filedialog.askopenfilename(filetypes=[
            ("Text Files", "*.txt")
        ])
        if file_path:
            self.controller.set_document_path(file_path)
            self.document_label.config(text=f"Document: {file_path}")

    def analyze_document(self):
        api_key = self.api_key_entry.get()
        if api_key:
            self.controller.set_openai_key(api_key)
        else:
            self.result_text.insert(tk.END, "Please enter an OpenAI API key.\n")
            return

        result = self.controller.analyze_document()
        self.result_text.insert(tk.END, result)


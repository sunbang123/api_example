import tkinter as tk
import asyncio
from controllers.text_ai_controller import interact_with_gpt

class TextAIWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("OpenAI 텍스트 생성기")
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
        text_label = tk.Label(self, text="입력 텍스트:")
        text_label.pack(pady=10)
        self.text_entry = tk.Entry(self, width=40)
        self.text_entry.pack()

        # 생성 버튼
        generate_button = tk.Button(self, text="Generate", command=self.generate_text)
        generate_button.pack(pady=10)

        # 결과 출력 영역
        result_label = tk.Label(self, text="생성된 텍스트:")
        result_label.pack(pady=10)
        self.result_text = tk.Text(self, width=40, height=10)
        self.result_text.pack()

    def generate_text(self):
        async def generate_text_async():
            api_key = self.api_key.get()
            user_input = self.text_entry.get()
            generated_text = await interact_with_gpt(api_key, user_input)
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, generated_text)

        asyncio.run(generate_text_async())

import tkinter as tk

class MainWindow(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.title("AI Desktop App")
        self.geometry("400x500")
        self.create_widgets()

    def create_widgets(self):
        # 제목 라벨
        title_label = tk.Label(self, text="AI Desktop App", font=("Arial", 16))
        title_label.pack(pady=20)

        # 텍스트 AI 버튼
        text_ai_button = tk.Button(self, text="Text AI", command=self.controller.open_text_ai_window)
        text_ai_button.pack(pady=10)

        # 이미지 AI 버튼
        image_ai_button = tk.Button(self, text="Image AI", command=self.controller.open_image_ai_window)
        image_ai_button.pack(pady=10)

        # 이미지 분석 버튼
        image_analysis_button = tk.Button(self, text="Image Analysis", command=self.controller.open_image_analysis_window)
        image_analysis_button.pack(pady=10)

        # 문서 편집 버튼
        document_analysis_button = tk.Button(self, text="document Analysis", command=self.controller.open_document_analysis_window)
        document_analysis_button.pack(pady=10)

        # 이미지 편집 버튼
        image_editing_button = tk.Button(self, text="Image Editing", command=self.controller.open_image_editing_window)
        image_editing_button.pack(pady=10)

        # 작곡 AI 버튼
        music_composition_button = tk.Button(self, text="Music Composition", command=self.controller.open_music_composition_window)
        music_composition_button.pack(pady=10)
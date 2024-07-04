from views.document_analysis_window import DocumentAnalysisWindow
from views.main_window import MainWindow
from views.text_ai_window import TextAIWindow
from views.image_ai_window import ImageAIWindow
from views.image_analysis_window import ImageAnalysisWindow
from views.image_editing_window import ImageEditingWindow
from views.music_composition_window import MusicCompositionWindow

class MainController:
    def __init__(self):
        self.view = MainWindow(self)

    def run(self):
        self.view.mainloop()

    def open_text_ai_window(self):
        TextAIWindow(parent=self.view)
        # TextAIWindow 열기
        pass

    def open_image_ai_window(self):
        ImageAIWindow(parent=self.view)
        # ImageAIWindow 열기
        pass

    def open_image_analysis_window(self):
        ImageAnalysisWindow(parent=self.view)
        # ImageAnalysisWindow 열기
        pass

    def open_document_analysis_window(self):
        DocumentAnalysisWindow(parent=self.view)
        # ImageAnalysisWindow 열기
        pass

    def open_image_editing_window(self):
        ImageEditingWindow(parent=self.view)
        # ImageEditingWindow 열기
        pass

    def open_music_composition_window(self):
        MusicCompositionWindow(parent=self.view)
        # MusicCompositionWindow 열기
        pass
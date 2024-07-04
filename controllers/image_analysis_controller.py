from models.image_analyzer import ImageAnalyzer

class ImageAnalysisController:
    def __init__(self):
        self.analyzer = ImageAnalyzer()
        self.image_path = None

    def set_token_path(self, path):
        self.analyzer.set_token_path(path)

    def set_openai_key(self, api_key):
        self.analyzer.set_openai_key(api_key)

    def set_image_path(self, path):
        self.image_path = path

    def analyze_image(self):
        if self.image_path:
            return self.analyzer.analyze_image(self.image_path)
        return "No image uploaded"


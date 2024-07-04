from models.document_analyzer import DocumentAnalyzer

class DocumentAnalysisController:
    def __init__(self):
        self.analyzer = DocumentAnalyzer()
        self.document_path = None

    def set_token_path(self, path):
        self.analyzer.set_token_path(path)

    def set_openai_key(self, api_key):
        self.analyzer.set_openai_key(api_key)

    def set_document_path(self, path):
        self.document_path = path

    def analyze_document(self):
        if self.document_path:
            return self.analyzer.analyze_document(self.document_path)
        return "No document uploaded"

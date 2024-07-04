# models/__init__.py

from abc import ABC, abstractmethod

class FileAnalyzer(ABC):
    @abstractmethod
    def analyze(self, file_path: str) -> str:
        """파일을 분석하는 메서드
        :param file_path: 분석할 파일 경로
        :return: 분석 결과 문자열
        """
        pass
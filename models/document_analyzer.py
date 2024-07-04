import os
import logging
import json
from google.cloud import language_v1
from google.api_core.exceptions import PermissionDenied
import openai
import asyncio

from openai import AsyncOpenAI


class DocumentAnalyzer:
    def __init__(self):
        self.client = None
        self.api_key = None

    def set_token_path(self, path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
        self.client = language_v1.LanguageServiceClient()

    def set_openai_key(self, api_key):
        self.api_key = api_key

    def analyze_document(self, document_path):
        analyzer = TextDocumentAnalyzer(self.client, self.api_key)
        return analyzer.analyze(document_path)


class TextDocumentAnalyzer:
    def __init__(self, client, api_key):
        self.client = client
        self.api_key = api_key
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def analyze(self, document_path):
        if not os.path.exists(document_path):
            logging.error(f'File not found: {document_path}')
            return json.dumps({'error': 'File not found'})

        try:
            with open(document_path, 'r', encoding='utf-8') as file:
                content = file.read()
                if not content.strip():
                    return json.dumps({'error': 'Text file is empty'})

            document = language_v1.Document(content=content, type_=language_v1.Document.Type.PLAIN_TEXT)

            # Sentiment analysis
            sentiment_response = self.client.analyze_sentiment(request={'document': document})
            sentiment = sentiment_response.document_sentiment

            # Entity analysis
            entity_response = self.client.analyze_entities(request={'document': document})
            entities = entity_response.entities

            # Syntax analysis
            syntax_response = self.client.analyze_syntax(request={'document': document})
            tokens = syntax_response.tokens

            # Extract main topics and key phrases
            main_topics = [entity.name for entity in entities if entity.salience > 0.01]
            main_topics_str = ', '.join(main_topics)
            keywords_str = ', '.join([token.text.content for token in tokens[:5]])

            # Determine the overall sentiment
            if sentiment.score > 0:
                sentiment_text = '긍정적인'
            elif sentiment.score < 0:
                sentiment_text = '부정적인'
            else:
                sentiment_text = '중립적인'

            topics = {
                'topics': main_topics_str,
                'keywords': keywords_str,
                'sentiment': sentiment_text,
                'magnitude': sentiment.magnitude
            }

            summary = asyncio.run(self.summarize_topics(topics))
            logging.info(f'Text analyzed successfully: {document_path}')
            return summary
        except PermissionDenied as e:
            logging.error(f'Google API permission denied: {str(e)}')
            return json.dumps({'error': 'Google API permission denied'})
        except Exception as e:
            logging.error(f'Error analyzing text: {str(e)}')
            return json.dumps({'error': f'Error analyzing text: {str(e)}'})

    async def summarize_topics(self, topics):
        openai.api_key = self.api_key

        prompt = (
            "다음 주제와 주요 단어를 기반으로 글의 주요 주제를 요약해 주세요.\n"
            f"주제: {topics['topics']}\n"
            f"주요 단어: {topics['keywords']}\n"
            f"이 글의 전반적인 감정은 {topics['sentiment']}이고, 감정의 강도는 {topics['magnitude']}입니다.\n"
            "이 글의 주요 주제는 무엇인가요? 이 글을 3문장으로 요약하세요."
        )

        async with AsyncOpenAI(api_key=self.api_key) as client:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1200,
                temperature=0.5,
            )

        return response.choices[0].message.content.strip()

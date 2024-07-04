import os
from google.cloud import vision
import openai
import asyncio
from openai import AsyncOpenAI
import cv2
import numpy as np

class ImageAnalyzer:
    def __init__(self):
        self.client = None
        self.api_key = None

    def set_token_path(self, path):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = path
        self.client = vision.ImageAnnotatorClient()

    def set_openai_key(self, api_key):
        self.api_key = api_key

    def preprocess_image(self, image):
        # 이미지 크기 조정
        resized_image = cv2.resize(image, (800, 600))

        # 노이즈 제거
        denoised_image = cv2.fastNlMeansDenoisingColored(resized_image, None, 10, 10, 7, 21)

        # 대비 향상
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab_image = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2LAB)
        lab_image[:, :, 0] = clahe.apply(lab_image[:, :, 0])
        enhanced_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)

        return enhanced_image

    def segment_image(self, image):
        # 그레이스케일 변환
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 이진화
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 거리 변환
        dist_transform = cv2.distanceTransform(thresh, cv2.DIST_L2, 5)

        # 거리 변환 결과 정규화
        cv2.normalize(dist_transform, dist_transform, 0, 1.0, cv2.NORM_MINMAX)

        # 마커 생성
        _, markers = cv2.threshold(dist_transform, 0.4, 1.0, 0)
        markers = np.int32(markers)

        # 워터쉐드 알고리즘 적용
        markers = cv2.watershed(image, markers)

        # 세그멘테이션 결과 반환
        return markers

    def analyze_image(self, image_path):
        image = cv2.imread(image_path)
        preprocessed_image = self.preprocess_image(image)
        segmented_image = self.segment_image(preprocessed_image)

        # 세그멘테이션 결과를 기반으로 영역별 분석 수행
        unique_markers = np.unique(segmented_image)
        analysis_results = []

        for marker in unique_markers:
            if marker == -1:  # 경계선은 제외
                continue

            # 마커에 해당하는 영역 추출
            mask = np.uint8(segmented_image == marker)
            masked_image = cv2.bitwise_and(preprocessed_image, preprocessed_image, mask=mask)

            # 추출된 영역에 대한 분석 수행
            _, encoded_image = cv2.imencode('.jpg', masked_image)
            content = encoded_image.tobytes()
            image = vision.Image(content=content)

            response = self.client.annotate_image({
                'image': image,
                'features': [
                    {'type_': vision.Feature.Type.LABEL_DETECTION},
                    {'type_': vision.Feature.Type.OBJECT_LOCALIZATION},
                    {'type_': vision.Feature.Type.SAFE_SEARCH_DETECTION},
                ],
            })

            if response.error.message:
                continue

            labels = response.label_annotations
            objects = response.localized_object_annotations
            safe_search = response.safe_search_annotation

            labels_str = ', '.join([label.description for label in labels])
            objects_str = ', '.join([obj.name for obj in objects])
            safe_search_str = f"Adult: {safe_search.adult}, Violence: {safe_search.violence}"

            analysis_results.append({
                'labels': labels_str,
                'objects': objects_str,
                'safe_search': safe_search_str
            })

        # 분석 결과 종합
        combined_labels = ', '.join([result['labels'] for result in analysis_results])
        combined_objects = ', '.join([result['objects'] for result in analysis_results])
        combined_safe_search = ', '.join([result['safe_search'] for result in analysis_results])

        description = asyncio.run(self.describe_image(combined_labels, combined_objects, combined_safe_search))
        return description

    async def describe_image(self, labels, objects, safe_search):
        openai.api_key = self.api_key

        prompt = (
            "The following information has been detected from the image:\n"
            f"Labels: {labels}\n"
            f"Objects: {objects}\n"
            f"Safe Search: {safe_search}\n"
            "Based on this information, please provide a detailed description of the image's subject and content. "
            "Include details about the situation, actions, and atmosphere depicted in the image. Please exclude the speculation."
            "Your response should be at least 3 sentences long."
            "response in korean language."
        )

        async with AsyncOpenAI(api_key=self.api_key) as client:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7,
            )

        return response.choices[0].message.content.strip()

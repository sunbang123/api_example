import openai
from utils.image_utils import convert_image_format
import io

class ImageEditor:
    def __init__(self, api_key):
        self.api_key = api_key

    async def edit(self, image_path, mask, user_prompt):
        try:
            openai.api_key = self.api_key
            image_data = convert_image_format(image_path)

            # 마스크 이미지를 바이너리 데이터로 변환
            mask_bytes = io.BytesIO()
            mask.save(mask_bytes, format='PNG')
            mask_bytes.seek(0)

            async with openai.AsyncOpenAI(api_key=self.api_key) as client:
                response = await client.images.edit(
                    image=image_data,
                    mask=mask_bytes,
                    prompt=user_prompt,
                    n=1,
                    size="1024x1024",
                    response_format="url",
                )

            edited_image_url = response.data[0].url
            return edited_image_url

        except Exception as e:
            print(f"Error occurred while editing image: {str(e)}")
            return None

class ImageEditorProxy:
    def __init__(self, api_key):
        self.api_key = api_key
        self.image_editor = None

    def get_image_editor(self):
        if self.image_editor is None:
            self.image_editor = ImageEditor(self.api_key)
        return self.image_editor

    async def edit(self, image_path, mask, user_prompt):
        editor = self.get_image_editor()
        return await editor.edit(image_path, mask, user_prompt)

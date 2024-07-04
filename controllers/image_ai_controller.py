import openai
from openai import AsyncOpenAI
class GPTInterface:
    def __init__(self, api_key):
        self.api_key = api_key
        self.conversation_history = []

    async def generate_image(self, prompt, max_tokens=8192, generating_option="vivid"):
        async with AsyncOpenAI(api_key=self.api_key) as client:

            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n = 1,
                style = generating_option
            )

            # 응답에서 URL 추출
            image_url = response.data[0].url
            return image_url

    def build_conversation_prompt(self, new_prompt):
        conversation_prompt = self.conversation_history.copy()
        conversation_prompt.append({"role": "user", "content": new_prompt})
        return conversation_prompt

async def interact_with_gpt(api_key, user_input, generating_option):
    gpt = GPTInterface(api_key=api_key)
    generated_image_url = await gpt.generate_image(prompt=user_input, max_tokens=4096, generating_option="vivid")
    return generated_image_url
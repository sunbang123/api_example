import asyncio
from openai import AsyncOpenAI

class GPTInterface:
    def __init__(self, api_key):
        self.api_key = api_key
        self.conversation_history = []

    async def generate_text(self, prompt, max_tokens=8192):
        async with AsyncOpenAI(api_key=self.api_key) as client:
            # 이전 대화 내용을 프롬프트에 추가
            conversation_prompt = self.build_conversation_prompt(prompt)

            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_prompt,
                max_tokens=max_tokens
            )

            # 생성된 텍스트를 대화 기록에 추가
            self.conversation_history.append(
                {"role": "assistant", "content": response.choices[0].message.content.strip()})

            return response.choices[0].message.content.strip()

    def build_conversation_prompt(self, new_prompt):
        conversation_prompt = self.conversation_history.copy()
        conversation_prompt.append({"role": "user", "content": new_prompt})
        return conversation_prompt


async def interact_with_gpt(api_key, user_input):
    gpt = GPTInterface(api_key=api_key)
    generated_text = await gpt.generate_text(prompt=user_input, max_tokens=4096)
    return generated_text

from openai import AsyncOpenAI

async def analyze_keyword(keyword, api_key):
    client = AsyncOpenAI(api_key=api_key)
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a music composer."},
            {"role": "user", "content": f"Analyze the following keyword for music generation: {keyword}"}
        ]
    )
    return response.choices[0].message.content

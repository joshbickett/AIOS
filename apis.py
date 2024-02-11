from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)


def call_openai(messages, user_prompt, img_base64):
    vision_message = {
        "role": "user",
        "content": [
            {"type": "text", "text": user_prompt},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
            },
        ],
    }
    messages.append(vision_message)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        presence_penalty=1,
        frequency_penalty=1,
        temperature=0.7,
        max_tokens=1000,
    )

    content = response.choices[0].message.content
    print("[call_openai] content:", content)

    # content = clean_json(content)

    # assistant_message = {"role": "assistant", "content": content}

from openai import OpenAI
import os
from dotenv import load_dotenv
from config import Config

verbose = Config().verbose

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key=api_key,
)


def call_openai(messages, user_prompt, img_base64):
    if verbose:
        print("[call_openai]")
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

    stream = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=messages,
        stream=True,
    )

    print("[assistant] ", end="")
    content = ""

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
            content += chunk.choices[0].delta.content

    # content = clean_json(content)

    assistant_message = {"role": "assistant", "content": content}
    messages.append(assistant_message)

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gptModelUsed = os.getenv("GPT_MODEL_USED")


def conversation_send_openai(conversation_history):
    completion = client.chat.completions.create(
        model=gptModelUsed,
        messages=conversation_history,
    )
    return completion.choices[0].message.content

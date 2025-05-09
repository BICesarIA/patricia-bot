import os
from openai import OpenAI
from utils.google_sheets import (
    read_sheet_inventario,
)
from utils.whatsappBot import (
    history_conversation_flow,
)

PROMPT_INICIAL = os.getenv("PROMPT_INICIAL")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gptModelUsed = os.getenv("GPT_MODEL_USED")


def gpt_conversation_first_initialization(
    conversation_whatsappp_history, to_number, sender_number, incoming_msg
):
    df = read_sheet_inventario("Inventario", "Inventario")
    catalogo = "\n".join(
        [
            "; ".join([f"{col}: {row[col]}" for col in row.index])
            for _, row in df.iterrows()
        ]
    )

    history_conversation_flow(
        conversation_whatsappp_history,
        to_number,
        sender_number,
        {
            "role": "system",
            "content": f"{PROMPT_INICIAL} Este es el catalogo de articulos: {catalogo}",
        },
        None,
        None,
        None,
        "gpt",
    )

    gpt_conversation_history = [
        msg.get("incoming_msg")
        for msg in conversation_whatsappp_history["conversation_flow"]
        if msg.get("typeResponse") == "gpt"
    ]

    gpt_conversation_history.append({"role": "user", "content": incoming_msg})

    return gpt_conversation_history


def conversation_send_openai(conversation_history):
    completion = client.chat.completions.create(
        model=gptModelUsed,
        messages=conversation_history,
    )
    return completion.choices[0].message.content

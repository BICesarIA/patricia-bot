from datetime import datetime
import pytz
import os
import json

PHRASES_END_CONVERSATION_BY_GPT = json.loads(os.getenv("PHRASES_END_CONVERSATION_BY_GPT"))


def history_conversation_flow(
    conversationHistory, to, sender_number, msg, step, next_step, response, typeResponse
):
    dr_tz = pytz.timezone("America/Santo_Domingo")
    created_at = datetime.now(dr_tz).strftime("%Y-%m-%d %H:%M:%S")
    conversation_flow = conversationHistory["conversation_flow"]
    conversation_flow.append(
        {
            "To": to,
            "from": sender_number,
            "step": step,
            "next_step": next_step,
            "incoming_msg": msg,
            "response": response,
            "typeResponse": typeResponse,
            "created_at": created_at,
        }
    )


def clear_conversation(conversation_whatsappp_history):
    conversation_whatsappp_history["conversation_flow"] = []


def get_last_message(conversation_whatsappp_history):
    return (
        conversation_whatsappp_history["conversation_flow"][-1]
        if len(conversation_whatsappp_history["conversation_flow"]) > 0
        else []
    )


def gpt_end_conversation(gpt_response, conversation_whatsappp_history):
    if any(
        sentence.lower() in gpt_response.lower()
        for sentence in PHRASES_END_CONVERSATION_BY_GPT
    ):
        clear_conversation(conversation_whatsappp_history)
        return True
    return False

def history_conversation_flow(
    conversationHistory, to, sender_number, msg, step, next_step, response, typeResponse
):
    conversation_flow = conversationHistory["conversation_flow"]
    conversation_flow.append(
        {
            "To": to,
            "from": sender_number,
            "step": step,
            "next_step": next_step,
            "incoming_msg": msg,
            "responnse": response,
            "typeResponse": typeResponse
        }
    )

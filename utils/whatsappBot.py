from datetime import datetime
import pytz


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
            "responnse": response,
            "typeResponse": typeResponse,
            "created_at": created_at,
        }
    )

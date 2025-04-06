from flask import Flask, request
import os
from twilio.twiml.voice_response import VoiceResponse
from collections import defaultdict
from utils.gpt import conversation_send_openai
from utils.twilio import (
    conversation_gatherResponse,
    end_call_response,
    handle_error_response,
    make_voice_call,
)
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

from utils.whatsappBot import (
    history_conversation_flow,
)

app = Flask(__name__)

PROMPT_INICIAL = os.getenv("PROMPT_INICIAL")
conversation_histories = defaultdict(list)
conversation_whatsappp_histories = defaultdict(
    lambda: {
        "conversation_flow": [],
    }
)
sentencesToGptEndCall = [
    "pago agendado",
    "Gracias por su tiempo",
]


@app.route("/call", methods=["GET"])
def call():
    # return make_voice_call("+18098773238")
    return make_voice_call("8294465093")


@app.route("/voice", methods=["POST"])
def voice():
    recogido = request.form.get("SpeechResult", "")
    call_sid = request.form.get("CallSid")
    conversation_history = conversation_histories[call_sid]
    voiceResponseObj = VoiceResponse()

    try:
        if not recogido:
            conversation_history.append({"role": "system", "content": PROMPT_INICIAL})
            firstMessage = "Hola. Soy Patricia de BM Cell Comercial. Espero que estés bien. debes un total de 500 pesos, deseas pagarlo hoy o mañana?."
            # firstMessage = "Hola. Soy Patricia de BM Cell Comercial. Espero que estés bien. Te llamo para hablar sobre un pago pendiente."
            conversation_history.append({"role": "assistant", "content": firstMessage})
            return conversation_gatherResponse(
                voiceResponseObj,
                firstMessage,
            )

        completion = conversation_send_openai(conversation_history, recogido)
        respuesta = completion.choices[0].message.content

        if any(sentence in respuesta.lower() for sentence in sentencesToGptEndCall):
            return end_call_response(
                conversation_history,
                voiceResponseObj,
                respuesta,
            )

        conversation_history.append({"role": "assistant", "content": respuesta})
        return conversation_gatherResponse(voiceResponseObj, respuesta)

    except Exception as e:
        app.logger.error(e)
        return handle_error_response(conversation_history, voiceResponseObj)


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    try:
        googleDriveFileURL = "https://docs.google.com/spreadsheets/d/1wd6_OVgyhYFOvmuXS_oHRmaH-Ou4dPYo5pWbJZcjtpU/export?format=csv&gid=0"
        incoming_msg = request.values.get("Body", "").lower()
        resp = MessagingResponse()
        msg = resp.message()
        optionsMessage = """
    1️⃣ Aplicar para la oferta?
    2️⃣ Otro equipo distinto a la oferta?
    3️⃣ Ubicación
    4️⃣ Métodos de pago
        """

        sender_number = request.form.get("From")
        conversation_whatsappp_history = conversation_whatsappp_histories[sender_number]
        conversation_last_interaction = (
            conversation_whatsappp_history["conversation_flow"][-1]
            if len(conversation_whatsappp_history["conversation_flow"]) > 0
            else []
        )

        if len(conversation_whatsappp_history["conversation_flow"]) == 0:
            response = f"*CESAR IA Celulares*\n\nHola👋, Un placer de saludarte.\n¿En qué podemos servirle?\n\n{optionsMessage}".strip()

            history_conversation_flow(
                conversation_whatsappp_history,
                None,
                sender_number,
                incoming_msg,
                "start_menu",
                "select_menu_option",
                response,
            )
            msg.body(response)

        elif conversation_last_interaction["next_step"] == "start_menu" or (
            (
                conversation_last_interaction["step"] == "start_menu"
                or conversation_last_interaction["step"] == "select_menu_option"
            )
            and conversation_last_interaction["next_step"] != "redeem_offer_option"
        ):
            next_step = None

            if incoming_msg in ["1", "uno", "1️⃣"]:
                next_step = "redeem_offer_option"
                response = (
                    "📌 *Aplicar para la oferta* 📌\n\n"
                    "Dependiendo de los resultados de su evaluación, aplica para el inicial de la oferta desde RD$10 pesos en adelante.\n"
                    "Para aplicar, necesita:\n"
                    "1️⃣ Foto de su cédula o Pasaporte.\n"
                    "2️⃣ Dos familiares que den referencias. (*Se contactarán*)\n"
                    "3️⃣ Monto inicial 😎\n\n"
                    "*Envíe sus documentos* para validar su proceso y nos pondremos en contacto con usted."
                ).strip()

            elif incoming_msg in ["2", "dos", "2️⃣"]:
                response = "Aqui iniciara la conversacion con GPT. \n\n*Esto sera implementado en las proximas horas 🍻*"

            elif incoming_msg in ["3", "tres", "3️⃣"]:
                response = (
                    "📍 *Ubicación* 📍\n\n"
                    "Alma Rosa 1ra, Santo Domingo Este, a una esquina de la Sabana Larga.\n\n"
                    "📍 Google Maps: https://maps.app.goo.gl/w7LNLx43dawzeN3aA?g_st=ic\n\n"
                    "*También contamos con Delivery y envíos* 🏍️✈️🚍"
                ).strip()

            elif incoming_msg in ["4", "cuatro", "4️⃣"]:
                response = (
                    "💰 *Métodos de pago* 💰\n\n".join(
                        ["💲 Efectivo", "💻 Transferencia", "💳 Tarjeta de Crédito"]
                    )
                ).strip()

            else:
                response = ("⚠️ *Opción no válida* ⚠️\n\n" f"{optionsMessage}").strip()

            history_conversation_flow(
                conversation_whatsappp_history,
                None,
                sender_number,
                incoming_msg,
                "select_menu_option",
                next_step,
                response,
            )
            msg.body(response)

        elif conversation_last_interaction["next_step"] == "redeem_offer_option":
            response = "En breve un vendedor se estara comunicando con usted."
            history_conversation_flow(
                conversation_whatsappp_history,
                None,
                sender_number,
                incoming_msg,
                "redeem_offer_option",
                "start_menu",
                response,
            )
            msg.body(response)
            # elif lastOption in ["2", "dos", "2️⃣"]:
            #     msg.body("Que estas buscando?")

            #     conversation_flow = conversation_whatsappp_history[conversation_flow]
            #     conversation_flow.append({"in": 2})
            #     conversation_whatsappp_history = {
            #         "conversation_flow": conversation_flow
            #     }

        print(conversation_whatsappp_history)

        return str(resp)
    except Exception as e:
        app.logger.error(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

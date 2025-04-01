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

app = Flask(__name__)

PROMPT_INICIAL = os.getenv("PROMPT_INICIAL")
conversation_histories = defaultdict(list)
conversation_whatsappp_histories = defaultdict(list)
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
        incoming_msg = request.values.get("Body", "").lower()
        resp = MessagingResponse()
        msg = resp.message()
        greetings_word_sentences = ["hola", "saludos", "buenas", "hi", "hello"]
        optionsMessage = """
    1️⃣ Aplicar para la oferta?
    3️⃣ Ubicación
    4️⃣ Métodos de pago
        """
        # 2️⃣ Otro equipo distinto a la oferta?
        # 5️⃣ Hablar con un agente

        sender_number = request.form.get("From")
        conversation_whatsappp_history = conversation_whatsappp_histories[sender_number]

        if incoming_msg == "cancelar" or (
            any(word in incoming_msg for word in greetings_word_sentences)
            and conversation_whatsappp_history
        ):
            conversation_whatsappp_history.clear()

        if len(conversation_whatsappp_history) == 0:
            msg.body(
                "*CESAR IA Celulares*\n\n"
                "Hola👋, Un placer de saludarte.\n"
                "¿En qué podemos servirle?\n"
                f"{optionsMessage}"
            )
            conversation_whatsappp_history.append(incoming_msg)

        elif len(conversation_whatsappp_history) == 1:
            if incoming_msg in ["1", "uno", "1️⃣"]:
                msg.body(
                    "📌 *Aplicar para la oferta* 📌\n\n"
                    "Dependiendo de los resultados de su evaluación, aplica para el inicial de la oferta desde RD$10 pesos en adelante.\n"
                    "Para aplicar, necesita:\n"
                    "1️⃣ Foto de su cédula o Pasaporte.\n"
                    "2️⃣ Dos familiares que den referencias. (*Se contactarán*)\n"
                    "3️⃣ Monto inicial 😎\n\n"
                    "*Envíe sus documentos* para validar su proceso y nos pondremos en contacto con usted."
                )
                conversation_whatsappp_history.append(incoming_msg)

            elif incoming_msg in ["3", "tres", "3️⃣"]:
                msg.body(
                    "📍 *Ubicación* 📍\n\n"
                    "Alma Rosa 1ra, Santo Domingo Este, a una esquina de la Sabana Larga.\n\n"
                    "📍 Google Maps: https://maps.app.goo.gl/w7LNLx43dawzeN3aA?g_st=ic\n\n"
                    "*También contamos con Delivery y envíos* 🏍️✈️🚍"
                )

            elif incoming_msg in ["4", "cuatro", "4️⃣"]:
                msg.body(
                    "💰 *Métodos de pago* 💰\n"
                    + "\n".join(
                        ["💲 Efectivo", "💻 Transferencia", "💳 Tarjeta de Crédito"]
                    )
                )

            else:
                msg.body("⚠️ *Opción no válida* ⚠️\n\n" f"{optionsMessage}")

        elif len(conversation_whatsappp_history) == 2:
            lastOption = conversation_whatsappp_history[-1]

            if lastOption in ["1", "uno", "1️⃣"]:
                if any(
                    incoming_msg.lower().endswith(format.lower())
                    for format in [".jpg", ".png"]
                ):
                    msg.body(
                        "El documento ha sido recibido con exito! estarmod validando su informacion y nos comunacremos con usted"
                    )
                    conversation_whatsappp_history.clear()
                else:
                    msg.body(
                        "⚠️ *El documento enviado debe ser una imagen.* ⚠️ \n Si quieres cancelar el proceso, envia *calcelar*"
                    )

        return str(resp)
    except Exception as e:
        app.logger.error(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

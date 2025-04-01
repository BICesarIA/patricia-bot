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


@app.route("/test", methods=["GET"])
def test():
    testList = defaultdict(list)
    testListItem = testList[1]

    varLen = len(testListItem)
    testListItem.append(1)
    varLen2 = len(testListItem)
    testListItem.append(2)
    varLen3 = len(testListItem)
    return str("")


@app.route("/call", methods=["GET"])
def call():
    # return make_voice_call("+18098773238")
    return make_voice_call("+8294465093")


@app.route("/voice", methods=["POST"])
def voice():
    recogido = request.form.get("SpeechResult", "")
    call_sid = request.form.get("CallSid")
    conversation_history = conversation_histories[call_sid]
    voiceResponseObj = VoiceResponse()

    try:
        if not recogido:
            conversation_history.append({"role": "system", "content": PROMPT_INICIAL})
            firstMessage = "Hola. Soy Patricia de BM Cell Comercial. Espero que estés bien. Te llamo para hablar sobre un pago pendiente."
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
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    greetings_word_sentences = ["hola", "saludos", "buenas", "hi", "hello"]
    optionsMessage = """
1️⃣ Aplicar para la oferta?
2️⃣ Otro equipo distinto a la oferta?
3️⃣ Ubicación
4️⃣ Métodos de pago
    """
    # 5️⃣ Hablar con un agente

    sender_number = request.form.get("From")
    conversation_whatsappp_history = conversation_whatsappp_histories[sender_number]

    if (
        any(word in incoming_msg for word in greetings_word_sentences)
        and conversation_whatsappp_history
    ):
        conversation_whatsappp_history.clear()

    if len(conversation_whatsappp_history) == 0:
        msg.body(
            "*CESAR IA Celulares*\n\n"
            "Hola👋, Un placer de saldarte."
            "¿En que podemos servirle?"
            f"{optionsMessage}"
        )
        conversation_whatsappp_history.append(incoming_msg)
    elif len(conversation_whatsappp_history) == 1:
        if incoming_msg in ["1", "uno", "1️⃣"]:
            msg.body(
                "Dependiendo de los resultados de su evaluación, aplica para el Inicial de la oferta desde RD$10 pesos en adelante.\n"
                "Puedes completar los requisitos Sin Compromisos. Para aplicar necesita:\n\n"
                "1. Foto de su cédula o Pasaporte.\n"
                "2. Contar con dos familiares que den referencias de usted. (*Se contactarán*)\n"
                "3. Monto inicial😎\n\n"
                "Puedes iniciar el proceso enviando tus documentos y cuando sean validados nos pondremos en contacto con tigo."
            )
            conversation_whatsappp_history.append(incoming_msg)
        elif incoming_msg in ["3", "tres", "3️⃣"]:
            msg.body(
                "Alma Rosa 1ra,  Santo Domingo Este, a una esquina de la sabana larga.\n\n"
                "https://maps.app.goo.gl/w7LNLx43dawzeN3aA?g_st=ic\n\n"
                "*Igualmente, contamos con Delivery y envíos* 🏍️✈️🚍"
            )
        elif incoming_msg in ["4", "cuatro", "4️⃣"]:
            msg.body("Efectivo 💲\n" "Transferencia 💻\n" "Tarjeta de Crédito 💳")
        else:
            msg.body("Opciones validas:\n\n" f"{optionsMessage}")

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

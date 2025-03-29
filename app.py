from flask import Flask, request, Response
from openai import OpenAI
import os
from twilio.twiml.voice_response import VoiceResponse, Gather
from collections import defaultdict

app = Flask(__name__)

client = OpenAI(os.getenv("OPENAI_API_KEY"))
PROMPT_INICIAL = os.getenv("PROMPT_INICIAL")
gptModelUsed = os.getenv("GPT_MODEL_USED")
conversation_histories = defaultdict(list)
sentencesToGptEndCall = [
    "pago agendado",
    "Gracias por su tiempo",
]


@app.route("/voice", methods=["POST"])
def voice():
    recogido = request.form.get("SpeechResult", "")
    call_sid = request.form.get("CallSid")
    conversation_history = conversation_histories[call_sid]
    voiceResponseObj = VoiceResponse()

    try:
        if not recogido:
            conversation_history.append({"role": "system", "content": PROMPT_INICIAL})
            firstMessage = "Hola. Soy Patricia de BM Cell Comercial. Espero que estés bien. Te llamo para hablar sobre un pago pendiente. ¿Podemos hablar un momento?"
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


def conversation_gatherResponse(voiceResponseObj, message):
    gather = Gather(
        input="speech",
        action="/voice",
        method="POST",
        language="es-US",
        timeout=4,
    )
    gather.say(
        message,
        voice="Polly.Lupe",
        language="es-US",
    )
    voiceResponseObj.append(gather)
    return Response(str(voiceResponseObj), mimetype="text/xml")


def conversation_send_openai(conversation_history, recogido):
    conversation_history.append({"role": "user", "content": recogido})
    return client.chat.completions.create(
        model=gptModelUsed,
        messages=conversation_history,
    )


def end_call_response(conversation_history, voiceResponseObj, message):
    conversation_history.clear()
    voiceResponseObj.say(
        message,
        voice="Polly.Lupe",
        language="es-US",
    )
    voiceResponseObj.hangup()
    return Response(str(voiceResponseObj), mimetype="text/xml")


def handle_error_response(conversation_history, voiceResponseObj):
    conversation_history.clear()
    voiceResponseObj.say(
        "Lo siento, ha ocurrido un error procesando esta llamada. Te estaremos llamando mas tarde, disculpe los inconvenientes.",
        voice="Polly.Lupe",
        language="es-US",
    )
    return Response(str(voiceResponseObj), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

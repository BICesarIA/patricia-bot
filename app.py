from flask import Flask, request, Response
from openai import OpenAI
import os
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt base de Patricia
PROMPT_INICIAL = """
Eres Patricia de BM Cell Comercial y llamas al usuario por teléfono. Eres una cobradora amable, persuasiva y enfocada en resultados...
Todas las respuestas deben estar en español neutro con tono caribeño. No respondas en inglés ni tampoco preguntas que no sean referente a agendar
su pago pendiente, la llamada inicia con tigo preguntandole si pueden tener una conversacion.
"""

conversation_history = [
    {"role": "system", "content": PROMPT_INICIAL},
]


@app.route("/voice", methods=["POST"])
def voice():
    print("✅ Twilio llamó a /voice")
    recogido = request.form.get("SpeechResult", "")
    print(f"🗣️ SpeechResult recibido: {recogido}")

    voiceResponseObj = VoiceResponse()

    try:
        if not recogido:
            return conversation_gatherResponse(
                voiceResponseObj,
                "Hola, Leandro. Soy Patricia de BM Cell Comercial. Espero que estés bien. Te llamo para hablar sobre un pago pendiente. ¿Podemos hablar un momento?",
            )

        wordsToEnfCall = [
            "terminar la llamada",
            "no quiero",
            "finalizar llamada",
            "finalizar la llamada",
            "pago agendado",
        ]
        if any(word in recogido.lower() for word in wordsToEnfCall):
            return end_call_response()

        completion = conversation_send_openai(recogido)
        respuesta = completion["choices"][0]["message"]["content"]
        conversation_history.append({"role": "assistant", "content": respuesta})
        return conversation_gatherResponse(voiceResponseObj, respuesta)

    except Exception as e:
        print(f"❌ Error en voice(): {e}")
        return handle_error_response(voiceResponseObj)


def conversation_gatherResponse(voiceResponseObj, message):
    print(f"message: {message}")
    gather = Gather(
        input="speech",
        action="/voice",
        method="POST",
        language="es-US",
        timeout=3,
    )
    gather.say(
        message,
        voice="Polly.Lupe",
        language="es-US",
    )
    voiceResponseObj.append(gather)
    return Response(str(voiceResponseObj), mimetype="text/xml")


def conversation_send_openai(recogido):
    print("🤖 Enviando solicitud a OpenAI...")
    conversation_history.append({"role": "user", "content": recogido})
    return client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history,
    )


def end_call_response(voiceResponseObj):
    voiceResponseObj.say(
        "Gracias por tu tiempo.",
        voice="Polly.Lupe",
        language="es-US",
    )
    voiceResponseObj.hangup()
    return Response(str(voiceResponseObj), mimetype="text/xml")


def handle_error_response(voiceResponseObj):
    voiceResponseObj.say(
        "Lo siento, ha ocurrido un error procesando esta llamada. Por favor, intenta más tarde.",
        voice="Polly.Lupe",
        language="es-US",
    )
    return Response(str(voiceResponseObj), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

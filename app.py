from flask import Flask, request, Response
from openai import OpenAI
import os
from twilio.twiml.voice_response import VoiceResponse, Gather
from collections import defaultdict

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
PROMPT_INICIAL = """
Eres Patricia de BM Cell Comercial y llamas al usuario por teléfono. Eres una cobradora amable, persuasiva y enfocada en resultados.
Todas las respuestas deben estar en español neutro con tono caribeño. No respondas en inglés y no respondas preguntas que no sean referente a agendar
su pago pendiente, la llamada inicia con tigo preguntandole si pueden tener una conversacion. El objetivo de la llamada es agendar un pago que se debe
realizar el dia de la llamada o al siguiente dia, ya que la llamada se realiza como recordatorio de al usuario de que si no paga se va a cancelar su 
servicio, tu objetivo es responder dos preguntas, 'Si va a realizar su pago hoy o mañana' y 'Como va a realizar su pago en efectivo o transferencia'
cuando esas dos preguntas sean respondidas le diras al usuario 'pago agendado', no envies emojis ni ningun caracter especial ya que la conversacion 
sera por llamada telefonica
"""
conversation_histories = defaultdict(list)
sentencesToUserEndCall = [
    "No quiero hablar de eso.",
    "No estoy interesado.",
    "No voy a pagar.",
    "No puedo hablar ahora.",
    "No puedo atender en este momento.",
    "Estoy ocupado ahora mismo.",
    "Ahora no puedo.",
    "Llámame después.",
    "No quiero seguir con esta conversación.",
    "Prefiero no hablar de esto.",
    "No me interesa seguir discutiendo esto.",
    "No tengo tiempo para esto.",
    "Voy a colgar.",
    "Déjame pensarlo.",
    "Voy a revisar y te aviso.",
    "Voy a ver qué puedo hacer.",
    "Voy a consultar y te llamo.",
    "Lo hablamos después.",
    "Más tarde hablamos de eso.",
    "Luego lo veo.",
    "Te llamo si decido algo.",
    "Ya te dije que no.",
    "No insistas.",
    "No me vuelvas a llamar.",
    "Basta ya con esto.",
    "Déjame en paz.",
    "No quiero discutir más.",
    "No quiero seguir con esto.",
    "No voy a hablar de esto más.",
    "No voy a pagar ahora.",
    "No voy a tomar ninguna decisión en este momento.",
    "No puedo seguir hablando.",
    "No tengo más nada que decir.",
    "No voy a responder eso.",
    "Voy a colgar.",
    "No tengo dinero para pagar.",
    "No es un buen momento para hablar.",
    "No estoy en condiciones de atender esta llamada.",
    "Déjame ver qué puedo hacer.",
    "Voy a revisar y te aviso.",
    "Después hablamos de eso.",
    "Llámame más tarde.",
    "Voy a ver cómo hago y te aviso.",
    "No te puedo confirmar nada ahora.",
    "Déjame consultarlo primero.",
    "Déjame pensarlo.",
    "Voy a evaluar mis opciones.",
]
sentencesToGptEndCall = [
    "pago agendado",
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

        if any(sentence in recogido.lower() for sentence in sentencesToUserEndCall):
            return end_call_response(conversation_history, voiceResponseObj)

        completion = conversation_send_openai(conversation_history, recogido)
        respuesta = completion.choices[0].message.content

        if any(sentence in respuesta.lower() for sentence in sentencesToGptEndCall):
            return end_call_response(conversation_history, voiceResponseObj)

        conversation_history.append({"role": "assistant", "content": respuesta})
        return conversation_gatherResponse(voiceResponseObj, respuesta)

    except Exception as e:
        print(f"❌ Error en voice(): {e}")
        return handle_error_response(conversation_history, voiceResponseObj)


def conversation_gatherResponse(voiceResponseObj, message):
    print(f"message: {message}")
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
    print("🤖 Enviando solicitud a OpenAI...")
    conversation_history.append({"role": "user", "content": recogido})
    return client.chat.completions.create(
        model="gpt-4o",
        messages=conversation_history,
    )


def end_call_response(conversation_history, voiceResponseObj):
    conversation_history.clear()
    voiceResponseObj.say(
        "Gracias por tu tiempo.",
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

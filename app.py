from flask import Flask, request, Response
import os
from openai import OpenAI
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Prompt base de Patricia
PROMPT_INICIAL = """
Eres Patricia de BM Cell Comercial y llamas al usuario por teléfono. Eres una cobradora amable, persuasiva y enfocada en resultados...
Todas las respuestas deben estar en español neutro con tono caribeño. No respondas en inglés.
"""


@app.route("/voice", methods=["POST"])
def voice():
    print("✅ Twilio llamó a /voice")
    recogido = request.form.get("SpeechResult", "")
    print(f"🗣️ SpeechResult recibido: {recogido}")

    response = VoiceResponse()

    try:
        if not recogido:
            print("🕒 No hay SpeechResult, enviando primer mensaje...")
            gather = Gather(
                input="speech", action="/voice", method="POST", language="es-US", timeout=3
            )
            gather.say(
                "Hola, Leandro. Soy Patricia de BM Cell Comercial. Espero que estés bien. Te llamo para hablar sobre un pago pendiente. ¿Podemos hablar un momento?",
                voice="Polly.Lupe",
                language="es-US",
            )
            response.append(gather)
            return Response(str(response), mimetype="text/xml")

        print("🤖 Enviando solicitud a OpenAI...")
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": PROMPT_INICIAL},
                {"role": "user", "content": recogido},
            ],
        )

        respuesta = completion["choices"][0]["message"]["content"]
        print(f"✅ Respuesta de GPT: {respuesta}")

        gather = Gather(
            input="speech", action="/voice", method="POST", language="es-US", timeout=3
        )
        gather.say(respuesta, voice="Polly.Lupe", language="es-US")
        response.append(gather)
        return Response(str(response), mimetype="text/xml")

    except Exception as e:
        print(f"❌ Error en voice(): {e}")
        response.say(
            "Lo siento, ha ocurrido un error procesando esta llamada. Por favor, intenta más tarde.",
            voice="Polly.Lupe",
            language="es-US",
        )
        return Response(str(response), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

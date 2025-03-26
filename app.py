from flask import Flask, request, Response
import openai
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# Configura tu API Key
openai.api_key = 'TU_OPENAI_API_KEY'

# Prompt base de Patricia
PROMPT_INICIAL = """
Eres Patricia de BM Cell Comercial y llamas al usuario por teléfono. Eres una cobradora amable, persuasiva y enfocada en resultados, asegurándote de que el cliente realice su pago en el día de hoy o, en caso contrario, acuerde una fecha dentro de los próximos tres días. Tu tono es amable pero firme, dejando claro el motivo de la llamada de manera directa y profesional. Al inicio de la llamada, saludas con: "Hola, Leandro. Soy Patricia de BM Cell Comercial. Espero que estés bien."...
"""

@app.route("/voice", methods=['POST'])
def voice():
    recogido = request.form.get("SpeechResult", "")

    if not recogido:
        response = VoiceResponse()
        gather = Gather(input='speech', action='/voice', method='POST')
        gather.say("Hola, Leandro. Soy Patricia de BM Cell Comercial. Espero que estés bien. Te llamo para hablar sobre un pago pendiente. ¿Podemos hablar un momento?")
        response.append(gather)
        return Response(str(response), mimetype="text/xml")

    completion = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": PROMPT_INICIAL},
            {"role": "user", "content": recogido}
        ]
    )

    respuesta = completion['choices'][0]['message']['content']

    response = VoiceResponse()
    gather = Gather(input='speech', action='/voice', method='POST')
    gather.say(respuesta)
    response.append(gather)
    return Response(str(response), mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

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

from utils.whatsappBot import apply_to_offer, invalid_option, item_selected

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
        googleDriveFileURL = "https://docs.google.com/spreadsheets/d/1wd6_OVgyhYFOvmuXS_oHRmaH-Ou4dPYo5pWbJZcjtpU/export?format=csv&gid=0"
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
            if incoming_msg != "cancelar":
                conversation_whatsappp_history.append(incoming_msg)
            else:
                conversation_whatsappp_history.append("hola")

        elif len(conversation_whatsappp_history) == 1:
            if incoming_msg in ["1", "uno", "1️⃣"]:
                apply_to_offer(incoming_msg, conversation_whatsappp_history, msg)

            elif incoming_msg in ["2", "dos", "2️⃣"]:
                msg.body(
                    "1️⃣ Ver el catalogo de Articulos.\n"
                    "2️⃣ Buscar.\n\nSi quieres cancelar el proceso, envia *calcelar*"
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
                invalid_option(conversation_whatsappp_history, msg, optionsMessage)

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
                        "⚠️ *Debe enviar un documento valido.* ⚠️ \n Si quieres cancelar el proceso, envia *calcelar*"
                    )

            elif lastOption in ["2", "dos", "2️⃣"]:
                if incoming_msg in ["1", "uno", "1️⃣"]:
                    df = pd.read_csv(googleDriveFileURL)
                    sorted_categories = sorted(
                        df["tipo_articulo"].astype(str).str.strip().unique()
                    )
                    catalog = "\n".join(
                        [
                            f"{i + 1}. {category}"
                            for i, category in enumerate(sorted_categories)
                        ]
                    )

                    msg.body(f"Nuestro Catalogo\n\n{catalog}")
                    conversation_whatsappp_history.append(incoming_msg)

                elif incoming_msg in ["2", "dos", "2️⃣"]:
                    msg.body(
                        "Que articulo esta buscando?\n Si quieres cancelar el proceso, envia *calcelar*"
                    )
                    conversation_whatsappp_history.append(incoming_msg)

                else:
                    msg.body(
                        "⚠️ *Opción no válida seleccione una opcion del menu principal* ⚠️\n\n"
                        f"{optionsMessage}"
                    )

            else:
                invalid_option(conversation_whatsappp_history, msg, optionsMessage)

        elif len(conversation_whatsappp_history) == 3:
            lastOption = conversation_whatsappp_history[-1]

            if lastOption in ["1", "uno", "1️⃣"]:
                df = pd.read_csv(googleDriveFileURL)
                sorted_categories = sorted(df["tipo_articulo"].unique())

                index = int(incoming_msg) - 1
                if index > len(sorted_categories):
                    invalid_option(conversation_whatsappp_history, msg, optionsMessage)

                else:
                    itemSelected = sorted_categories[index]

                    filtered_df = df[df["tipo_articulo"] == itemSelected].reset_index(
                        drop=True
                    )
                    message = "\n".join(
                        [
                            f"{i + 1}. {row['Articulo']} - {row['precio_venta_unitario']} DOP"
                            for i, row in filtered_df.iterrows()
                        ]
                    )

                    conversation_whatsappp_history.append(incoming_msg)

                    msg.body(f"Seleccione el articulo deseado:\n\n{message}")

            elif lastOption in ["2", "dos", "2️⃣"]:
                df = pd.read_csv(googleDriveFileURL)
                filtered_df = df[
                    df["Articulo"].str.contains(incoming_msg, case=False, na=False)
                ].reset_index(drop=True)
                message = "\n".join(
                    [
                        f"{i + 1}.  {row['Articulo']} - {row['precio_venta_unitario']} DOP"
                        for i, row in filtered_df.iterrows()
                    ]
                )
                respuesta = ""
                if len(message) > 0:
                    conversation_whatsappp_history.append(incoming_msg)
                    respuesta = f"Coincidencias:\n\n{message}\n\nSi quieres cancelar el proceso, envia *calcelar*"
                else:
                    respuesta = f"Sin coincidencias. Pregunta por tu articulo mas adelante y puede que tengamos disponibilidad!"
                    conversation_whatsappp_history.clear()

                msg.body(respuesta)

        elif len(conversation_whatsappp_history) == 4:
            optionSelected = conversation_whatsappp_history[-2]

            if optionSelected == "1":
                df = pd.read_csv(googleDriveFileURL)
                sorted_categories = sorted(df["tipo_articulo"].unique())
                itemSelected = sorted_categories[
                    int(conversation_whatsappp_history[-1]) - 1
                ]

                filtered_df = df[df["tipo_articulo"] == itemSelected].reset_index(
                    drop=True
                )
                items = [row["Articulo"] for _, row in filtered_df.iterrows()]

                index = int(incoming_msg) - 1
                if index > len(items):
                    invalid_option(conversation_whatsappp_history, msg, optionsMessage)

                else:
                    item_selected(
                        conversation_whatsappp_history, items, incoming_msg, msg
                    )

            elif optionSelected == "2":
                df = pd.read_csv(googleDriveFileURL)
                filtered_df = df[
                    df["Articulo"].str.contains(
                        conversation_whatsappp_history[-1], case=False, na=False
                    )
                ].reset_index(drop=True)
                items = [row["Articulo"] for _, row in filtered_df.iterrows()]

                index = int(incoming_msg) - 1
                if index > len(items):
                    invalid_option(conversation_whatsappp_history, msg, optionsMessage)

                else:
                    item_selected(
                        conversation_whatsappp_history, items, incoming_msg, msg
                    )

            else:
                invalid_option(conversation_whatsappp_history, msg, optionsMessage)

        print(conversation_whatsappp_history)

        return str(resp)
    except Exception as e:
        app.logger.error(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, request
import os
from collections import defaultdict
from utils.gpt import conversation_send_openai
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

from utils.whatsappBot import (
    history_conversation_flow,
)

app = Flask(__name__)

PROMPT_INICIAL = os.getenv("PROMPT_INICIAL")
conversation_whatsappp_histories = defaultdict(
    lambda: {
        "conversation_flow": [],
    }
)


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
                "bot",
            )
            msg.body(response)

        elif conversation_last_interaction["next_step"] == "start_menu" or (
            (
                conversation_last_interaction["step"] == "start_menu"
                or conversation_last_interaction["step"] == "select_menu_option"
            )
            and conversation_last_interaction["next_step"] != "redeem_offer_option"
            and conversation_last_interaction["next_step"] != "start_gpt_conversation"
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
                next_step = "start_gpt_conversation"
                response = "Que articulo esta buscando?"

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
                "bot",
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
                "bot",
            )
            msg.body(response)

        elif conversation_last_interaction["next_step"] == "start_gpt_conversation":
            df = pd.read_csv(googleDriveFileURL)
            catalogo = "\n".join(
                [
                    f"(tipo_articulo: {row['tipo_articulo']}; Articulo: {row['Articulo']}; precio_venta_unitario: {row['precio_venta_unitario']} DOP)"
                    for _, row in df.iterrows()
                ]
            )

            history_conversation_flow(
                conversation_whatsappp_history,
                None,
                sender_number,
                {
                    "role": "system",
                    "content": f"{PROMPT_INICIAL} Este es el catalogo de articulos: {catalogo}",
                },
                None,
                None,
                None,
                "gpt",
            )

            history_conversation_flow(
                conversation_whatsappp_history,
                None,
                sender_number,
                {"role": "user", "content": incoming_msg},
                "start_gpt_conversation",
                None,
                None,
                "gpt",
            )

            gpt_conversation_history = [
                msg.get("incoming_msg")
                for msg in conversation_whatsappp_history["conversation_flow"]
                if msg.get("typeResponse") == "gpt"
            ]
            gpt_response = conversation_send_openai(gpt_conversation_history)

            history_conversation_flow(
                conversation_whatsappp_history,
                None,
                sender_number,
                None,
                "start_gpt_conversation",
                "gpt_conversation",
                {"role": "assistant", "content": gpt_response},
                "gpt",
            )
            msg.body(gpt_response)

        elif conversation_last_interaction["next_step"] == "gpt_conversation":
            history_conversation_flow(
                conversation_whatsappp_history,
                None,
                sender_number,
                {"role": "user", "content": incoming_msg},
                None,
                None,
                None,
                "gpt",
            )
            gpt_conversation_history = []
            for msg_flow in conversation_whatsappp_history["conversation_flow"]:
                if msg_flow.get("typeResponse") == "gpt":
                    if msg_flow.get("incoming_msg") != None:
                        gpt_conversation_history.append(msg_flow.get("incoming_msg"))
                    if msg_flow.get("responnse") != None:
                        gpt_conversation_history.append(msg_flow.get("responnse"))

            gpt_response = conversation_send_openai(gpt_conversation_history)
            next_step = "gpt_conversation"

            if any(
                sentence.lower() in gpt_response.lower()
                for sentence in [
                    "Articulo seleccionado exitosamente",
                    "Articulos seleccionados exitosamente",
                    "Artículos seleccionados exitosamente",
                    "Artículo seleccionado exitosamente",
                ]
            ):
                next_step = "start_menu"
            elif any(
                sentence.lower() in gpt_response.lower()
                for sentence in [
                    "vendedor se estará comunicando contigo",
                    "vendedor se pondrá en contacto",
                ]
            ):
                next_step = "start_menu"

            history_conversation_flow(
                conversation_whatsappp_history,
                None,
                sender_number,
                {"role": "user", "content": incoming_msg},
                "gpt_conversation",
                next_step,
                {"role": "assistant", "content": gpt_response},
                "gpt",
            )
            msg.body(gpt_response)

        print(conversation_whatsappp_history)
        return str(resp)
    except Exception as e:
        app.logger.error(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

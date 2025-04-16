import base64
from datetime import datetime
from flask import Flask, request
import os
from collections import defaultdict
import time
import pytz
from utils.google_sheets import (
    delete_old_messages,
    read_sheet_inventario,
    write_on_sheet_file,
)
from utils.gpt import conversation_send_openai
from twilio.twiml.messaging_response import MessagingResponse
from utils.requests import is_valid_image_url
from utils.whatsappBot import (
    clear_conversation,
    get_last_message,
    gpt_end_conversation,
    history_conversation_flow,
)
import re

app = Flask(__name__)

IMAGE_TRIGGER_PHRASE = "Aquí tienes la imagen de"
PROMPT_INICIAL = os.getenv("PROMPT_INICIAL")
INVENTORY_EXCEL_URL = os.getenv("INVENTORY_EXCEL_URL")
conversation_whatsappp_histories = defaultdict(
    lambda: {
        "conversation_flow": [],
    }
)


@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.values.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        optionsMessage = """
    1️⃣ Aplicar para la oferta?
    2️⃣ Otro equipo distinto a la oferta?
    3️⃣ Ubicación
    4️⃣ Métodos de pago
        """

        to_number = (request.form.get("To")).replace("whatsapp:+","")
        sender_number = (request.form.get("From")).replace("whatsapp:+", "")
        conversation_whatsappp_history = conversation_whatsappp_histories[sender_number]
        conversation_last_interaction = get_last_message(conversation_whatsappp_history)

        if conversation_last_interaction:
            tz = pytz.timezone("America/Santo_Domingo")
            dominicantime = datetime.now(tz)

            created_at_str = conversation_last_interaction["created_at"]
            created_at = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
            created_at = tz.localize(created_at)

            time_diff = dominicantime - created_at
            minutes_passed = int(time_diff.total_seconds() / 60)

            if minutes_passed >= 30:
                clear_conversation(conversation_whatsappp_history)
            elif (
                conversation_last_interaction["typeResponse"] == "gpt"
                and (
                    conversation_last_interaction["step"] == "start_gpt_conversation"
                    or conversation_last_interaction["step"] == "gpt_conversation"
                )
                and conversation_last_interaction["next_step"] == "start_menu"
                and minutes_passed < 30
            ):
                return str(resp)

        if len(conversation_whatsappp_history["conversation_flow"]) == 0:
            df = read_sheet_inventario("Inventario", "Datos")
            DatosPrincipales = "\n\n".join(df["Datos_Principales"].dropna())
            response = f"*{DatosPrincipales}* Hola👋, Un placer de saludarte.\n¿En qué podemos servirle?\n\n{optionsMessage}".strip()

            history_conversation_flow(
                conversation_whatsappp_history,
                to_number,
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
                response = "En que podemos servirle? 🙏🏾"

            elif incoming_msg in ["3", "tres", "3️⃣"]:
                df = read_sheet_inventario("Inventario", "Datos")
                Direccion = "\n\n".join(df["Direccion"].dropna())
                response = (
                    "📍 *Ubicación* 📍\n\n"
                    f"{Direccion}"
                    "*También contamos con Delivery y envíos* 🏍️✈️🚍"
                ).strip()

            elif incoming_msg in ["4", "cuatro", "4️⃣"]:
                df = read_sheet_inventario("Inventario", "Datos")
                MetodosDePago = "\n".join(df["Metodos_de_Pago"].dropna())
                response = (f"💰 *Métodos de pago* 💰\n\n{MetodosDePago}").strip()

            else:
                response = ("⚠️ *Opción no válida* ⚠️\n\n" f"{optionsMessage}").strip()

            history_conversation_flow(
                conversation_whatsappp_history,
                to_number,
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
                to_number,
                sender_number,
                incoming_msg,
                "redeem_offer_option",
                "start_menu",
                response,
                "bot",
            )
            msg.body(response)

        elif conversation_last_interaction["next_step"] == "start_gpt_conversation":
            delete_old_messages(sender_number)
            next_step = "gpt_conversation"
            df = read_sheet_inventario("Inventario", "Inventario")
            catalogo = "\n".join(
                [
                    "; ".join([f"{col}: {row[col]}" for col in row.index])
                    for _, row in df.iterrows()
                ]
            )

            history_conversation_flow(
                conversation_whatsappp_history,
                to_number,
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

            gpt_conversation_history = [
                msg.get("incoming_msg")
                for msg in conversation_whatsappp_history["conversation_flow"]
                if msg.get("typeResponse") == "gpt"
            ]
            gpt_conversation_history.append({"role": "user", "content": incoming_msg})
            gpt_response = conversation_send_openai(gpt_conversation_history)

            end_conversation = gpt_end_conversation(
                gpt_response, conversation_whatsappp_history
            )
            if end_conversation:
                next_step = "start_menu"

            history_conversation_flow(
                conversation_whatsappp_history,
                to_number,
                sender_number,
                {"role": "user", "content": incoming_msg},
                "start_gpt_conversation",
                next_step,
                {"role": "assistant", "content": gpt_response},
                "gpt",
            )
            msg.body(gpt_response)

        elif conversation_last_interaction["next_step"] == "gpt_conversation":
            history_conversation_flow(
                conversation_whatsappp_history,
                to_number,
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
                    if msg_flow.get("response") != None:
                        gpt_conversation_history.append(msg_flow.get("response"))

            gpt_response = conversation_send_openai(gpt_conversation_history)
            next_step = "gpt_conversation"

            end_conversation = gpt_end_conversation(
                gpt_response, conversation_whatsappp_history
            )
            if end_conversation:
                next_step = "start_menu"

            if IMAGE_TRIGGER_PHRASE.lower() in gpt_response.lower():
                match = re.search(
                    f"{re.escape(IMAGE_TRIGGER_PHRASE.lower())} (.+)",
                    gpt_response.lower(),
                )
                if match:
                    product_name = match.group(1).strip()
                    df = read_sheet_inventario("Inventario", "Inventario")
                    image_series = df[
                        df["Articulo"].str.lower() == product_name.lower()
                    ]["Imagen"]
                    if not image_series.empty:
                        not_image_response = "Disculpa, no tenemos foto de ese articulo por el momento 😥"
                        image_url = image_series.iloc[0]
                        if is_valid_image_url(image_url):
                            msg.media(image_url)

                            history_conversation_flow(
                                conversation_whatsappp_history,
                                to_number,
                                sender_number,
                                {"role": "user", "content": incoming_msg},
                                "gpt_conversation",
                                next_step,
                                {"role": "assistant", "content": gpt_response},
                                "gpt",
                            )
                            msg.body(gpt_response)

                            history_conversation_flow(
                                conversation_whatsappp_history,
                                to_number,
                                sender_number,
                                None,
                                "gpt_conversation",
                                next_step,
                                {"role": "assistant", "content": "<image of product>"},
                                "gpt",
                            )
                        else:
                            history_conversation_flow(
                                conversation_whatsappp_history,
                                to_number,
                                sender_number,
                                {"role": "user", "content": incoming_msg},
                                "gpt_conversation",
                                next_step,
                                {"role": "assistant", "content": not_image_response},
                                "gpt",
                            )
                            msg.body(not_image_response)
                else:
                    history_conversation_flow(
                        conversation_whatsappp_history,
                        to_number,
                        sender_number,
                        {"role": "user", "content": incoming_msg},
                        "gpt_conversation",
                        next_step,
                        {"role": "assistant", "content": not_image_response},
                        "gpt",
                    )
                    msg.body(not_image_response)
            else:
                history_conversation_flow(
                    conversation_whatsappp_history,
                    to_number,
                    sender_number,
                    {"role": "user", "content": incoming_msg},
                    "gpt_conversation",
                    next_step,
                    {"role": "assistant", "content": gpt_response},
                    "gpt",
                )
                msg.body(gpt_response)
        if (
            conversation_last_interaction
            and conversation_last_interaction["typeResponse"] == "gpt"
        ):
            time.sleep(5)

        last_message = get_last_message(conversation_whatsappp_history)
        write_on_sheet_file(
            {
                "from": last_message["from"],
                "incoming_msg": last_message["incoming_msg"],
                "response": last_message["response"],
                "created_at": last_message["created_at"],
                "typeResponse": last_message["typeResponse"],
            }
        )
        return str(resp)
    except Exception as e:
        app.logger.error(e)
        msg.body(
            "Disculpas, en este momento estamos teniendo problemas, nos estaremos comunicando con tigo mas adelante"
        )
        return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

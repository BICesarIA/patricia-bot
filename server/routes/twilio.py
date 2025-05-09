from datetime import datetime
from fastapi import APIRouter, Request
import os
import time
import pytz
from utils.google_sheets import (
    read_sheet_inventario,
)
from utils.gpt import conversation_send_openai, gpt_conversation_first_initialization
from twilio.twiml.messaging_response import MessagingResponse
from utils.requests import is_valid_image_url
from utils.whatsappBot import (
    clear_conversation,
    get_last_message,
    gpt_end_conversation,
    history_conversation_flow,
)
import re
from utils.database.postgres import save_message_to_db
from collections import defaultdict
from twilio.rest import Client
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import Response
from twilio.twiml.messaging_response import MessagingResponse

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
whatsapp_from = "whatsapp:+18492866787"
IMAGE_TRIGGER_PHRASE = "Aquí tienes la imagen de"
ERROR_MESSAGE = "Disculpas, en este momento estamos teniendo problemas, nos estaremos comunicando con tigo mas adelante"
INVENTORY_EXCEL_URL = os.getenv("INVENTORY_EXCEL_URL")
conversation_whatsappp_histories = defaultdict(
    lambda: {
        "conversation_flow": [],
    }
)

router = APIRouter()


@router.post("/whatsapp")
async def whatsapp(request: Request):
    form = await request.form()
    incoming_msg = form.get("Body", "").lower()
    resp = MessagingResponse()
    msg = resp.message()
    to_number = form.get("To")
    sender_number = form.get("From")

    try:
        optionsMessage = """
    1️⃣ Aplicar para la oferta?
    2️⃣ Otro equipo distinto a la oferta?
    3️⃣ Ubicación
    4️⃣ Métodos de pago
        """

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
            elif conversation_last_interaction["response"] == ERROR_MESSAGE or (
                conversation_last_interaction["typeResponse"] == "gpt"
                and conversation_last_interaction["step"] == "gpt_conversation"
                and conversation_last_interaction["next_step"] == "start_menu"
                and minutes_passed < 30
            ):
                await save_message_to_db(
                    {
                        "to": conversation_last_interaction["To"],
                        "from": conversation_last_interaction["from"],
                        "incoming_msg": incoming_msg,
                        "response": "",
                        "typeResponse": "client",
                    }
                )
                return str(resp)

        if len(conversation_whatsappp_history["conversation_flow"]) == 0:
            df = read_sheet_inventario("Inventario", "Datos")
            DatosPrincipales = "".join(df["Datos_Principales"].dropna())
            response = f"*{DatosPrincipales}*\n\n Hola👋, Un placer de saludarte.\n¿En qué podemos servirle?\n\n{optionsMessage}".strip()

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
            and conversation_last_interaction["next_step"] != "gpt_conversation"
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
                next_step = "gpt_conversation"
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

        elif conversation_last_interaction["next_step"] == "gpt_conversation":
            end_conversation_bypass = False
            gpt_conversation_history = []

            gpt_conversation_history = [
                msg.get("incoming_msg")
                for msg in conversation_whatsappp_history["conversation_flow"]
                if msg.get("typeResponse") == "gpt"
            ]

            if not gpt_conversation_history:
                gpt_conversation_history = gpt_conversation_first_initialization(
                    conversation_whatsappp_history,
                    to_number,
                    sender_number,
                    incoming_msg,
                )

                await save_message_to_db(
                    {
                        "to": to_number,
                        "from": sender_number,
                        "incoming_msg": incoming_msg,
                        "response": None,
                        "typeResponse": "bot",
                    }
                )

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
            else:
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
                for msg_flow in conversation_whatsappp_history["conversation_flow"]:
                    if msg_flow.get("typeResponse") == "gpt":
                        if msg_flow.get("incoming_msg") != None:
                            gpt_conversation_history.append(
                                msg_flow.get("incoming_msg")
                            )
                        if msg_flow.get("response") != None:
                            gpt_conversation_history.append(msg_flow.get("response"))
            
            filtered_history = [msg for msg in gpt_conversation_history if msg is not None]
            gpt_response = conversation_send_openai(filtered_history)
            next_step = "gpt_conversation"

            end_conversation = gpt_end_conversation(
                end_conversation_bypass, gpt_response, conversation_whatsappp_history
            )
            if end_conversation:
                next_step = "start_menu"

            if IMAGE_TRIGGER_PHRASE.lower() in gpt_response.lower():
                cannot_show_image = False

                try:
                    match = re.search(
                        rf"{re.escape(IMAGE_TRIGGER_PHRASE.lower())}\s+(.+?)(?:[\.,;!?\n\r]|$)",
                        gpt_response.lower(),
                    )
                    if match:
                        product_name = match.group(1).strip()
                        df = read_sheet_inventario("Inventario", "Inventario")
                        image_series = df[
                            df["Articulo"].str.lower() == product_name.lower()
                        ]["Imagen"]

                        if not image_series.empty:
                            image_url = image_series.iloc[0]
                            if is_valid_image_url(image_url):
                                msg.media(image_url)

                                history_conversation_flow(
                                    conversation_whatsappp_history,
                                    to_number,
                                    sender_number,
                                    None,
                                    "gpt_conversation",
                                    next_step,
                                    {
                                        "role": "assistant",
                                        "content": "<image of product>",
                                    },
                                    "gpt",
                                )
                            else:
                                cannot_show_image = True
                        else:
                            cannot_show_image = True
                except:
                    cannot_show_image = True

                if cannot_show_image:
                    not_image_response = "Valido con mi supervisor y le respondo"
                    end_conversation_bypass = True
                    next_step = "start_menu"

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
            time.sleep(0)

        last_message = get_last_message(conversation_whatsappp_history)

        if last_message:
            incoming_msg = None
            response = None
            if last_message["incoming_msg"] is not None:
                incoming_msg = (
                    last_message["incoming_msg"]
                    if last_message["typeResponse"] != "gpt"
                    else last_message["incoming_msg"]["content"]
                )
            if last_message["response"] is not None:
                response = (
                    last_message["response"]
                    if last_message["typeResponse"] != "gpt"
                    else last_message["response"]["content"]
                )

            await save_message_to_db(
                {
                    "to": last_message["To"],
                    "from": last_message["from"],
                    "incoming_msg": incoming_msg,
                    "response": response,
                    "typeResponse": last_message["typeResponse"],
                }
            )

        return Response(content=str(resp), media_type="application/xml")
    except Exception as e:
        await save_message_to_db(
            {
                "to": to_number,
                "from": sender_number,
                "incoming_msg": None,
                "response": ERROR_MESSAGE,
                "typeResponse": "bot",
            }
        )

        msg.body(ERROR_MESSAGE)
        return Response(content=str(resp), media_type="application/xml")


class SendMessageRequest(BaseModel):
    to: str
    message: str


@router.post("/send")
async def send_message(data: SendMessageRequest):
    twilio_client.messages.create(
        body=data.message,
        from_=whatsapp_from,
        to=f"whatsapp:{data.to}",
    )

    await save_message_to_db(
        {
            "to": whatsapp_from,
            "from": data.to,
            "incoming_msg": "",
            "response": data.message,
            "typeResponse": "seller",
        }
    )

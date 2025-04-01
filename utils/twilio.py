import os
from flask import Response, request
from twilio.twiml.voice_response import Gather
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


def make_voice_call(number):
    client = Client()
    call = client.calls.create(
        to=number, from_=TWILIO_PHONE_NUMBER, url=f"{request.host_url}voice"
    )

    return f"Call initiated! SID: {call.sid}"


def conversation_gatherResponse(voiceResponseObj, message):
    gather = Gather(
        input="speech",
        action="/voice",
        method="POST",
        language="es-US",
        timeout=2,
        barge_in=False,
    )
    gather.say(
        message,
        voice="Polly.Mia-Neural",
        language="es-US",
    )
    voiceResponseObj.append(gather)
    return Response(str(voiceResponseObj), mimetype="text/xml")


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

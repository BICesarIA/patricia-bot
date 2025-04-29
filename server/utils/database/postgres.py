from fastapi import FastAPI
from contextlib import asynccontextmanager
from .connection import database
from .models import conversations

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


async def save_message_to_db(last_message: dict):
    query = conversations.insert().values(
        to=last_message.get("to"),
        from_number=last_message.get("from"),
        incoming_msg=last_message.get("incoming_msg"),
        response=last_message.get("response"),
        type_response=last_message.get("typeResponse")
    )
    await database.execute(query)


app = FastAPI(lifespan=lifespan)

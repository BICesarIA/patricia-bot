from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy import delete
from sqlalchemy import desc, func, select
from .connection import database
from .models import conversations
from utils.websocket_manager import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


async def save_message_to_db(last_message: dict):
    obj = {
        "to": last_message.get("to"),
        "from_number": last_message.get("from"),
        "incoming_msg": last_message.get("incoming_msg"),
        "response": last_message.get("response"),
        "type_response": last_message.get("typeResponse"),
    }
    query = conversations.insert().values(obj)
    await database.execute(query)
    await manager.broadcast({"type": "message", "payload": obj})


async def conversations_from_number(phone_number):
    query = conversations.select().where(conversations.c.from_number == phone_number)
    return await database.fetch_all(query)


async def conversations_open():
    c1 = conversations.alias("c1")
    c2 = conversations.alias("c2")

    subquery = (
        select(func.max(c2.c.created_at))
        .where(c2.c.from_number == c1.c.from_number)
        .scalar_subquery()
    )

    query = (
        select(c1).where(c1.c.created_at == subquery).order_by(desc(c1.c.created_at))
    )

    return await database.fetch_all(query)


async def delete_conversation(from_number: str):
    query = delete(conversations).where(conversations.c.from_number == from_number)
    await database.execute(query)


async def delete_all_conversation():
    query = delete(conversations)
    await database.execute(query)


app = FastAPI(lifespan=lifespan)

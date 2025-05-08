from datetime import datetime
from pydantic import BaseModel
from utils.database.postgres import (
    conversations_from_number,
    conversations_open,
    delete_all_conversation,
    delete_conversation,
)
from typing import List
from fastapi import APIRouter
from typing import Optional

router = APIRouter()


class Conversation(BaseModel):
    id: int
    to: str
    from_number: str
    incoming_msg: Optional[str] = None
    response: Optional[str] = None
    type_response: str
    created_at: datetime


@router.get("/conversations/{phone_number}", response_model=List[Conversation])
async def get_conversations_from_number(phone_number: str):
    result = await conversations_from_number(phone_number)
    return result


@router.get("/conversations", response_model=List[Conversation])
async def get_conversatios_open():
    result = await conversations_open()
    return result


@router.post("/conversations/delete")
async def post_delete_all_conversation():
    await delete_all_conversation()


@router.post("/conversations/delete/{phone_number}")
async def post_delete_conversation(phone_number):
    await delete_conversation()

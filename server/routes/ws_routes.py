from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from server.utils.websocket_manager import manager

ws_router = APIRouter()

@ws_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

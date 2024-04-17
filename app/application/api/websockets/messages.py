
from fastapi.websockets import WebSocket
from fastapi.routing import APIRouter


router = APIRouter(tags=['chats'])


@router.websocket('{chat_oid}')
async def messages_handlers(chat_oid: str, websocket: WebSocket):
    await websocket.accept()

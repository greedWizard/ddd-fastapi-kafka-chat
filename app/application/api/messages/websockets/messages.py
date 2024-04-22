from uuid import UUID
from fastapi import Depends, WebSocketDisconnect
from punq import Container

from fastapi.websockets import WebSocket
from fastapi.routing import APIRouter
from websockets import ConnectionClosed

from infra.message_brokers.base import BaseMessageBroker
from infra.websockets.managers import BaseConnectionManager
from logic.init import init_container
from logic.mediator.base import Mediator
from settings.config import Config


router = APIRouter(tags=['chats'])


@router.websocket("/{chat_oid}/")
async def websocket_endpoint(
    chat_oid: str,
    websocket: WebSocket,
    container: Container = Depends(init_container),
):
    connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
    await connection_manager.accept_connection(websocket=websocket, key=chat_oid)

    # print("Connection established")
    await websocket.send_text("You are now connected!")

    try:
        while True:
            # Здесь должен быть код, который слушает то, что приходит в вебсокет,
            # и создает новые ивенты на поступление сообщений в вебсокет
            # и закидывает это всё в медиатор, оно там всё хэндлится и т.д.
            await websocket.receive_text()

        # Но так как мы ничего не читаем, то просто  захурим бесконечный цикл,
        # который держит коннет (читает в пустоту) и рвётся при дисконнекте
    except WebSocketDisconnect:
        # Мы сами не рвём соединение, а вот когда от нас кто-то отключается,
        # рейзится эксепшн, в котором мы просто удаляем коннект из списка, чтобы
        # на него мы уже не слали сообщения в будущем. Поэтому нам на самом деле
        # не надо явно вызывать websocket.close() нигде.
        # Основываюсь на этом:
        # https://fastapi.tiangolo.com/advanced/websockets/#handling-disconnections-and-multiple-clients

        print("Connection broken")

        await connection_manager.remove_connection(websocket=websocket, key=chat_oid)


# @router.websocket("/{chat_oid}/")
# async def websocket_endpoint(
#     chat_oid: UUID,
#     websocket: WebSocket,
#     container: Container = Depends(init_container),
# ):
#     config: Config = container.resolve(Config)
#     connection_manager: BaseConnectionManager = container.resolve(BaseConnectionManager)
#
#     await connection_manager.accept_connection(websocket=websocket, key=chat_oid)
#
#     message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
#
#     try:
#         async for message in message_broker.start_consuming(
#             topic=config.new_message_received_topic,
#         ):
#             await connection_manager.send_all(key=chat_oid, json_message=message)
#     finally:
#         await connection_manager.remove_connection(websocket=websocket, key=chat_oid)
#         await message_broker.stop_consuming()
#
#     await message_broker.stop_consuming()
#     await websocket.close(reason='Dolboeb')

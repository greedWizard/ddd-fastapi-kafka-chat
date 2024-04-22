from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Mapping

from fastapi import WebSocket


@dataclass
class BaseConnectionManager(ABC):
    connections_map: dict[str, list[WebSocket]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    async def accept_connection(self, websocket: WebSocket, key: str):
        ...

    @abstractmethod
    async def remove_connection(self, websocket: WebSocket, key: str):
        ...

    @abstractmethod
    async def send_all(self, key: str, bytes_: bytes):
        ...


@dataclass
class ConnectionManager(BaseConnectionManager):
    async def accept_connection(self, websocket: WebSocket, key: str):
        await websocket.accept()
        self.connections_map[key].append(websocket)

    async def remove_connection(self, websocket: WebSocket, key: str):
        # await websocket.close()
        self.connections_map[key].remove(websocket)

    async def send_all(self, key: str, bytes_: bytes):
        for websocket in self.connections_map[key]:
            # Тут был send_json раньше
            # send_json под капотом вызывает json.dumps, который нихуя не проглатывает UUID и datetime
            # заменил на send_bytes и взял готовый конвертер
            # TODO: этот момент отрефакторить, делаю как временное быстрое решение
            await websocket.send_bytes(bytes_)

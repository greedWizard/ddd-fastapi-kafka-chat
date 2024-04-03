from abc import ABC, abstractmethod
from dataclasses import dataclass

from domain.entities.messages import Chat, Message


@dataclass
class BaseChatsRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        ...

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        ...


@dataclass
class BaseMessagesRepository(ABC):
    @abstractmethod
    async def add_message(self, chat_oid: str, message: Message) -> None:
        ...

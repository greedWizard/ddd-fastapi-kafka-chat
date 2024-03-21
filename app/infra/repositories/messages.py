from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from domain.entities.messages import Chat


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    def check_chat_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    def add_chat(self, chat: Chat) -> None:
        ...


@dataclass
class MemoryChatRepository(ABC):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(next(
                chat for chat in self._saved_chats if chat.title == title
            ))
        except StopIteration:
            return False

    def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

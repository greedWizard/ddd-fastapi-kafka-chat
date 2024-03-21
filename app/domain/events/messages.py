from dataclasses import dataclass

from domain.events.base import BaseEvent


@dataclass
class NewMessageReceivedEvent(BaseEvent):
    message_text: str
    message_oid: str
    chat_oid: str


@dataclass
class NewChatCreated(BaseEvent):
    chat_oid: str
    chat_title: str

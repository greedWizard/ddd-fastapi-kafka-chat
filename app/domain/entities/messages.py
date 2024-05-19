from dataclasses import (
    dataclass,
    field,
)

from domain.entities.base import BaseEntity
from domain.events.messages import (
    ChatDeletedEvent,
    NewChatCreatedEvent,
    NewMessageReceivedEvent,
)
from domain.values.messages import (
    Text,
    Title,
)


@dataclass(eq=False)
class Message(BaseEntity):
    chat_oid: str
    text: Text


@dataclass(eq=False)
class Chat(BaseEntity):
    title: Title
    messages: set[Message] = field(default_factory=set, kw_only=True)
    is_deleted: bool = field(default=False, kw_only=True)

    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(NewChatCreatedEvent(chat_oid=new_chat.oid, chat_title=new_chat.title.as_generic_type()))

        return new_chat

    def add_message(self, message: Message):
        self.messages.add(message)
        self.register_event(
            NewMessageReceivedEvent(
                message_text=message.text.as_generic_type(),
                chat_oid=self.oid,
                message_oid=message.oid,
            ),
        )

    def delete(self):
        self.is_deleted = True
        self.register_event(ChatDeletedEvent(chat_oid=self.oid))

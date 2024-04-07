from abc import ABC
from dataclasses import dataclass

from motor.core import AgnosticClient

from domain.entities.messages import Chat, Message
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from infra.repositories.messages.converters import convert_chat_document_to_entity, convert_chat_entity_to_document, convert_message_to_document


@dataclass
class BaseMongoDBRepository(ABC):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    @property
    def _collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]


@dataclass
class MongoDBChatsRepository(BaseChatsRepository, BaseMongoDBRepository):
    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        chat_document = await self._collection.find_one(filter={'oid': oid})

        if not chat_document:
            return None

        return convert_chat_document_to_entity(chat_document)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return bool(await self._collection.find_one(filter={'title': title}))

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(convert_chat_entity_to_document(chat))


@dataclass
class MongoDBMessagesRepository(BaseMessagesRepository, BaseMongoDBRepository):
    async def add_message(self, chat_oid: str, message: Message) -> None:
        await self._collection.insert_one(
            document=convert_message_to_document(message),
        )
        await self._collection.update_one(
            filter={'oid': chat_oid},
            update={
                '$push': {
                    'messages': convert_message_to_document(message),
                },
            },
        )

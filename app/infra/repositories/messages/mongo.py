from dataclasses import dataclass

from motor.core import AgnosticClient

from domain.entities.messages import Chat
from infra.repositories.messages.base import BaseChatRepository
from infra.repositories.messages.converters import convert_chat_entity_to_document


@dataclass
class MongoDBChatRepository(BaseChatRepository):
    mongo_db_client: AgnosticClient
    mongo_db_db_name: str
    mongo_db_collection_name: str

    def _get_chat_collection(self):
        return self.mongo_db_client[self.mongo_db_db_name][self.mongo_db_collection_name]

    async def check_chat_exists_by_title(self, title: str) -> bool:
        collection = self._get_chat_collection()

        return bool(await collection.find_one(filter={'title': title}))

    async def add_chat(self, chat: Chat) -> None:
        collection = self._get_chat_collection()
        await collection.insert_one(convert_chat_entity_to_document(chat))

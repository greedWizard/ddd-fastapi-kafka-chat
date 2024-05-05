from dataclasses import dataclass


@dataclass
class GetMessagesFilters:
    limit: int = 10
    offset: int = 0


@dataclass
class GetAllChatsFilters:
    limit: int = 10
    offset: int = 0

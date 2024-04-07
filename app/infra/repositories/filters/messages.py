from dataclasses import dataclass


@dataclass
class GetMessagesFilters:
    limit: int = 10
    offset: int = 0

from dataclasses import dataclass

from domain.values.messages import Text


@dataclass
class Message:
    oid: str
    text: Text

from abc import ABC
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from domain.events.base import BaseEvent


ET = TypeVar('ET', bound=BaseEvent)
ER = TypeVar('ER', bound=Any)


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    def handle(self, event: ET) -> ER:
        ...

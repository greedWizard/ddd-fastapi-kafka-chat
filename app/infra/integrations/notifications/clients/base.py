from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from infra.integrations.notifications.dots import Notification


@dataclass
class BaseNotificationClient(ABC):
    @abstractmethod
    async def _format_notification(self, notification: Notification) -> str:
        ...

    @abstractmethod
    async def send(self, notification: Notification):
        ...

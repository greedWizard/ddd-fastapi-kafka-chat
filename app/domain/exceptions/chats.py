from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class ListenerAlreadyExistsException(ApplicationException):
    listener_oid: str

    @property
    def message(self):
        return 'Listener already listens this chat.'

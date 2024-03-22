from functools import lru_cache
from punq import Container, Scope

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from logic.mediator import Mediator


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(BaseChatRepository, MemoryChatRepository, scope=Scope.singleton)
    container.register(CreateChatCommandHandler)

    def init_mediator():
        mediator = Mediator()
        mediator.register_command(
            CreateChatCommand,
            [container.resolve(CreateChatCommandHandler)],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container

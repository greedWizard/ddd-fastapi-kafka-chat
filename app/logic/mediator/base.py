from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field

from domain.events.base import BaseEvent
from logic.commands.base import CR, CT, BaseCommand, CommandHandler
from logic.events.base import ER, ET, EventHandler
from logic.exceptions.mediator import CommandHandlersNotRegisteredException, EventHandlersNotRegisteredException
from logic.mediator.command import CommandMediator
from logic.mediator.converters import convert_event_to_broker_message
from logic.mediator.event import EventMediator
from logic.mediator.query import QueryMediator
from logic.queries.base import QR, QT, BaseQuery, BaseQueryHandler


@dataclass(eq=False)
class Mediator(EventMediator, QueryMediator, CommandMediator):
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event].append(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]):
        self.events_map[command].extend(command_handlers)

    def register_query(self, query: QT, query_handler: BaseQueryHandler[QT, QR]) -> QR:
        self.queries_map[query] = query_handler

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            handlers: Iterable[EventHandler] = self.events_map[event.__class__]

            for handler in handlers:
                result.append(await handler.handle(event=event))

            result.extend([await handler.handle(event) for handler in handlers])

        await self.message_broker.send_message()

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.events_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)

        return [await handler.handle(command) for handler in handlers]

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.queries_map[query.__class__].handle(query=query)

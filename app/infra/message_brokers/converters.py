import orjson

from domain.events.base import BaseEvent


def convert_event_to_broker_message(event: BaseEvent) -> bytes:
    return orjson.dumps(event)

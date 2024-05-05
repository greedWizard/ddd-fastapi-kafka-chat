from dataclasses import dataclass


@dataclass(frozen=True)
class Notification:
    # TODO: user_id
    title: str
    text: str

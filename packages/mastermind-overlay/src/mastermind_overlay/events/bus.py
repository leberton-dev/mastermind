from collections.abc import Callable
from typing import Any, TypeVar


E = TypeVar("E")

class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable[[Any], None]]] = {}


    def subscribe(self, event_type: type[E], handler: Callable[[E], None]) -> None:
        self._handlers.setdefault(event_type, []).append(handler)


    def publish(self, event: object) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)


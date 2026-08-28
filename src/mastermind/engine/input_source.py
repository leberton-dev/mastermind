from typing import Protocol

from mastermind.engine.input_event import InputEvent


class InputSource(Protocol):
    def next_event(self) -> InputEvent | None: ...

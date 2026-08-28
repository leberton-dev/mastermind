from typing import Protocol

from mastermind_shell.engine.input_event import InputEvent


class InputSource(Protocol):
    def next_event(self) -> InputEvent | None: ...

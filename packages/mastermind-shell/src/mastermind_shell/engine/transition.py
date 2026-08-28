from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from mastermind_shell.engine.screen import Screen


class TransitionKind(Enum):
    PUSH = 1
    POP = 2
    QUIT = 3


class ScreenTransition(NamedTuple):
    kind: TransitionKind
    screen: Screen | None = None


    @classmethod
    def push(cls, screen: Screen) -> ScreenTransition:
        return cls(TransitionKind.PUSH, screen)


    @classmethod
    def pop(cls) -> ScreenTransition:
        return cls(TransitionKind.POP)


    @classmethod
    def quit(cls) -> ScreenTransition:
        return cls(TransitionKind.QUIT)

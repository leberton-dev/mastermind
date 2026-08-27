from __future__ import annotations

from abc import ABC, abstractmethod
import curses
from enum import Enum
from typing import NamedTuple


class Screen(ABC):
    def __init__(self, stdscr: curses.window, queue: ScreenQueue, opaque: bool = True) -> None:
        self._stdscr: curses.window = stdscr
        self._queue: ScreenQueue = queue
        self._opaque: bool = opaque


    @property
    def opaque(self) -> bool:
        return self._opaque


    @abstractmethod
    def handle_input(self, key: int) -> None: ...
    @abstractmethod
    def update(self) -> None: ...
    @abstractmethod
    def render(self) -> None: ...

    def on_enter(self) -> None: ...
    def on_exit(self) -> None: ...


class TransitionKind(Enum):
    PUSH = 1
    POP = 2
    QUIT = 3


class ScreenTransition(NamedTuple):
    kind: TransitionKind
    screen: "Screen | None" = None


    @classmethod
    def push(cls, screen: "Screen") -> "ScreenTransition":
        return cls(TransitionKind.PUSH, screen)


    @classmethod
    def pop(cls) -> "ScreenTransition":
        return cls(TransitionKind.POP)


    @classmethod
    def quit(cls) -> "ScreenTransition":
        return cls(TransitionKind.QUIT)


class ScreenQueue:
    def __init__(self) -> None:
        self._pending: list[ScreenTransition] = []


    def push(self, transition: ScreenTransition) -> None:
        self._pending.append(transition)


    def drain(self) -> list[ScreenTransition]:
        pending = self._pending
        self._pending = []
        return pending


class ScreenStack:
    def __init__(self, stdscr: curses.window, queue: ScreenQueue, initial: Screen) -> None:
        self._stdscr: curses.window = stdscr
        self._queue: ScreenQueue = queue
        self._screens: list[Screen] = [initial]
        self._running: bool = True


    @property
    def top(self) -> Screen:
        return self._screens[-1]


    def push(self, screen: Screen) -> None:
        self._screens.append(screen)
        self.top.on_enter()


    def pop(self) -> None:
        self.top.on_exit()
        self._screens.remove(self.top)


    def render(self) -> None:
        first_no_opaque_idx = 0

        for i, screen in enumerate(reversed(self._screens)):
            if screen.opaque:
                first_no_opaque_idx = len(self._screens) - i - 1
                break

        for i in range(first_no_opaque_idx, len(self._screens)):
            self._screens[i].render()


    def step(self) -> bool:
        self.render()
        key = self._stdscr.getch()
        self.top.handle_input(key)
        self.top.update()

        for transition in self._queue.drain():
            match transition.kind:
                case TransitionKind.PUSH:
                    assert transition.screen is not None
                    self.push(transition.screen)
                case TransitionKind.POP:
                    self.pop()
                case TransitionKind.QUIT:
                    self._running = False

        return self._running


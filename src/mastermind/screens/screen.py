from abc import ABC, abstractmethod
import curses

from mastermind.screens.queue import ScreenQueue


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


import curses
from typing import override

from mastermind.screens.screen import Screen
from mastermind.screens.queue import ScreenQueue


class GameOverScreen(Screen):
    def __init__(self, stdscr: curses.window, queue: ScreenQueue, opaque: bool = False) -> None:
        super().__init__(stdscr, queue, opaque)


    @override
    def handle_input(self, key: int) -> None:
        pass


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        pass

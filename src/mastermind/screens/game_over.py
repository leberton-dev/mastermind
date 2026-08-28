import curses
from typing import override

from mastermind.core.screen_manager import Screen, ScreenQueue, ScreenTransition
from mastermind.ui.renderer import Renderer
from mastermind.core.gamestate import GameState


class GameOverScreen(Screen):
    def __init__(self, stdscr: curses.window, queue: ScreenQueue, renderer: Renderer, state: GameState) -> None:
        super().__init__(stdscr, queue, False)
        self._renderer: Renderer = renderer
        self._state: GameState = state


    @override
    def handle_input(self, key: int) -> None:
        self._queue.push(ScreenTransition.pop())
        if not self._state.won:
            self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        if self._state.won:
            self._renderer.win()
        else:
            self._renderer.loose(f"Correct was {[c.name for c in self._state.secret_code]}")

from typing import override

from mastermind.core.gamestate import GameState
from mastermind.core.run import RunState
from mastermind.engine.input_event import InputEvent
from mastermind.engine.renderer import Renderer
from mastermind.engine.screen import Screen
from mastermind.engine.screen_queue import ScreenQueue
from mastermind.engine.transition import ScreenTransition
from mastermind.screens.shop import ShopScreen


class GameOverScreen(Screen):
    def __init__(self, queue: ScreenQueue, renderer: Renderer, state: GameState, run_state: RunState, next_state: GameState | None) -> None:
        super().__init__(queue, False)
        self._renderer: Renderer = renderer
        self._state: GameState = state
        self._run_state: RunState = run_state
        self._next_state: GameState | None = next_state


    @override
    def handle_input(self, event: InputEvent) -> None:
        self._queue.push(ScreenTransition.pop())
        if self._state.won:
            assert self._next_state is not None
            self._queue.push(ScreenTransition.push(ShopScreen(self._queue, self._renderer, self._run_state, self._next_state)))
        else:
            self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        if self._state.won:
            self._renderer.render_win(f"You found {[c.name for c in self._state.secret_code]}")
        else:
            self._renderer.render_loose(f"Correct was {[c.name for c in self._state.secret_code]}")

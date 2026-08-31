from typing import override

from mastermind_overlay.run.gamestate import GameState
from mastermind_overlay.run.run_state import RunState

from mastermind_shell.engine.input_event import InputEvent
from mastermind_shell.engine.renderer import Renderer
from mastermind_shell.engine.screen import Screen
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.transition import ScreenTransition
from mastermind_shell.screens.shop import ShopScreen


class GameOverScreen(Screen):
    def __init__(self, queue: ScreenQueue, renderer: Renderer, state: GameState, run_state: RunState, next_state: GameState | None) -> None:
        super().__init__(queue, False)
        self._renderer: Renderer = renderer
        self._game_state: GameState = state
        self._run_state: RunState = run_state
        self._next_state: GameState | None = next_state


    @override
    def handle_input(self, event: InputEvent) -> None:
        self._queue.push(ScreenTransition.pop())
        if self._run_state.run_over:
            self._queue.push(ScreenTransition.pop())
            return
        if self._game_state.won:
            assert self._next_state is not None
            self._queue.push(ScreenTransition.push(ShopScreen(self._queue, self._renderer, self._run_state, self._next_state)))
        else:
            self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        if self._run_state.run_over:
            self._renderer.render_run_over()
        elif self._game_state.won:
            self._renderer.render_win(f"You found {[c.name for c in self._game_state.secret_code]}")
        else:
            self._renderer.render_loose(f"Correct was {[c.name for c in self._game_state.secret_code]}")

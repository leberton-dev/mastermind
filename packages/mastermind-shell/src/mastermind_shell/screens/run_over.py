from typing import override

from mastermind_overlay.run.gamestate import GameState
from mastermind_overlay.run.run_state import RunState

from mastermind_shell.engine.input_event import InputEvent
from mastermind_shell.engine.renderer import Renderer
from mastermind_shell.engine.screen import Screen
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.transition import ScreenTransition
from mastermind_shell.screens.shop import ShopScreen


class RunOverScreen(Screen):
    def __init__(self, queue: ScreenQueue, renderer: Renderer, state: GameState, run_state: RunState, next_state: GameState | None) -> None:
        super().__init__(queue, False)
        self._renderer: Renderer = renderer
        self._game_state: GameState = state
        self._run_state: RunState = run_state
        self._next_state: GameState | None = next_state
        self._cursor_idx: int = 0


    @override
    def handle_input(self, event: InputEvent) -> None:
        if event == InputEvent.RIGHT or event == InputEvent.LEFT:
            self._cursor_idx = 1 if self._cursor_idx == 0 else 0
        if event == InputEvent.CONFIRM:
            if self._cursor_idx == 0:
                self._run_state.set_max_stages(1000)
                self._queue.push(ScreenTransition.pop())
                self._queue.push(ScreenTransition.push(ShopScreen(self._queue, self._renderer, self._run_state, self._next_state)))
            else:
                self._queue.push(ScreenTransition.pop())
                self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        self._renderer.render_run_over(self._cursor_idx)

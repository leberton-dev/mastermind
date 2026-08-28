from typing import override

from mastermind.core.gamestate import GameState
from mastermind.core.run import RunState
from mastermind.engine.input_event import InputEvent
from mastermind.engine.renderer import Renderer
from mastermind.engine.screen import Screen
from mastermind.engine.screen_queue import ScreenQueue
from mastermind.engine.transition import ScreenTransition
from mastermind.screens.game_over import GameOverScreen


class GameplayScreen(Screen):
    def __init__(self, queue: ScreenQueue, renderer: Renderer, run_state: RunState) -> None:
        super().__init__(queue, True)
        self._state: GameState = run_state.new_round()
        self._renderer: Renderer = renderer
        self._run_state: RunState = run_state


    @override
    def handle_input(self, event: InputEvent) -> None:
        if event == InputEvent.UP:
            self._cycle_color_up()
        if event == InputEvent.DOWN:
            self._cycle_color_down()
        if event == InputEvent.LEFT:
            self._move_left()
        if event == InputEvent.RIGHT:
            self._move_right()
        if event == InputEvent.CONFIRM:
            self._submit_guess()
        if event == InputEvent.QUIT:
            self._quit()


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        self._renderer.render_gameplay(self._state, self._run_state.ante, self._run_state.relics)


    def _cycle_color_up(self) -> None:
        self._state.cycle_color(-1)

    def _cycle_color_down(self) -> None:
        self._state.cycle_color(1)

    def _move_left(self) -> None:
        self._state.cycle_current_square(-1)

    def _move_right(self) -> None:
        self._state.cycle_current_square(1)

    def _quit(self) -> None:
        self._queue.push(ScreenTransition.pop())

    def _submit_guess(self) -> None:
        self._state.submit_guess()

        if self._state.game_over:
            if self._state.won:
                game_over = GameOverScreen(self._queue, self._renderer, self._state)
                self._queue.push(ScreenTransition.push(game_over))
                self._run_state.reward_round(self._state)
                self._run_state.advance_ante()
                self._state = self._run_state.new_round()

            if self._state.lost:
                game_over = GameOverScreen(self._queue, self._renderer, self._state)
                self._queue.push(ScreenTransition.push(game_over))

        self._state.reset_current_guess()

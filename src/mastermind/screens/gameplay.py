import curses
from typing import override

from mastermind.core.screen_manager import Screen, ScreenQueue, ScreenTransition
from mastermind.core.gamestate import GameState
from mastermind.screens.game_over import GameOverScreen
from mastermind.ui.renderer import Renderer
from mastermind.core.run import RunState


class GameplayScreen(Screen):
    def __init__(self, stdscr: curses.window, queue: ScreenQueue, run_state: RunState) -> None:
        super().__init__(stdscr, queue, True)
        self._state: GameState = run_state.new_round()
        self._renderer: Renderer = Renderer(stdscr)
        self._run_state: RunState = run_state


    @override
    def handle_input(self, key: int) -> None:
        if key == curses.KEY_UP:
            self._cycle_color_up()
        if key == curses.KEY_DOWN:
            self._cycle_color_down()
        if key == curses.KEY_LEFT:
            self._move_left()
        if key == curses.KEY_RIGHT:
            self._move_right()
        if key == curses.KEY_ENTER or key == ord('\n') or key == ord('\r'):
            self._submit_guess()
        if key == ord('q'):
            self._quit()


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        self._renderer.render(self._state, self._run_state.ante, self._run_state.relics)


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
                game_over = GameOverScreen(self._stdscr, self._queue, self._renderer, self._state)
                self._queue.push(ScreenTransition.push(game_over))
                self._run_state.advance_ante()
                self._state = self._run_state.new_round()

            if self._state.lost:
                game_over = GameOverScreen(self._stdscr, self._queue, self._renderer, self._state)
                self._queue.push(ScreenTransition.push(game_over))

        self._state.reset_current_guess()


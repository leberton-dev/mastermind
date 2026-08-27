from abc import ABC, abstractmethod
import curses
from curses import wrapper
from typing import Callable, override

from mastermind import ui
from mastermind.ui import Renderer
from mastermind.gamestate import GameState

def _init_curses(stdscr: curses.window) -> None:
    _ = curses.curs_set(0)
    stdscr.keypad(True)

    curses.cbreak()
    curses.noecho()
    curses.start_color()
    if not curses.has_colors():
        raise Exception("Terminal does not have colors")
    ui.palette.init_color_pairs()

class Action(ABC):
    def __init__(self, stdscr: curses.window, state: GameState, renderer: Renderer) -> None:
        self._stdscr: curses.window = stdscr
        self._state: GameState = state
        self._renderer: Renderer = renderer

    @abstractmethod
    def act(self) -> bool:
        pass

class CycleColorUp(Action):
    def __init__(self, stdscr: curses.window, state: GameState, renderer: Renderer) -> None:
        super().__init__(stdscr, state, renderer)

    @override
    def act(self) -> bool:
        self._state.cycle_color(-1)
        return True

class CycleColorDown(Action):
    def __init__(self, stdscr: curses.window, state: GameState, renderer: Renderer) -> None:
        super().__init__(stdscr, state, renderer)

    @override
    def act(self) -> bool:
        self._state.cycle_color(1)
        return True

def _move_left(stdscr: curses.window, state: GameState, renderer: Renderer) -> bool:
    state.cycle_current_square(-1)
    return True

def _move_right(stdscr: curses.window, state: GameState, renderer: Renderer) -> bool:
    state.cycle_current_square(1)
    return True

def _quit(stdscr: curses.window, state: GameState, renderer: Renderer) -> bool:
    return False

def _submit_guess(stdscr: curses.window, state: GameState, renderer: Renderer) -> bool:
    state.submit_guess()

    if state.won:
        renderer.win()
        _ = stdscr.getch()
        return False

    if state.lost:
        renderer.loose(f"Correct was : {[c for c in state.secret_code]}")
        _ = stdscr.getch()
        return False

    state.reset_current_guess()

    return True


_KEY_ACTIONS: dict[int, Callable[[curses.window, GameState, Renderer], bool]] = {
    curses.KEY_UP: _cycle_color_up,
    curses.KEY_DOWN: _cycle_color_down,
    curses.KEY_LEFT: _move_left,
    curses.KEY_RIGHT: _move_right,
    curses.KEY_ENTER: _submit_guess,
    ord('\n'): _submit_guess,
    ord('\r'): _submit_guess,
    ord('q'): _quit
}

def _handle_input(stdscr: curses.window, state: GameState, renderer: Renderer) -> bool:
    key = stdscr.getch()
    action = _KEY_ACTIONS.get(key)
    if action is None:
        return True
    return action(stdscr, state, renderer)


def main(stdscr: curses.window):
    _init_curses(stdscr)

    state = GameState()
    renderer = Renderer(stdscr)

    while True:
        renderer.render(state)
        if not _handle_input(stdscr, state, renderer):
            break


if __name__ == "__main__":
    wrapper(main)

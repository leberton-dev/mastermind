import curses
from curses import wrapper

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

def main(stdscr: curses.window):
    _init_curses(stdscr)

    state = GameState()
    renderer = Renderer(stdscr)

    while True:

        renderer.render(state)

        key = stdscr.getch()
        if key == curses.KEY_UP:
            state.cycle_color(-1)
        if key == curses.KEY_DOWN:
            state.cycle_color(1)
        if key == curses.KEY_LEFT:
            state.cycle_current_square(-1)
        if key == curses.KEY_RIGHT:
            state.cycle_current_square(1)

        if key in (curses.KEY_ENTER, ord('\n'), ord('\r')):

            state.submit_guess()

            if state.won:
                renderer.win()
                _ = stdscr.getch()
                break

            if state.lost:
                renderer.loose(f"Correct was : {[c for c in state.secret_code]}")
                _ = stdscr.getch()
                break

            state.reset_current_guess()

        if key == ord('q'):
            break


if __name__ == "__main__":
    wrapper(main)

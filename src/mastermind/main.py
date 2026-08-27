import curses
from curses import wrapper

from mastermind import ui
from mastermind.gamestate import GameState

_WIN_STR = "You won"
_LOOSE_STR = "You lost"

def _init_curses(stdscr: curses.window) -> None:
    _ = curses.curs_set(0)
    stdscr.keypad(True)

    curses.cbreak()
    curses.noecho()
    curses.start_color()
    if not curses.has_colors():
        raise Exception("Terminal does not have colors")

def main(stdscr: curses.window):
    _init_curses(stdscr)
    ui.palette.init_color_pairs()

    state = GameState()
    while True:
        stdscr.clear()
        stdscr.addstr(1, (curses.COLS - len("Welcome to Mastermind")) // 2, "Welcome to Mastermind", curses.A_STANDOUT)
        ui.board.draw_guessed_squares(stdscr, state.guessed_squares, state.guessed_feedback)
        ui.board.draw_guess_squares(stdscr, state.current_square, state.guess_squares)
        stdscr.refresh()

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
                stdscr.addstr(curses.LINES // 2, (curses.COLS + len(_WIN_STR)) // 2, _WIN_STR, curses.A_STANDOUT)
                _ = stdscr.getch()
                break

            if state.lost:
                correct_guess_str = f"Correct was : {[c for c in state.secret_code]}"
                stdscr.addstr(curses.LINES // 2, (curses.COLS + len(_LOOSE_STR)) // 2, _LOOSE_STR, curses.A_STANDOUT)
                stdscr.addstr(curses.LINES // 2, (curses.COLS + len(correct_guess_str)) // 2, correct_guess_str, curses.A_STANDOUT)
                _ = stdscr.getch()
                break

            state.reset_current_guess()

        if key == ord('q'):
            break


if __name__ == "__main__":
    wrapper(main)

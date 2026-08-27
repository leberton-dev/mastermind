
import curses
from curses.textpad import rectangle

from mastermind.core.feedback import Feedback
from mastermind.core.code import Code
from mastermind.ui import palette


_BOTTOM_PADDING = 1

def _fill_rectangle(stdscr: curses.window, y_start: int, y_end: int, x_start: int, x_end: int, attr: int) -> None:
    for y in range(y_start, y_end):
        stdscr.chgat(y, x_start, x_end, attr)


def draw_guess_squares(stdscr: curses.window, square_idx: int, guess_squares: Code) -> None:
    square_width = 7
    square_height = 3
    y_pos = curses.LINES - square_height - _BOTTOM_PADDING
    x_pos = (curses.COLS - (square_width*4)) // 2

    for i, sq in enumerate(guess_squares):
        attr = palette.to_curses_pair(sq)
        border_attr = curses.color_pair(7) if i == square_idx else curses.A_NORMAL

        stdscr.attron(border_attr)
        rectangle(stdscr, y_pos, x_pos, y_pos + square_height, x_pos + square_width)
        stdscr.attroff(border_attr)

        _fill_rectangle(stdscr, y_pos + 1, y_pos + square_height, x_pos + 1, square_width - 1, attr)
        x_pos += square_width + 1


def draw_guessed_squares(stdscr: curses.window, guessed_squares: list[Code], guessed_feedback: list[Feedback]) -> None:
    if len(guessed_squares) == 0:
        return

    square_height = curses.LINES // 16
    square_width = square_height * 2
    y_pos = 2
    x_start = (curses.COLS - (square_width*4)) // 2

    for idx, guess in enumerate(guessed_squares):
        x_pos = x_start
        stdscr.addstr(y_pos, x_pos - 5, f"{guessed_feedback[idx].black}")
        for sq in guess:
            attr = palette.to_curses_pair(sq)
            rectangle(stdscr, y_pos, x_pos, y_pos + square_height, x_pos + square_width)
            _fill_rectangle(stdscr, y_pos + 1, y_pos + square_height, x_pos + 1, square_width - 1, attr)
            x_pos += square_width + 1
        stdscr.addstr(y_pos, x_pos + 5, f"{guessed_feedback[idx].white}")
        y_pos += square_height + 1

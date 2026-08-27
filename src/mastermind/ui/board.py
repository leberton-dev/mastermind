
import curses
from curses.textpad import rectangle

from mastermind.core.colors import Color
from mastermind.ui import palette


_BOTTOM_PADDING = 5

def switch_guess_color(square_idx: int, direction: int, guess_squares: list[Color]) -> None:
    idx = (guess_squares[square_idx].value - 1 + direction) % len(Color)
    guess_squares[square_idx] = Color(idx + 1)


def _fill_rectangle(stdscr: curses.window, y_start: int, y_end: int, x_start: int, x_end: int, attr: int) -> None:
    for y in range(y_start, y_end):
        stdscr.chgat(y, x_start, x_end, attr)


def draw_guess_squares(stdscr: curses.window, square_idx: int, guess_squares: list[Color]) -> None:
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


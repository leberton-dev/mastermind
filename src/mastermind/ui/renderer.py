import curses
from curses.textpad import rectangle

from mastermind.ui import palette
from mastermind.core.code import Code
from mastermind.gamestate import GameState

from mastermind.core.feedback import CodeFeedback

class Renderer:
    _BOTTOM_PADDING: int = 1
    _WIN_STR: str = "You won"
    _LOOSE_STR: str = "You lost"


    def __init__(self, stdscr: curses.window) -> None:
        self._stdscr: curses.window = stdscr


    def render(self, state: GameState) -> None:
        self._stdscr.clear()
        self._stdscr.addstr(1, (curses.COLS - len("Welcome to Mastermind")) // 2, "Welcome to Mastermind", curses.A_STANDOUT)
        self._draw_guessed_squares(state.guessed_squares, state.guessed_feedback)
        self._draw_guess_squares(state.current_square, state.guess_squares)
        self._render_commands()
        self._stdscr.refresh()


    def _render_commands(self) -> None:
        self._stdscr.addstr(curses.LINES-3, 1, "LEFT/RIGHT: switch box")
        self._stdscr.addstr(curses.LINES-2, 1, "TOP/DOWN: cycle trough colors")
        self._stdscr.addstr(curses.LINES-1, 1, "ENTER: submit colors")

    def win(self) -> None:
        self._stdscr.addstr(
            curses.LINES // 2,
            (curses.COLS + len(self._WIN_STR)) // 2,
            self._WIN_STR,
            curses.A_STANDOUT)

    def loose(self, correct_guess_str: str) -> None:
        self._stdscr.addstr(
            curses.LINES // 2,
            (curses.COLS - len(self._LOOSE_STR)) // 2,
            self._LOOSE_STR,
            curses.A_STANDOUT)
        self._stdscr.addstr(
            curses.LINES // 2 + 1,
            (curses.COLS - len(correct_guess_str)) // 2,
            correct_guess_str,
            curses.A_STANDOUT)


    def _fill_rectangle(self, y_start: int, y_end: int, x_start: int, x_end: int, attr: int) -> None:
        for y in range(y_start, y_end):
            self._stdscr.chgat(y, x_start, x_end, attr)


    def _draw_guess_squares(self, square_idx: int, guess_squares: Code) -> None:
        square_width = 7
        square_height = 3
        y_pos = curses.LINES - square_height - self._BOTTOM_PADDING
        x_pos = (curses.COLS - (square_width*4) - 4) // 2

        for i, sq in enumerate(guess_squares):
            attr = palette.to_curses_pair(sq)
            border_attr = curses.color_pair(7) if i == square_idx else curses.A_NORMAL

            self._stdscr.attron(border_attr)
            rectangle(self._stdscr, y_pos, x_pos, y_pos + square_height, x_pos + square_width)
            self._stdscr.attroff(border_attr)

            self._fill_rectangle(y_pos + 1, y_pos + square_height, x_pos + 1, square_width - 1, attr)
            x_pos += square_width + 1


    def _draw_guessed_squares(self, guessed_squares: list[Code], guessed_feedback: list[CodeFeedback]) -> None:
        if len(guessed_squares) == 0:
            return

        square_height = curses.LINES // 16
        square_width = square_height * 2
        y_pos = 2
        x_start = (curses.COLS - (square_width*4) - 4) // 2

        for idx, guess in enumerate(guessed_squares):
            x_pos = x_start
            self._stdscr.addstr(y_pos, x_pos - 5, f"{guessed_feedback[idx].black_pegs}")
            for sq in guess:
                attr = palette.to_curses_pair(sq)
                rectangle(self._stdscr, y_pos, x_pos, y_pos + square_height, x_pos + square_width)
                self._fill_rectangle(y_pos + 1, y_pos + square_height, x_pos + 1, square_width - 1, attr)
                x_pos += square_width + 1
            self._stdscr.addstr(y_pos, x_pos + 5, f"{guessed_feedback[idx].white_pegs}")
            y_pos += square_height + 1

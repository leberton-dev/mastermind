import curses
from curses.textpad import rectangle

from mastermind.curses_backend import palette
from mastermind.core.code import Code
from mastermind.core.gamestate import GameState
from mastermind.core.relic import Relic
from mastermind.core.feedback import CodeFeedback


class CursesRenderer:
    _BOTTOM_PADDING: int = 1
    _WIN_STR: str = "You won, let's go to the next round."
    _LOOSE_STR: str = "You lost, you must restart haha..."


    def __init__(self, stdscr: curses.window) -> None:
        self._stdscr: curses.window = stdscr


    def dimensions(self) -> tuple[int, int]:
        return curses.LINES, curses.COLS


    def clear(self) -> None:
        self._stdscr.clear()


    def refresh(self) -> None:
        self._stdscr.refresh()


    def draw_text(self, y: int, x: int, text: str, highlighted: bool = False) -> None:
        attr = curses.A_STANDOUT if highlighted else curses.A_NORMAL
        self._stdscr.addstr(y, x, text, attr)


    def render_gameplay(self, state: GameState, ante: int, relics: list[Relic]) -> None:
        self._stdscr.clear()
        self._stdscr.addstr(1, (curses.COLS - len("Welcome to Mastermind")) // 2, "Welcome to Mastermind", curses.A_STANDOUT)
        self._draw_guessed_squares(state.guessed_codes, state.guessed_feedback)
        self._draw_guess_squares(state.current_peg, state.current_code)
        self._render_commands()
        self._render_score_hud(ante, state.score, state.target_score, state.turns_left)
        self._render_relics(relics)
        self._stdscr.refresh()


    def _render_commands(self) -> None:
        self._stdscr.addstr(curses.LINES-3, 1, "LEFT/RIGHT: switch box")
        self._stdscr.addstr(curses.LINES-2, 1, "TOP/DOWN: cycle trough colors")
        self._stdscr.addstr(curses.LINES-1, 1, "ENTER: submit colors")

    def render_win(self, correct_guess_str: str) -> None:
        self._stdscr.addstr(
            curses.LINES // 2,
            (curses.COLS + len(self._WIN_STR)) // 2,
            self._WIN_STR,
            curses.A_STANDOUT)
        self._stdscr.addstr(
            curses.LINES // 2 + 1,
            (curses.COLS - len(correct_guess_str)) // 2,
            correct_guess_str,
            curses.A_STANDOUT)

    def render_loose(self, correct_guess_str: str) -> None:
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


    def _render_score_hud(self, ante: int, score: int, target: int, turns_left: int) -> None:
        ante_str = f"ANTE   : {ante}"
        score_str = f"SCORE  : {score}"
        target_str = f"TARGET : {target}"
        turns_str = f"TURNS  : {turns_left}"
        strs = [ante_str, score_str, target_str, turns_str]
        max_len = max(len(s) for s in strs)
        x = curses.COLS - max_len - 1
        y = 1

        for s in strs:
            self._stdscr.addstr(y, x, s)
            y += 1

    def _render_relics(self, relics: list[Relic]) -> None:
        x = 0
        y = 0
        for relic in relics:
            self._stdscr.addstr(y, x, str(relic))
            y += 1


    def render_shop(self, currency: int, offer: list[Relic], price: int, extra_guess_price: int, selected: int) -> None:
        self._stdscr.clear()
        self._stdscr.addstr(1, (curses.COLS - len("SHOP")) // 2, "SHOP", curses.A_STANDOUT)
        self._stdscr.addstr(3, 1, f"Currency: {currency}")

        y = 5
        for i, relic in enumerate(offer):
            attr = curses.A_STANDOUT if i == selected else curses.A_NORMAL
            self._stdscr.addstr(y, 1, f"{str(relic)} - {price}", attr)
            y += 1

        extra_guess_idx = len(offer)
        attr = curses.A_STANDOUT if selected == extra_guess_idx else curses.A_NORMAL
        self._stdscr.addstr(y + 1, 1, f"Extra guess - {extra_guess_price}", attr)
        y += 1

        leave_idx = extra_guess_idx + 1
        attr = curses.A_STANDOUT if selected == leave_idx else curses.A_NORMAL
        self._stdscr.addstr(y + 1, 1, "Leave Shop", attr)

        self._stdscr.addstr(curses.LINES - 1, 1, "UP/DOWN: select   ENTER: buy/leave")
        self._stdscr.refresh()

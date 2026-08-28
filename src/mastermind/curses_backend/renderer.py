import curses
import textwrap
from curses.textpad import rectangle

from mastermind.core.code import Code
from mastermind.core.feedback import CodeFeedback
from mastermind.core.gamestate import GameState
from mastermind.core.relic import Relic
from mastermind.curses_backend import palette


class CursesRenderer:
    _BOTTOM_PADDING: int = 1
    _WIN_STR: str = "You won, let's go to the next round."
    _LOOSE_STR: str = "You lost, you must restart haha..."
    _PANEL_WIDTH: int = 22


    def __init__(self, stdscr: curses.window) -> None:
        self._stdscr: curses.window = stdscr


    def _draw_frame(self) -> None:
        rectangle(self._stdscr, 0, 0, curses.LINES - 2, curses.COLS - 2)
        for y in range(1, curses.LINES - 2):
            self._stdscr.addch(y, self._PANEL_WIDTH, curses.ACS_VLINE)
        self._stdscr.addch(0, self._PANEL_WIDTH, curses.ACS_TTEE)
        self._stdscr.addch(curses.LINES - 2, self._PANEL_WIDTH, curses.ACS_BTEE)


    def dimensions(self) -> tuple[int, int]:
        return curses.LINES, curses.COLS


    def clear(self) -> None:
        self._stdscr.clear()


    def refresh(self) -> None:
        self._stdscr.refresh()


    def draw_text(self, y: int, x: int, text: str, highlighted: bool = False) -> None:
        attr = curses.A_STANDOUT if highlighted else curses.A_NORMAL
        self._stdscr.addstr(y, x, text, attr)


    def render_gameplay(self, state: GameState, ante: int, blind_label: str, relics: list[Relic]) -> None:
        self._stdscr.clear()
        self._draw_frame()
        self._render_left_panel(ante, state.score, state.target_score, state.turns_left, blind_label, relics)
        self._draw_guessed_squares(state.guessed_codes, state.guessed_feedback)
        self._draw_guess_squares(state.current_peg, state.current_code)
        self._render_commands()
        self._stdscr.refresh()


    def _render_commands(self) -> None:
        y = curses.LINES - 3
        self._stdscr.addstr(y, self._PANEL_WIDTH + 2, "LEFT/RIGHT: box    UP/DOWN: color    ENTER: submit")

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
        y_pos = curses.LINES - square_height - self._BOTTOM_PADDING - 3
        board_width = curses.COLS - self._PANEL_WIDTH
        x_pos = self._PANEL_WIDTH + (board_width - (square_width * 4) - 4) // 2

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
        board_width = curses.COLS - self._PANEL_WIDTH
        x_start = self._PANEL_WIDTH + (board_width - (square_width * 4) - 4) // 2

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


    def _render_left_panel(self, ante: int, score: int, target: int, turns_left: int, blind_label: str, relics: list[Relic]) -> None:
        x = 2
        y = 1
        for line in (
            f"ANTE   : {ante}",
            f"BLIND  : {blind_label}",
            f"SCORE  : {score}",
            f"TARGET : {target}",
            f"TURNS  : {turns_left}",
            ):
            self._stdscr.addstr(y, x, line)
            y += 1

        y += 1
        self._stdscr.addch(y, 0, curses.ACS_LTEE)
        self._stdscr.hline(y, 1, curses.ACS_HLINE, self._PANEL_WIDTH - 1)
        self._stdscr.addch(y, self._PANEL_WIDTH, curses.ACS_RTEE)
        y += 1

        self._stdscr.addstr(y, x, "RELICS")
        y += 1
        for relic in relics:
            self._stdscr.addstr(y, x, str(relic))
            y += 1


    def render_shop(self, currency: int, offer: list[Relic], extra_guess_price: int, selected: int) -> None:
        self._stdscr.clear()
        rectangle(self._stdscr, 0, 0, curses.LINES - 2, curses.COLS - 2)

        title = "SHOP"
        self._stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD | curses.A_STANDOUT)
        self._stdscr.addstr(1, 2, f"$ {currency}")

        items = [(str(relic), relic.description, relic.price) for relic in offer] + [("Extra guess", "Gain an extra guess this blind", extra_guess_price)]
        self._draw_shop_cards(items, selected)

        leave_idx = len(items)
        leave_str = "[ Leave Shop ]"
        attr = curses.A_STANDOUT if selected == leave_idx else curses.A_NORMAL
        self._stdscr.addstr(curses.LINES - 4, (curses.COLS - len(leave_str)) // 2, leave_str, attr)

        self._stdscr.addstr(curses.LINES - 3, 2, "LEFT/RIGHT: select   ENTER: buy/leave")
        self._stdscr.refresh()


    def _draw_shop_cards(self, items: list[tuple[str, str, int]], selected: int) -> None:
        card_width = 25
        card_height = 14
        total_width = card_width * len(items) + (len(items) - 1)
        x_start = (curses.COLS - total_width) // 2
        y_pos = curses.LINES // 2 - card_height // 2

        x = x_start
        for i, (label, description, cost) in enumerate(items):
            border_attr = curses.color_pair(7) if i == selected else curses.A_NORMAL

            self._stdscr.attron(border_attr)
            rectangle(self._stdscr, y_pos, x, y_pos + card_height, x + card_width)
            self._stdscr.attroff(border_attr)

            name_lines = textwrap.wrap(label, card_width - 2)
            name_y = y_pos + 1
            for line in name_lines:
                self._stdscr.addstr(name_y, x + (card_width - len(line)) // 2, line)
                name_y += 1

            desc_lines = textwrap.wrap(description, card_width -2)[:card_height - 4 - len(name_lines)]
            desc_y = name_y + 1
            for line in desc_lines:
                self._stdscr.addstr(desc_y, x + (card_width - len(line)) // 2 + 1, line)
                desc_y += 1

            price_str = f"${cost}"
            self._stdscr.addstr(y_pos + card_height - 2, x + (card_width - len(price_str)) // 2, price_str)

            x += card_width + 1

import curses
import textwrap
from curses.textpad import rectangle

from mastermind_kernel.code import Code
from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.jokers import Joker
from mastermind_overlay.relics.relic import Relic
from mastermind_overlay.run.gamestate import GameState

from mastermind_overlay.run.run_state import RunState
from mastermind_shell.curses_backend import palette


class CursesRenderer:
    _BOTTOM_PADDING: int = 1
    _WIN_STR: str = "You won, let's go to the next round."
    _RUN_WIN_STR: str = "You finished the run"
    _LOOSE_STR: str = "You lost, you must restart haha..."
    _RUN_OVER_STR: str = "You finished the run, good for you. Do you want an endless mode ?"
    _PANEL_WIDTH: int = 22
    _PLAY_STR: str = """
   ___  __   _____  __
  / _ \\/ /  / _ \\ \\/ /
 / ___/ /__/ __ |\\  /
/_/  /____/_/ |_|/_/
"""

    _QUIT_STR: str = """
   ___  _   _ ___ _____
  / _ \\| | | |_ _|_   _|
 | (_) | |_| || |  | |
  \\__\\_\\\\___/|___| |_|
"""


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


    def render_menu(self, current: int) -> None:
        self.clear()

        lines, _ = self.dimensions()

        height_play = 0
        for _ in self._PLAY_STR.strip("\n").splitlines():
            height_play += 1

        start_y = (lines // 2) - height_play - 1
        self._render_big_str(start_y, self._PLAY_STR, current == 0)
        start_y += height_play + 1
        self._render_big_str(start_y, self._QUIT_STR, current == 1)

        self.refresh()

    def _render_big_str(self, start_y: int, big_text: str, highlighted: bool) -> None:
        lines_list = big_text.strip('\n').splitlines()
        max_len = max(len(line) for line in lines_list)
        _, cols = self.dimensions()
        start_x = (cols - max_len) // 2

        for line in lines_list:
            self.draw_text(start_y, start_x, line, highlighted)
            start_y += 1


    def render_gameplay(self, state: GameState, stage: int, tier_label: str, relics: list[Relic], jokers: list[Joker], run_state: RunState) -> None:
        self._stdscr.clear()
        self._draw_frame()
        self._render_left_panel(stage, state.score, state.target_score, state.turns_left, tier_label, relics, jokers, run_state)
        self._draw_guessed_squares(state.guessed_codes, state.guessed_feedback)
        self._draw_guess_squares(state.current_peg, state.current_code)
        self._render_commands()
        self._stdscr.refresh()


    def _render_commands(self) -> None:
        y = curses.LINES - 3
        self._stdscr.addstr(y, self._PANEL_WIDTH + 2, "LEFT/RIGHT: box    UP/DOWN: color    ENTER: submit")


    def render_run_over(self, selected: int) -> None:
        y = curses.LINES // 2
        self._stdscr.addstr(
            y,
            (curses.COLS - len(self._RUN_OVER_STR)) // 2,
            self._RUN_OVER_STR,
            curses.A_STANDOUT)
        
        width = 17
        height = 5
        boxes_width = width * 2 + 5
        y += 1
        x = (curses.COLS - boxes_width) // 2

        self._render_rectangle_with_centered_text(selected == 0, y, x, width, height, "YES")

        x += width + 5
        self._render_rectangle_with_centered_text(selected == 1, y, x, width, height, "NO")


    def _render_rectangle_with_centered_text(self, selected: bool, y: int, x: int, width: int, height: int, text: str) -> None:
        border_attr = curses.color_pair(7) if selected else curses.A_NORMAL
        self._stdscr.attron(border_attr)
        rectangle(self._stdscr, y, x, y + height, x + width)
        self._stdscr.attroff(border_attr)

        self._stdscr.addstr(
            y + (height // 2),
            x + (width // 2),
            text,
            curses.A_NORMAL)



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

    def render_win_run(self) -> None:
        self._stdscr.addstr(
            curses.LINES // 2,
            (curses.COLS + len(self._RUN_WIN_STR)) // 2,
            self._WIN_STR,
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


    def _render_left_panel(self, stage: int, score: int, target: int, turns_left: int, tier_label: str, relics: list[Relic], jokers: list[Joker], run_state: RunState) -> None:
        x = 2
        y = 1
        for line in (
            f"STAGE    : {stage}",
            f"TIER     : {tier_label}",
            f"SCORE    : {score}",
            f"TARGET   : {target}",
            f"TURNS    : {turns_left}",
            f"CURRENCY : ${run_state.currency}",
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

        y += 1
        self._stdscr.addch(y, 0, curses.ACS_LTEE)
        self._stdscr.hline(y, 1, curses.ACS_HLINE, self._PANEL_WIDTH - 1)
        self._stdscr.addch(y, self._PANEL_WIDTH, curses.ACS_RTEE)
        y += 1

        self._stdscr.addstr(y, x, "JOKERS")
        y += 1
        for joker in jokers:
            self._stdscr.addstr(y, x, str(joker))
            y += 1


    def render_shop(self, currency: int, offer: list[Relic], extra_guess_price: int, selected: int, owned_relics: list[Relic], max_relics: int, reroll_price: int, joker_price: int) -> None:
        self._stdscr.clear()
        rectangle(self._stdscr, 0, 1, curses.LINES - 2, curses.COLS - 2)

        title = "SHOP"
        self._stdscr.addstr(1, (curses.COLS - len(title)) // 2, title, curses.A_BOLD | curses.A_STANDOUT)
        self._stdscr.addstr(1, 2, f"$ {currency}")

        self._render_relic_slots(owned_relics, max_relics, selected)

        relics_full = len(owned_relics) >= max_relics
        items = [(str(relic), relic.description, relic.price) for relic in offer] + [("Extra guess", "Gain an extra guess this round", extra_guess_price)]
        self._render_shop_cards(items, selected - len(owned_relics), len(offer), relics_full)

        reroll_idx = len(owned_relics) + len(items)
        self._render_shop_reroll(reroll_price, selected == reroll_idx)

        jokers_idx = reroll_idx + 1
        self._render_shop_joker_booster(joker_price, selected == jokers_idx)

        leave_idx = jokers_idx + 1
        leave_str = "[ Leave Shop ]"
        attr = curses.A_STANDOUT if selected == leave_idx else curses.A_NORMAL
        self._stdscr.addstr(curses.LINES - 4, (curses.COLS - len(leave_str)) // 2, leave_str, attr)

        self._stdscr.addstr(curses.LINES - 3, 2, "LEFT/RIGHT: select   ENTER: buy/sell/leave")
        self._stdscr.refresh()


    def _render_shop_joker_booster(self, price: int, selected: bool) -> None:
        width = 18
        height = 10
        x_pos = curses.COLS - width - 4
        y_pos = curses.LINES - height - 3
        border_attr = curses.color_pair(7) if selected else curses.A_NORMAL

        self._stdscr.attron(border_attr)
        rectangle(self._stdscr, y_pos, x_pos, y_pos + height, x_pos + width)
        self._stdscr.attroff(border_attr)

        self._stdscr.addstr(y_pos + (height // 2), x_pos + (width - len("JOKER BOOSTER")) // 2, "JOKER BOOSTER")
        self._stdscr.addstr(y_pos + (height // 2) + 1, x_pos + (width - len(f"${price}")) // 2, f"${price}")


    def _render_shop_reroll(self, price: int, selected: bool) -> None:
        width = 18
        height = 5
        x_pos = curses.COLS - width - 4
        y_pos = (curses.LINES - height) // 2
        border_attr = curses.color_pair(7) if selected else curses.A_NORMAL

        self._stdscr.attron(border_attr)
        rectangle(self._stdscr, y_pos, x_pos, y_pos + height, x_pos + width)
        self._stdscr.attroff(border_attr)

        self._stdscr.addstr(y_pos + (height // 2), x_pos + (width - len("REROLL")) // 2, "REROLL")
        self._stdscr.addstr(y_pos + (height // 2) + 1, x_pos + (width - len(f"${price}")) // 2, f"${price}")


    def _render_relic_slots(self, owned_relics: list[Relic], max_relics: int, selected: int) -> None:
        slot_width = 16
        slot_height = 4
        total_width = slot_width * max_relics + (max_relics - 1)
        x_start = (curses.COLS - total_width) // 2
        y_pos = 3

        x = x_start
        for i in range(max_relics):
            filled = i < len(owned_relics)
            if filled:
                border_attr = curses.color_pair(7) if i == selected else curses.A_NORMAL
            else:
                border_attr = curses.A_DIM

            self._stdscr.attron(border_attr)
            rectangle(self._stdscr, y_pos, x, y_pos + slot_height, x + slot_width)
            self._stdscr.attroff(border_attr)

            if filled:
                label_lines = textwrap.wrap(str(owned_relics[i]), slot_width - 2)[:slot_height - 2]
                label_y = y_pos + 1
                for line in label_lines:
                    self._stdscr.addstr(label_y, x + (slot_width - len(line)) // 2, line)
                    label_y += 1

            x += slot_width + 1


    def _render_shop_cards(self, items: list[tuple[str, str, int]], selected: int, relic_count: int, relics_full: bool) -> None:
        card_width = 25
        card_height = 14
        total_width = card_width * len(items) + (len(items) - 1)
        x_start = (curses.COLS - total_width) // 2
        y_pos = curses.LINES // 2 - card_height // 2

        x = x_start
        for i, (label, description, cost) in enumerate(items):
            is_locked = relics_full and i < relic_count
            border_attr = curses.color_pair(7) if i == selected else curses.A_NORMAL
            text_attr = curses.A_DIM if is_locked else curses.A_NORMAL

            self._stdscr.attron(border_attr)
            rectangle(self._stdscr, y_pos, x, y_pos + card_height, x + card_width)
            self._stdscr.attroff(border_attr)

            name_lines = textwrap.wrap(label, card_width - 2)
            name_y = y_pos + 1
            for line in name_lines:
                self._stdscr.addstr(name_y, x + (card_width - len(line)) // 2, line, text_attr)
                name_y += 1

            desc_lines = textwrap.wrap(description, card_width -2)[:card_height - 4 - len(name_lines)]
            desc_y = name_y + 1
            for line in desc_lines:
                self._stdscr.addstr(desc_y, x + (card_width - len(line)) // 2 + 1, line, text_attr)
                desc_y += 1

            price_str = "LOCKED" if is_locked else f"${cost}"
            self._stdscr.addstr(y_pos + card_height - 2, x + (card_width - len(price_str)) // 2, price_str, text_attr)

            x += card_width + 1


    def render_boss_announcement(self, title: str, description: str) -> None:
        self._stdscr.clear()
        self._stdscr.addstr(
            curses.LINES // 2,
            (curses.COLS - len(title)) // 2,
            title,
            curses.A_STANDOUT)
        self._stdscr.addstr(
            curses.LINES // 2 + 1,
            (curses.COLS - len(description)) // 2,
            description,
            curses.A_STANDOUT)
        self._stdscr.refresh()

    def error(self, message: str) -> None:
        self._stdscr.addstr(
            curses.LINES // 2,
            (curses.COLS - len(message)) // 2,
            message,
            curses.A_STANDOUT)
        _ = self._stdscr.getch()


    def render_joker_booster(self, jokers: list[Joker], selected: int) -> None:
        self._stdscr.clear()
        rectangle(self._stdscr, 1, 1, curses.LINES - 2, curses.COLS - 2)

        card_width = 25
        card_height = 14
        total_width = card_width * len(jokers) + (len(jokers) - 1)
        x_start = (curses.COLS - total_width) // 2
        y_pos = curses.LINES // 2 - card_height // 2

        x = x_start
        for i, joker in enumerate(jokers):
            border_attr = curses.color_pair(7) if i == selected else curses.A_NORMAL

            self._stdscr.attron(border_attr)
            rectangle(self._stdscr, y_pos, x, y_pos + card_height, x + card_width)
            self._stdscr.attroff(border_attr)

            name_lines = textwrap.wrap(str(joker), card_width - 2)
            name_y = y_pos + 1
            for line in name_lines:
                self._stdscr.addstr(name_y, x + (card_width - len(line)) // 2, line, curses.A_NORMAL)
                name_y += 1

            desc_lines = textwrap.wrap(joker.description, card_width -2)[:card_height - 4 - len(name_lines)]
            desc_y = name_y + 1
            for line in desc_lines:
                self._stdscr.addstr(desc_y, x + (card_width - len(line)) // 2 + 1, line, curses.A_NORMAL)
                desc_y += 1

            x += card_width + 1


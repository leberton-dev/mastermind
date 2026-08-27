import curses

from typing import override

from mastermind.core.screen_manager import Screen, ScreenQueue, ScreenTransition
from mastermind.screens.gameplay import GameplayScreen


class MenuScreen(Screen):
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
                      
    def __init__(self, stdscr: curses.window, queue: ScreenQueue) -> None:
        super().__init__(stdscr, queue, True)
        self._current: int = 0


    @override
    def handle_input(self, key: int) -> None:
        if key == ord('q'):
            self._queue.push(ScreenTransition.quit())
        if key == curses.KEY_ENTER or key == ord('\n') or key == ord('\r'):
            if self._current == 0:
                gameplay_screen = GameplayScreen(self._stdscr, self._queue)
                self._queue.push(ScreenTransition.push(gameplay_screen))
            elif self._current == 1:
                self._queue.push(ScreenTransition.quit())
        if key == curses.KEY_UP:
            self._current = (self._current + 1) % 2
        if key == curses.KEY_DOWN:
            self._current = (self._current - 1) % 2


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        self._stdscr.clear()

        height_play = 0
        for _ in self._PLAY_STR.strip("\n").splitlines():
            height_play += 1

        height_quit = 0
        for _ in self._QUIT_STR.strip("\n").splitlines():
            height_quit += 1

        start_y = (curses.LINES // 2) - height_play - 1
        attr = curses.A_STANDOUT if self._current == 0 else None
        self._render_big_str(start_y, self._PLAY_STR, attr)
        start_y += height_play + 1
        attr = curses.A_STANDOUT if self._current == 1 else None
        self._render_big_str(start_y, self._QUIT_STR, attr)

        self._stdscr.refresh()


    def _render_big_str(self, start_y: int, big_text: str, attr: int | None) -> None:
        lines = big_text.strip('\n').splitlines()
        max_len = max(len(line) for line in lines)
        start_x = (curses.COLS - max_len) // 2

        for line in lines:
            if attr is None:
                self._stdscr.addstr(start_y, start_x, line)
            else:
                self._stdscr.addstr(start_y, start_x, line, attr)
            start_y += 1


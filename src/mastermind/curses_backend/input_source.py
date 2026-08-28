import curses

from mastermind.curses_backend.keymap import keycode_to_event
from mastermind.engine.input_event import InputEvent


class CursesInputSource:
    def __init__(self, stdscr: curses.window) -> None:
        self._stdscr: curses.window = stdscr


    def next_event(self) -> InputEvent | None:
        key = self._stdscr.getch()
        return keycode_to_event(key)

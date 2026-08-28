import curses
from curses import wrapper

from mastermind.curses_backend import palette
from mastermind.curses_backend.input_source import CursesInputSource
from mastermind.curses_backend.renderer import CursesRenderer
from mastermind.engine.screen_queue import ScreenQueue
from mastermind.engine.screen_stack import ScreenStack
from mastermind.screens.menu import MenuScreen


def _init_curses(stdscr: curses.window) -> None:
    _ = curses.curs_set(0)
    stdscr.keypad(True)

    curses.cbreak()
    curses.noecho()
    curses.start_color()
    if not curses.has_colors():
        raise Exception("Terminal does not have colors")
    palette.init_color_pairs()


def main(stdscr: curses.window):
    _init_curses(stdscr)

    renderer: CursesRenderer = CursesRenderer(stdscr)
    input_source: CursesInputSource = CursesInputSource(stdscr)
    queue: ScreenQueue = ScreenQueue()
    menu: MenuScreen = MenuScreen(queue, renderer)
    stack: ScreenStack = ScreenStack(input_source, queue, menu)

    while stack.step():
        pass


if __name__ == "__main__":
    wrapper(main)

import curses
from curses import wrapper

from mastermind import ui
from mastermind.core.screen_manager import ScreenQueue, ScreenStack
from mastermind.screens.menu import MenuScreen


def _init_curses(stdscr: curses.window) -> None:
    _ = curses.curs_set(0)
    stdscr.keypad(True)

    curses.cbreak()
    curses.noecho()
    curses.start_color()
    if not curses.has_colors():
        raise Exception("Terminal does not have colors")
    ui.palette.init_color_pairs()


def main(stdscr: curses.window):
    _init_curses(stdscr)
    
    queue: ScreenQueue = ScreenQueue()
    menu: MenuScreen = MenuScreen(stdscr, queue)
    stack: ScreenStack = ScreenStack(stdscr, queue, menu)

    while stack.step():
        pass


if __name__ == "__main__":
    wrapper(main)

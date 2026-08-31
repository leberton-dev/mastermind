import curses
from curses import wrapper

from mastermind_shell.curses_backend import palette
from mastermind_shell.curses_backend.input_source import CursesInputSource
from mastermind_shell.curses_backend.renderer import CursesRenderer
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.screen_stack import ScreenStack
from mastermind_shell.screens.menu import MenuScreen

# import debugpy

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


def run() -> None:
    # _ = debugpy.listen(("127.0.0.1", 5678))
    # print("Waiting for debugger...")
    # debugpy.wait_for_client()
    wrapper(main)


if __name__ == "__main__":
    run()

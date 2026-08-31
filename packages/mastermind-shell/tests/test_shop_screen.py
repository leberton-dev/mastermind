import curses
from curses import wrapper

from mastermind_overlay.run.gamestate import GameState
from mastermind_overlay.run.run_state import RunState
from mastermind_shell.curses_backend.palette import init_color_pairs
from mastermind_shell.curses_backend.renderer import CursesRenderer
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.screens.shop import ShopScreen

def main(stdscr: curses.window):
    run_state = RunState()
    queue = ScreenQueue()
    renderer = CursesRenderer(stdscr)
    next_game_state = GameState(10, 10, [])
    screen = ShopScreen(queue, renderer, run_state, next_game_state)

    screen.render()

    _ = stdscr.getch()



def run():
    wrapper(main)
    init_color_pairs()


if __name__ == "__main__":
    run()

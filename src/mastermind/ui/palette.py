import curses

from mastermind.core.colors import Color



def init_color_pairs() -> None:
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(7, curses.COLOR_CYAN, curses.COLOR_BLACK)


def to_curses_pair(color: Color) -> int:
    color_to_curses: dict[Color, int] = {
            Color.WHITE: curses.color_pair(1),
            Color.ORANGE: curses.color_pair(2),
            Color.BLUE: curses.color_pair(3),
            Color.GREEN: curses.color_pair(4),
            Color.RED: curses.color_pair(5),
            Color.PURPLE: curses.color_pair(6)
    }
    return color_to_curses[color]


import curses
from curses import wrapper

import mastermind.bot as bot
import mastermind.player as player
from mastermind import ui

from mastermind.core.colors import Color

_MAX_TURNS = 10


def play():
    secret_code: list[Color] = bot.secret.random_code()

    for _ in range(_MAX_TURNS):
        guess = player.prompt.guess()
        result = bot.score.feedback(secret_code, guess)
        print(f"Result is : {result}")
        if result == (4, 0):
            print("You won.")
            break
    print("You lost.")


def main(stdscr: curses.window):
    _ = curses.curs_set(0)
    stdscr.keypad(True)

    curses.cbreak()
    curses.noecho()
    curses.start_color()
    if not curses.has_colors():
        raise Exception("Terminal does not have colors")
    ui.palette.init_color_pairs()

    current_square: int = 0
    guess_squares: list[Color] = [Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE]
    guessed_squares: list[list[Color]] = []
    while True:
        stdscr.clear()
        stdscr.addstr(1, (curses.COLS - len("Welcome to Mastermind")) // 2, "Welcome to Mastermind", curses.A_STANDOUT)
        ui.board.draw_guessed_squares(stdscr, guessed_squares)
        ui.board.draw_guess_squares(stdscr, current_square, guess_squares)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP:
            ui.board.switch_guess_color(current_square, -1, guess_squares)
        if key == curses.KEY_DOWN:
            ui.board.switch_guess_color(current_square, 1, guess_squares)
        if key == curses.KEY_LEFT:
            current_square = (current_square - 1) % len(guess_squares)
        if key == curses.KEY_RIGHT:
            current_square = (current_square + 1) % len(guess_squares)
        if key in (curses.KEY_ENTER, ord('\n'), ord('\r')):
            guessed_squares.append(list(guess_squares))
            guess_squares = [Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE]
            current_square = 0
        if key == ord('q'):
            break


if __name__ == "__main__":
    wrapper(main)

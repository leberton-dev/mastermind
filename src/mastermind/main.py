import curses
from curses import wrapper

from mastermind import bot
from mastermind import player
from mastermind import ui

from mastermind.core.colors import Color

_MAX_TURNS = 10
_WIN_STR = "You won"
_LOOSE_STR = "You lost"
_WINNING_VALUE = (4, 0)

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
    guessed_feedback: list[tuple[int, int]] = []
    secret_code: list[Color] = bot.secret.random_code()
    while True:
        stdscr.clear()
        stdscr.addstr(1, (curses.COLS - len("Welcome to Mastermind")) // 2, "Welcome to Mastermind", curses.A_STANDOUT)
        ui.board.draw_guessed_squares(stdscr, guessed_squares, guessed_feedback)
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
            feedback = bot.score.feedback(secret_code, guess_squares)
            guessed_feedback.append(feedback)

            if feedback == _WINNING_VALUE:
                stdscr.addstr(curses.LINES // 2, (curses.COLS + len(_WIN_STR)) // 2, _WIN_STR, curses.A_STANDOUT)
                _ = stdscr.getch()
                break

            if len(guessed_squares) >= _MAX_TURNS:
                correct_guess_str = f"Correct was : {[c for c in secret_code]}"
                stdscr.addstr(curses.LINES // 2, (curses.COLS + len(_LOOSE_STR)) // 2, _LOOSE_STR, curses.A_STANDOUT)
                stdscr.addstr(curses.LINES // 2, (curses.COLS + len(correct_guess_str)) // 2, correct_guess_str, curses.A_STANDOUT)
                _ = stdscr.getch()
                break

            guess_squares = [Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE]
            current_square = 0
        if key == ord('q'):
            break


if __name__ == "__main__":
    wrapper(main)

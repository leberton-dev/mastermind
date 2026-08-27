from mastermind.core.colors import Color
from mastermind.core.feedback import Feedback
from mastermind import bot

class GameState:
    _MAX_TURNS: int = 10
    _WINNING_VALUE: tuple[int, int] = (4, 0)

    def __init__(self) -> None:
        self._current_square: int = 0
        self._guess_squares: list[Color] = []
        self._secret_code: list[Color] = []
        self._guessed_squares: list[list[Color]] = []
        self._guessed_feedback: list[Feedback] = []
        self.reset()

    @property
    def current_square(self) -> int:
        return self._current_square

    @property
    def guess_squares(self) -> list[Color]:
        return self._guess_squares

    @property
    def secret_code(self) -> list[Color]:
        return self._secret_code

    @property
    def guessed_squares(self) -> list[list[Color]]:
        return self._guessed_squares

    @property
    def guessed_feedback(self) -> list[Feedback]:
        return self._guessed_feedback

    @property
    def won(self) -> bool:
        return self._guessed_feedback[-1].won

    @property
    def lost(self) -> bool:
        return len(self._guessed_feedback) >= self._MAX_TURNS and not self._guessed_feedback[-1].won

    def submit_guess(self) -> None:
        self._guessed_squares.append(list(self._guess_squares))
        feedback: Feedback = bot.score.feedback(self._secret_code, self._guess_squares)
        self._guessed_feedback.append(feedback)

    def cycle_color(self, direction: int) -> None:
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1

        idx = (self._guess_squares[self._current_square].value - 1 + direction) % len(Color)
        self._guess_squares[self._current_square] = Color(idx + 1)

    def cycle_current_square(self, direction: int) -> None:
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1

        self._current_square = (self._current_square + direction) % len(self._guess_squares)

    def reset_current_guess(self) -> None:
        self._guess_squares = [Color.WHITE] * 4
        self._current_square = 0

    def reset(self) -> None:
        self.reset_current_guess()
        self._secret_code = bot.secret.random_code()
        self._guessed_squares = []
        self._guessed_feedback = []



from mastermind.core.colors import PegColor
from mastermind.core.feedback import CodeFeedback
from mastermind.core.code import Code

class GameState:
    _MAX_TURNS: int = 10

    def __init__(self) -> None:
        self._current_square: int = 0
        self._guess_squares: Code = Code.blank()
        self._secret_code: Code = Code.random()
        self._guessed_squares: list[Code] = []
        self._guessed_feedback: list[CodeFeedback] = []

    @property
    def current_square(self) -> int:
        return self._current_square

    @property
    def guess_squares(self) -> Code:
        return self._guess_squares

    @property
    def secret_code(self) -> Code:
        return self._secret_code

    @property
    def guessed_squares(self) -> list[Code]:
        return self._guessed_squares

    @property
    def guessed_feedback(self) -> list[CodeFeedback]:
        return self._guessed_feedback

    @property
    def won(self) -> bool:
        return self._guessed_feedback[-1].won

    @property
    def lost(self) -> bool:
        return len(self._guessed_feedback) >= self._MAX_TURNS and not self._guessed_feedback[-1].won

    def submit_guess(self) -> None:
        self._guessed_squares.append(self._guess_squares)
        feedback: CodeFeedback = self._secret_code.feedback(self._guess_squares)
        self._guessed_feedback.append(feedback)

    def cycle_color(self, direction: int) -> None:
        self._guess_squares.cycle(self._current_square, direction)

    def cycle_current_square(self, direction: int) -> None:
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1

        self._current_square = (self._current_square + direction) % len(self._guess_squares)

    def reset_current_guess(self) -> None:
        self._guess_squares = Code.blank()
        self._current_square = 0

    def reset(self) -> None:
        self.reset_current_guess()
        self._secret_code = Code.random()
        self._guessed_squares = []
        self._guessed_feedback = []



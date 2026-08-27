from mastermind.core.feedback import CodeFeedback
from mastermind.core.code import Code

class GameState:
    _MAX_TURNS: int = 10

    def __init__(self) -> None:
        self._current_peg: int = 0
        self._current_code: Code = Code.blank()
        self._secret_code: Code = Code.random()
        self._guessed_codes: list[Code] = []
        self._guessed_feedback: list[CodeFeedback] = []

    @property
    def current_peg(self) -> int:
        return self._current_peg

    @property
    def current_code(self) -> Code:
        return self._current_code

    @property
    def secret_code(self) -> Code:
        return self._secret_code

    @property
    def guessed_codes(self) -> list[Code]:
        return self._guessed_codes

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
        self._guessed_codes.append(self._current_code)
        feedback: CodeFeedback = self._secret_code.feedback(self._current_code)
        self._guessed_feedback.append(feedback)

    def cycle_color(self, direction: int) -> None:
        self._current_code.cycle(self._current_peg, direction)

    def cycle_current_square(self, direction: int) -> None:
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1

        self._current_peg = (self._current_peg + direction) % len(self._current_code)

    def reset_current_guess(self) -> None:
        self._current_code = Code.blank()
        self._current_peg = 0

    def reset(self) -> None:
        self.reset_current_guess()
        self._secret_code = Code.random()
        self._guessed_codes = []
        self._guessed_feedback = []


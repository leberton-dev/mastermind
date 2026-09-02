from mastermind_kernel.code import Code
from mastermind_kernel.feedback import CodeFeedback

from mastermind_overlay.jokers.jokers import Joker, JokerContext
from mastermind_overlay.relics.relic import Relic
from mastermind_overlay.scoring.pipeline import ScoringPipeline
from mastermind_overlay.scoring.points import apply_multiplier, compute_points
from mastermind_overlay.boss_mutators.mutator import BossMutator


class GameState:
    def __init__(self, max_turns: int, target_score: int, relics: list[Relic], jokers: list[Joker], mutator: BossMutator | None = None) -> None:
        self._max_turns: int = max_turns
        self._target_score: int = target_score
        self._current_turn: int = 0
        self._current_peg: int = 0
        self._mutator: BossMutator | None = mutator
        self._current_code: Code = Code.blank()
        self._sanitize_current_code()
        self._secret_code: Code = Code.random()
        self._guessed_codes: list[Code] = []
        self._guessed_feedback: list[CodeFeedback] = []
        self._score: int = 14
        self._relics: list[Relic] = relics
        self._jokers: list[Joker] = jokers
        self._pipeline: ScoringPipeline = ScoringPipeline(relics)

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
    def score(self) -> int:
        return self._score

    @property
    def won(self) -> bool:
        return self._score >= self._target_score

    @property
    def lost(self) -> bool:
        return len(self._guessed_feedback) >= self._max_turns and not self.won

    @property
    def turns_left(self) -> int:
        return self._max_turns - self._current_turn

    @property
    def game_over(self) -> bool:
        return self.lost or self.won

    @property
    def target_score(self) -> int:
        return self._target_score

    @property
    def mutator(self) -> BossMutator | None:
        return self._mutator


    def submit_guess(self) -> None:
        if self._current_code in self._guessed_codes:
            raise ValueError("Code already exists in guessed codes")
        self._guessed_codes.append(self._current_code)

        context = JokerContext(
            guess = self._current_code,
            secret = self._secret_code,
            feedback = self._secret_code.feedback(self._current_code),
            turn = self._current_turn
        )

        for joker in self._jokers:
            context = joker.on_feedback(context)

        feedback = context.feedback

        displayed_feedback = feedback
        if self._mutator is not None:
            displayed_feedback = self._mutator.transform_feedback(feedback)
        self._guessed_feedback.append(displayed_feedback)

        points, mult = self._pipeline.run(compute_points(feedback), 1, feedback)
        self._score += apply_multiplier(points, mult)
        self._current_turn += 1


    def add_turn(self) -> None:
        self._max_turns += 1


    def cycle_color(self, direction: int) -> None:
        self._current_code.cycle(self._current_peg, direction)
        self._enforce_allowed_color(self._current_peg, direction)


    def _enforce_allowed_color(self, peg: int, direction: int = 1) -> None:
        if self._mutator is None:
            return

        allowed = self._mutator.allowed_colors()
        if allowed is None:
            return

        while self._current_code[peg] not in allowed:
            self._current_code.cycle(peg, direction)


    def _sanitize_current_code(self) -> None:
        for peg in range(len(self._current_code)):
            self._enforce_allowed_color(peg)


    def cycle_current_square(self, direction: int) -> None:
        if direction > 0:
            direction = 1
        elif direction < 0:
            direction = -1

        self._current_peg = (self._current_peg + direction) % len(self._current_code)

    def reset_current_guess(self) -> None:
        self._current_code = Code.blank()
        self._sanitize_current_code()
        self._current_peg = 0

    def reset(self) -> None:
        self.reset_current_guess()
        self._secret_code = Code.random()
        self._guessed_codes = []
        self._guessed_feedback = []



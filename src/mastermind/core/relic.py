from dataclasses import dataclass
from enum import Enum
from typing import override, Callable

import random

from mastermind.core.feedback import CodeFeedback
from mastermind.core.scoring import Points


class RelicGrade(Enum):
    STANDARD = 1
    ADVANCED = 2
    EXPERT = 3
    PRIME = 4


@dataclass(frozen=True)
class RelicSpec:
    key: str
    description: str
    grade: RelicGrade
    effect: Callable[[Points, int, CodeFeedback], tuple[Points, int]]


RELICS: list[RelicSpec] = [
    RelicSpec("mult_plus_one", "Add +1 to the multiplier", RelicGrade.STANDARD,
              lambda points, mult, fb: (points, mult + 1)),
    RelicSpec("points_plus_one", "Add +1 to the points", RelicGrade.STANDARD,
              lambda points, mult, fb: (Points(points.value + 1), mult)),
    RelicSpec("points_per_black_peg", "Add +1 to the points for each black peg", RelicGrade.ADVANCED,
              lambda points, mult, fb: (Points(points.value + fb.black_pegs), mult)),
    RelicSpec("points_per_white_peg", "Add +1 to the points for each white peg", RelicGrade.ADVANCED,
              lambda points, mult, fb: (Points(points.value + fb.white_pegs), mult)),
    RelicSpec("points_per_peg", "Add +1 to the points for each peg", RelicGrade.STANDARD,
              lambda points, mult, fb: (Points(points.value + fb.black_pegs + fb.white_pegs), mult)),
    RelicSpec("mult_on_no_black_peg", "Add +1 to the multiplier if the guess has no black pegs", RelicGrade.STANDARD,
              lambda points, mult, fb: (points, mult) if fb.black_pegs > 0 else (points, mult + 1)),
    RelicSpec("points_on_balanced_peg", "Add +2 to the points if black pegs equal white pegs", RelicGrade.STANDARD,
              lambda points, mult, fb: (points, mult) if fb.black_pegs != fb.white_pegs else (Points(points.value + 2), mult)),
    RelicSpec("mult_double_on_win", "Double the multiplier on a winning guess", RelicGrade.ADVANCED,
              lambda points, mult, fb: (points, mult * 2) if fb.won else (points, mult)),
    RelicSpec("mult_on_no_white_peg", "Add +1 to the multiplier if the guess has no white pegs", RelicGrade.ADVANCED,
              lambda points, mult, fb: (points, mult) if fb.white_pegs != 0 else (points, mult + 1)),
    RelicSpec("points_white_as_black", "Count white pegs as black pegs for points calculation", RelicGrade.EXPERT,
              lambda points, mult, fb: (Points(points.value + fb.white_pegs), mult)),
    RelicSpec("points_double_on_win", "Double the points on a winning guess", RelicGrade.EXPERT,
              lambda points, mult, fb: (Points(points.value * 2), mult) if fb.won else (points, mult)),
]


_PRICE_RANGES: dict[RelicGrade, tuple[int, int]] = {
        RelicGrade.STANDARD: (3, 6),
        RelicGrade.ADVANCED: (5, 8),
        RelicGrade.EXPERT: (7, 10),
        RelicGrade.PRIME: (20, 20),
        }


class Relic:
    def __init__(self, spec: RelicSpec) -> None:
        self.spec: RelicSpec = spec
        low, high = _PRICE_RANGES[spec.grade]
        self.price: int = random.randint(low, high)

    @property
    def description(self) -> str:
        return self.spec.description

    @property
    def grade(self) -> RelicGrade:
        return self.spec.grade

    def on_guess(self, points: Points, mult: int, feedback: CodeFeedback) -> tuple[Points, int]:
        return self.spec.effect(points, mult, feedback)

    @override
    def __str__(self) -> str:
        return self.spec.key

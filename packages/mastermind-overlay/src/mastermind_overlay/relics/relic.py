from dataclasses import dataclass
from enum import Enum
from typing import override, Callable

import random

from mastermind_kernel.feedback import CodeFeedback

from mastermind_overlay.scoring.points import Points


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

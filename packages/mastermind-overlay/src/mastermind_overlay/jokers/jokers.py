import random
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from typing import override

from mastermind_kernel.code import Code
from mastermind_kernel.feedback import CodeFeedback


class JokerGrade(Enum):
    STANDARD = 1
    ADVANCED = 2
    EXPERT = 3
    PRIME = 4


@dataclass(frozen=True)
class JokerContext:
    guess: Code
    secret: Code
    feedback: CodeFeedback
    turn: int


@dataclass(frozen=True)
class JokerSpec:
    key: str
    description: str
    grade: JokerGrade
    effect: Callable[[JokerContext], JokerContext]


_PRICE_RANGES: dict[JokerGrade, tuple[int, int]] = {
        JokerGrade.STANDARD: (3, 6),
        JokerGrade.ADVANCED: (5, 8),
        JokerGrade.EXPERT: (7, 10),
        JokerGrade.PRIME: (20, 20),
        }


class Joker:
    def __init__(self, spec: JokerSpec) -> None:
        self.spec: JokerSpec = spec
        low, high = _PRICE_RANGES[spec.grade]
        self.price: int = random.randint(low, high)

    @property
    def description(self) -> str:
        return self.spec.description

    @property
    def grade(self) -> JokerGrade:
        return self.spec.grade

    def on_feedback(self, context: JokerContext) -> JokerContext:
        return self.spec.effect(context)

    @override
    def __str__(self) -> str:
        return self.spec.key

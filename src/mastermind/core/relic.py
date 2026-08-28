from dataclasses import dataclass
from enum import Enum
from typing import override, Callable

import random

from mastermind.core.feedback import CodeFeedback
from mastermind.core.scoring import Chip


class RelicRarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    LEGENDARY = 4


@dataclass(frozen=True)
class RelicSpec:
    key: str
    description: str
    rarity: RelicRarity
    effect: Callable[[Chip, int, CodeFeedback], tuple[Chip, int]]


RELICS: list[RelicSpec] = [
    RelicSpec("mult_plus_one", "Add +1 to the multiplier", RelicRarity.COMMON,
              lambda chip, mult, fb: (chip, mult + 1)),
    RelicSpec("chip_plus_one", "Add +1 to the chip", RelicRarity.COMMON,
              lambda chip, mult, fb: (Chip(chip.value + 1), mult)),
    RelicSpec("chip_per_black_peg", "Add +1 to the chip for each black peg", RelicRarity.UNCOMMON,
              lambda chip, mult, fb: (Chip(chip.value + fb.black_pegs), mult)),
    RelicSpec("chip_per_white_peg", "Add +1 to the chip for each white peg", RelicRarity.UNCOMMON,
              lambda chip, mult, fb: (Chip(chip.value + fb.white_pegs), mult)),
    RelicSpec("chip_per_peg", "Add +1 to the chip for each peg", RelicRarity.COMMON,
              lambda chip, mult, fb: (Chip(chip.value + fb.black_pegs + fb.white_pegs), mult)),
    RelicSpec("mult_on_no_black_peg", "Add +1 to the multiplier if the guess has no black pegs", RelicRarity.COMMON,
              lambda chip, mult, fb: (chip, mult) if fb.black_pegs > 0 else (chip, mult + 1)),
    RelicSpec("chip_on_balanced_peg", "Add +2 to the chip if black pegs equal white pegs", RelicRarity.COMMON,
              lambda chip, mult, fb: (chip, mult) if fb.black_pegs != fb.white_pegs else (Chip(chip.value + 2), mult)),
    RelicSpec("mult_double_on_win", "Double the multiplier on a winning guess", RelicRarity.UNCOMMON,
              lambda chip, mult, fb: (chip, mult * 2) if fb.won else (chip, mult)),
    RelicSpec("mult_on_no_white_peg", "Add +1 to the multiplier if the guess has no white pegs", RelicRarity.UNCOMMON,
              lambda chip, mult, fb: (chip, mult) if fb.white_pegs != 0 else (chip, mult + 1)),
    RelicSpec("chip_white_as_black", "Count white pegs as black pegs for chip calculation", RelicRarity.RARE,
              lambda chip, mult, fb: (Chip(chip.value + fb.white_pegs), mult)),
    RelicSpec("chip_double_on_win", "Double the chip on a winning guess", RelicRarity.RARE,
              lambda chip, mult, fb: (Chip(chip.value * 2), mult) if fb.won else (chip, mult)),
]


_PRICE_RANGES: dict[RelicRarity, tuple[int, int]] = {
        RelicRarity.COMMON: (3, 6),
        RelicRarity.UNCOMMON: (5, 8),
        RelicRarity.RARE: (7, 10),
        RelicRarity.LEGENDARY: (20, 20),
        }


class Relic:
    def __init__(self, spec: RelicSpec) -> None:
        self.spec: RelicSpec = spec
        low, high = _PRICE_RANGES[spec.rarity]
        self.price: int = random.randint(low, high)

    @property
    def description(self) -> str:
        return self.spec.description

    @property
    def rarity(self) -> RelicRarity:
        return self.spec.rarity

    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        return self.spec.effect(chip, mult, feedback)

    @override
    def __str__(self) -> str:
        return self.spec.key


from abc import ABC, abstractmethod
from enum import Enum
from typing import override

import random

from mastermind.core.feedback import CodeFeedback
from mastermind.core.scoring import Chip


class RelicRarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    LEGENDARY = 4


_PRICE_RANGES: dict[RelicRarity, tuple[int, int]] = {
        RelicRarity.COMMON: (3, 6),
        RelicRarity.UNCOMMON: (5, 8),
        RelicRarity.RARE: (7, 10),
        RelicRarity.LEGENDARY: (20, 20),
        }

class Relic(ABC):
    description: str
    rarity: RelicRarity

    def __init__(self) -> None:
        low, high = _PRICE_RANGES[self.rarity]
        self.price: int = random.randint(low, high)

    @abstractmethod
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]: ...

    @abstractmethod
    def __str__(self) -> str: ...


class MultPlusOneRelic(Relic):
    description: str = "Add +1 to the multiplier"
    rarity: RelicRarity = RelicRarity.COMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        return (chip, mult + 1)

    @override
    def __str__(self) -> str:
        return "MultPlusOneRelic"


class ChipPlusOneRelic(Relic):
    description: str = "Add +1 to the chip"
    rarity: RelicRarity = RelicRarity.COMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        new_chip = Chip(chip.value + 1)
        return (new_chip, mult)

    @override
    def __str__(self) -> str:
        return "ChipPlusOneRelic"


class ChipPerBlackPegRelic(Relic):
    description: str = "Add +1 to the chip for each black peg"
    rarity: RelicRarity = RelicRarity.UNCOMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        new_chip = Chip(chip.value + feedback.black_pegs)
        return (new_chip, mult)

    @override
    def __str__(self) -> str:
        return "ChipPerBlackPegRelic"


class ChipPerWhitePegRelic(Relic):
    description: str = "Add +1 to the chip for each white peg"
    rarity: RelicRarity = RelicRarity.UNCOMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        new_chip = Chip(chip.value + feedback.white_pegs)
        return (new_chip, mult)

    @override
    def __str__(self) -> str:
        return "ChipPerWhitePegRelic"

class ChipPerPegRelic(Relic):
    description: str = "Add +1 to the chip for each peg"
    rarity: RelicRarity = RelicRarity.COMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        new_value: int = chip.value

        for _ in range(feedback.black_pegs + feedback.white_pegs):
            new_value += 1
        new_chip = Chip(new_value)

        return (new_chip, mult)

    @override
    def __str__(self) -> str:
        return "ChipPerPegRelic"


class MultOnNoBlackPegRelic(Relic):
    description: str = "Add +1 on the multiplier if the guess has no black pegs"
    rarity: RelicRarity = RelicRarity.COMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        if feedback.black_pegs > 0:
            return (chip, mult)
        return (chip, mult + 1)

    @override
    def __str__(self) -> str:
        return "MultOnNoBlackPegRelic"


class ChipOnBalancedPegRelic(Relic):
    description: str = "Add +2 to the chip if black pegs equal white pegs"
    rarity: RelicRarity = RelicRarity.COMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        if feedback.black_pegs != feedback.white_pegs:
            return (chip, mult)
        return (Chip(chip.value + 2), mult)

    @override
    def __str__(self) -> str:
        return "ChipOnBalancedPegRelic"


class MultDoubleOnWinRelic(Relic):
    description: str = "Double the multiplier on a winning guess"
    rarity: RelicRarity = RelicRarity.UNCOMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        if feedback.won:
            return (chip, mult * 2)
        return (chip, mult)


    @override
    def __str__(self) -> str:
        return "MultDoubleOnWinRelic"


class MultOnNoWhitePegRelic(Relic):
    description: str = "Add +1 to the multiplier if the guess has no white pegs"
    rarity: RelicRarity = RelicRarity.UNCOMMON

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        if feedback.white_pegs != 0:
            return (chip, mult)
        return (chip, mult + 1)

    @override
    def __str__(self) -> str:
        return "MultOnNoWhitePegRelic"


class ChipWhiteAsBlackRelic(Relic):
    description: str = "Count white pegs as black pegs for chip calculation"
    rarity: RelicRarity = RelicRarity.RARE

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        # TODO: to implement
        return (chip, mult)

    @override
    def __str__(self) -> str:
        return "ChipWhiteAsBlackRelic"


class ChipDoubleOnWinRelic(Relic):
    description: str = "Double the chip on a winning guess"
    rarity: RelicRarity = RelicRarity.RARE

    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        if feedback.won:
            return (Chip(chip.value * 2), mult)
        return (chip, mult)
    

    @override
    def __str__(self) -> str:
        return "ChipDoubleOnWinRelic"



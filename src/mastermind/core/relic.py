from abc import ABC, abstractmethod
from typing import override

from mastermind.core.scoring import Chip
from mastermind.core.feedback import CodeFeedback



class Relic(ABC):
    @abstractmethod
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]: ...

    @abstractmethod
    def __str__(self) -> str: ...


class MultPlusOneRelic(Relic):
    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        return (chip, mult + 1)

    @override
    def __str__(self) -> str:
        return "MultPlusOneRelic"


class ChipPlusOneRelic(Relic):
    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        new_chip = Chip(chip.value + 1)
        return (new_chip, mult)

    @override
    def __str__(self) -> str:
        return "ChipPlusOneRelic"


class ChipPerBlackPegRelic(Relic):
    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        new_chip = Chip(chip.value + feedback.black_pegs)
        return (new_chip, mult)

    @override
    def __str__(self) -> str:
        return "ChipPerBlackPegRelic"


class ChipPerWhitePegRelic(Relic):
    @override
    def act(self, chip: Chip, mult: int, feedback: CodeFeedback) -> tuple[Chip, int]:
        new_chip = Chip(chip.value + feedback.white_pegs)
        return (new_chip, mult)

    @override
    def __str__(self) -> str:
        return "ChipPerWhitePegRelic"

from dataclasses import dataclass

from mastermind.core.feedback import CodeFeedback


@dataclass
class Chip:
    value: int


def compute_chips(feedback: CodeFeedback) -> Chip:
    return Chip(feedback.black_pegs * 2 + feedback.white_pegs)


def apply_mult(chip: Chip, multiplier: int) -> int:
    return chip.value * multiplier
    

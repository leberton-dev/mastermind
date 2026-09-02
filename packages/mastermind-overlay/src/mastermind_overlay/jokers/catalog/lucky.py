import random

from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.jokers import JokerGrade, JokerSpec


def effect(fb: CodeFeedback) -> CodeFeedback:
    if fb.won:
        return fb

    if fb.white_pegs == 0:
        return fb

    if random.randint(1, 100) >= 20:
        return fb

    return CodeFeedback(
        black_pegs=fb.black_pegs + 1,
        white_pegs=fb.white_pegs - 1
    )


SPEC = JokerSpec(
    "lucky",
    "20% chance for a white peg to become black",
    JokerGrade.STANDARD,
    effect,
)

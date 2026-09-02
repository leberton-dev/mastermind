from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.jokers import JokerGrade, JokerSpec


def effect(fb: CodeFeedback) -> CodeFeedback:
    if fb.won:
        return fb

    return CodeFeedback(
        black_pegs=fb.black_pegs + 1,
        white_pegs=fb.white_pegs
    )


SPEC = JokerSpec(
    "multicolor",
    "Counts as any color of the board (adds a black peg)",
    JokerGrade.ADVANCED,
    effect,
)

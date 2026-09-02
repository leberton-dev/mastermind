import random

from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.jokers import JokerContext, JokerGrade, JokerSpec


def effect(context: JokerContext) -> JokerContext:
    if context.feedback.won:
        return context

    if context.feedback.white_pegs == 0:
        return context

    if random.randint(1, 100) >= 20:
        return context

    context = JokerContext(
        guess=context.guess,
        secret=context.secret,
        feedback=CodeFeedback(
            black_pegs=context.feedback.black_pegs + 1,
            white_pegs=context.feedback.white_pegs - 1),
        turn=context.turn
    )

    return context


SPEC = JokerSpec(
    "lucky",
    "20% chance for a white peg to become black",
    JokerGrade.STANDARD,
    effect,
)

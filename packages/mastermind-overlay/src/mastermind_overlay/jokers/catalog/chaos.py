import random

from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.jokers import JokerContext, JokerGrade, JokerSpec


def effect(context: JokerContext) -> JokerContext:
    if random.randint(1, 5) == 1:
        return context

    sign = 1
    if random.randint(1, 2) == 1:
        sign = -1

    black_pegs = 0
    white_pegs = 0
    if random.randint(1, 2) == 1:
        black_pegs = sign
    else:
        white_pegs = sign

    context = JokerContext(
        guess=context.guess,
        secret=context.secret,
        feedback=CodeFeedback(
            black_pegs=context.feedback.black_pegs + black_pegs,
            white_pegs=context.feedback.white_pegs + white_pegs),
        turn=context.turn
    )

    return context


SPEC = JokerSpec(
    "chaos",
    "Each guess, a random effect applies (+/-1 black, +/-1 white, nothing)",
    JokerGrade.STANDARD,
    effect,
)

import random

from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.jokers import JokerContext, JokerGrade, JokerSpec


def effect(context: JokerContext) -> JokerContext:
    black_pegs_to_add: int = 0

    if random.randint(1, 100) <= 40:
        black_pegs_to_add += 1
    else:
        black_pegs_to_add -= 2

    context = JokerContext(
        guess=context.guess,
        secret=context.secret,
        feedback=CodeFeedback(
            black_pegs=context.feedback.black_pegs + black_pegs_to_add,
            white_pegs=context.feedback.white_pegs),
        turn=context.turn
    )

    return context


SPEC = JokerSpec(
    "gambler",
    "40% : +1 black pegs, 60% : -2 blak pegs",
    JokerGrade.STANDARD,
    effect,
)

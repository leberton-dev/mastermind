from mastermind_kernel.colors import PegColor
from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.jokers import JokerContext, JokerGrade, JokerSpec


def effect(context: JokerContext) -> JokerContext:
    found_colors: list[PegColor] = []
    for c in context.guess.pegs:
        if c in found_colors:
            return context
        found_colors.append(c)

    context = JokerContext(
        guess=context.guess,
        secret=context.secret,
        feedback=CodeFeedback(
            black_pegs=context.feedback.black_pegs + 1,
            white_pegs=context.feedback.white_pegs),
        turn=context.turn
    )

    return context


SPEC = JokerSpec(
    "greedy",
    "Add 1 black peg if the guess contains 4 different colors",
    JokerGrade.ADVANCED,
    effect,
)

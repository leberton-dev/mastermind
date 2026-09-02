from mastermind_kernel.code import Code
from mastermind_kernel.colors import PegColor
from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.catalog.multicolor import SPEC
from mastermind_overlay.jokers.jokers import Joker, JokerContext


def test_multicolor_adds_black_peg():
    joker = Joker(SPEC)
    guess = Code([PegColor.WHITE, PegColor.RED, PegColor.BLUE, PegColor.GREEN])
    secret = Code([PegColor.RED, PegColor.WHITE, PegColor.BLUE, PegColor.PURPLE])
    context = JokerContext( guess=guess, secret=secret, feedback = secret.feedback(guess), turn=1)
    result = joker.on_feedback(context)

    assert result.feedback.black_pegs == 2
    assert result.feedback.white_pegs == 2


def test_multicolor_does_not_add_black_peg_if_four_present():
    joker = Joker(SPEC)
    guess = Code([PegColor.RED, PegColor.WHITE, PegColor.BLUE, PegColor.PURPLE])
    secret = Code([PegColor.RED, PegColor.WHITE, PegColor.BLUE, PegColor.PURPLE])
    context = JokerContext( guess=guess, secret=secret, feedback = secret.feedback(guess), turn=1)
    result = joker.on_feedback(context)

    assert result.feedback.black_pegs == 4
    assert result.feedback.white_pegs == 0


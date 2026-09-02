from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.jokers.catalog.multicolor import SPEC
from mastermind_overlay.jokers.jokers import Joker


def test_multicolor_adds_black_peg():
    joker = Joker(SPEC)
    feedback = CodeFeedback(black_pegs=1, white_pegs=2)
    result = joker.on_feedback(feedback)

    assert result.black_pegs == 2
    assert result.white_pegs == 2


def test_multicolor_does_not_add_black_peg_if_four_present():
    joker = Joker(SPEC)
    feedback = CodeFeedback(black_pegs=4, white_pegs=0)
    result = joker.on_feedback(feedback)

    assert result.black_pegs == 4
    assert result.white_pegs == 0


import pytest

from mastermind.core.colors import PegColor

import mastermind.bot as bot


def test_feedback_identical_sequences_all_exact():
    original = [PegColor.WHITE, PegColor.RED, PegColor.BLUE, PegColor.GREEN]
    answer = [PegColor.WHITE, PegColor.RED, PegColor.BLUE, PegColor.GREEN]

    assert bot.score.feedback(original, answer) == (4, 0)


def test_feedback_permutation_all_color_no_exact():
    original = [PegColor.WHITE, PegColor.RED, PegColor.BLUE, PegColor.GREEN]
    answer = [PegColor.RED, PegColor.WHITE, PegColor.GREEN, PegColor.BLUE]

    assert bot.score.feedback(original, answer) == (0, 4)


def test_feedback_partial_match_with_absent_color():
    original = [PegColor.WHITE, PegColor.RED, PegColor.BLUE, PegColor.GREEN]
    answer = [PegColor.WHITE, PegColor.BLUE, PegColor.ORANGE, PegColor.RED]
    
    assert bot.score.feedback(original, answer) == (1, 2)


def test_feedback_repeated_color_two_exact_one_color_match():
    original = [PegColor.WHITE, PegColor.RED, PegColor.WHITE, PegColor.RED]
    answer = [PegColor.WHITE, PegColor.RED, PegColor.BLUE, PegColor.WHITE]

    assert bot.score.feedback(original, answer) == (2, 1)


def test_feedback_repeated_color_one_exact_one_color_match():
    original = [PegColor.WHITE, PegColor.RED, PegColor.WHITE, PegColor.RED]
    answer = [PegColor.WHITE, PegColor.BLUE, PegColor.RED, PegColor.BLUE]

    assert bot.score.feedback(original, answer) == (1, 1)


def test_feedback_single_color_repeated_twice_in_answer_match():
    original = [PegColor.RED, PegColor.ORANGE, PegColor.ORANGE, PegColor.BLUE]
    answer = [PegColor.RED, PegColor.RED, PegColor.ORANGE, PegColor.BLUE]
    
    assert bot.score.feedback(original, answer) == (3, 0)


def test_feedback_raises_when_original_too_short():
    original = [PegColor.WHITE]
    answer = [PegColor.RED, PegColor.WHITE, PegColor.GREEN, PegColor.BLUE]

    with pytest.raises(ValueError):
        _ = bot.score.feedback(original, answer)


def test_feedback_raises_when_answer_too_short():
    original = [PegColor.RED, PegColor.WHITE, PegColor.GREEN, PegColor.BLUE]
    answer = [PegColor.WHITE]

    with pytest.raises(ValueError):
        _ = bot.score.feedback(original, answer)


def test_feedback_raises_when_original_too_long():
    original = [PegColor.RED, PegColor.WHITE, PegColor.GREEN, PegColor.BLUE, PegColor.ORANGE]
    answer = [PegColor.RED, PegColor.WHITE, PegColor.GREEN, PegColor.BLUE]

    with pytest.raises(ValueError):
        _ = bot.score.feedback(original, answer)


def test_feedback_raises_when_answer_too_long():
    original = [PegColor.RED, PegColor.WHITE, PegColor.GREEN, PegColor.BLUE]
    answer = [PegColor.RED, PegColor.WHITE, PegColor.GREEN, PegColor.BLUE, PegColor.ORANGE]

    with pytest.raises(ValueError):
        _ = bot.score.feedback(original, answer)

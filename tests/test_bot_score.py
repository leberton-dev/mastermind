import pytest

from mastermind.core.colors import Color

import mastermind.bot.score as score


def test_feedback_identical_sequences_all_exact():
    original = [Color.WHITE, Color.RED, Color.BLUE, Color.GREEN]
    answer = [Color.WHITE, Color.RED, Color.BLUE, Color.GREEN]

    assert score.feedback(original, answer) == (4, 0)


def test_feedback_permutation_all_color_no_exact():
    original = [Color.WHITE, Color.RED, Color.BLUE, Color.GREEN]
    answer = [Color.RED, Color.WHITE, Color.GREEN, Color.BLUE]

    assert score.feedback(original, answer) == (0, 4)


def test_feedback_partial_match_with_absent_color():
    original = [Color.WHITE, Color.RED, Color.BLUE, Color.GREEN]
    answer = [Color.WHITE, Color.BLUE, Color.ORANGE, Color.RED]
    
    assert score.feedback(original, answer) == (1, 2)


def test_feedback_repeated_color_two_exact_one_color_match():
    original = [Color.WHITE, Color.RED, Color.WHITE, Color.RED]
    answer = [Color.WHITE, Color.RED, Color.BLUE, Color.WHITE]

    assert score.feedback(original, answer) == (2, 1)


def test_feedback_repeated_color_one_exact_one_color_match():
    original = [Color.WHITE, Color.RED, Color.WHITE, Color.RED]
    answer = [Color.WHITE, Color.BLUE, Color.RED, Color.BLUE]

    assert score.feedback(original, answer) == (1, 1)


def test_feedback_raises_when_original_too_short():
    original = [Color.WHITE]
    answer = [Color.RED, Color.WHITE, Color.GREEN, Color.BLUE]

    with pytest.raises(ValueError):
        _ = score.feedback(original, answer)


def test_feedback_raises_when_answer_too_short():
    original = [Color.RED, Color.WHITE, Color.GREEN, Color.BLUE]
    answer = [Color.WHITE]

    with pytest.raises(ValueError):
        _ = score.feedback(original, answer)


def test_feedback_raises_when_original_too_long():
    original = [Color.RED, Color.WHITE, Color.GREEN, Color.BLUE, Color.ORANGE]
    answer = [Color.RED, Color.WHITE, Color.GREEN, Color.BLUE]

    with pytest.raises(ValueError):
        _ = score.feedback(original, answer)


def test_feedback_raises_when_answer_too_long():
    original = [Color.RED, Color.WHITE, Color.GREEN, Color.BLUE]
    answer = [Color.RED, Color.WHITE, Color.GREEN, Color.BLUE, Color.ORANGE]

    with pytest.raises(ValueError):
        _ = score.feedback(original, answer)

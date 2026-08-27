from mastermind.core.colors import Color
from mastermind.core.feedback import Feedback
from mastermind.core.code import Code

def feedback(secret: Code, guess: Code) -> Feedback:

    if len(secret) != 4:
        raise ValueError("original should be of length 4")
    if len(guess) != 4:
        raise ValueError("answer should be of length 4")

    secret_copy: list[Color] = [c for c in secret]
    guess_copy: list[Color] = [c for c in guess]

    black_pegs: int = _calculate_black_pegs(secret_copy, guess_copy)
    white_pegs: int = _calculate_white_pegs(secret_copy, guess_copy)

    return Feedback(black_pegs, white_pegs)


def _calculate_black_pegs(secret: list[Color], guess: list[Color]) -> int:
    black_pegs: int = 0
    found_idx: list[int] = []

    for idx, color in enumerate(guess):
        if secret[idx] == color:
            black_pegs += 1
            found_idx.append(idx)

    for idx in reversed(found_idx):
        _ = secret.pop(idx)
        _ = guess.pop(idx)

    return black_pegs


def _calculate_white_pegs(secret: list[Color], guess: list[Color]) -> int:
    white_pegs: int = 0

    for color in guess:
        for s in secret:
            if color == s:
                white_pegs += 1
                secret.remove(s)
                break

    return white_pegs


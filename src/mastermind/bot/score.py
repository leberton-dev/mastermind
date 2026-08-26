from mastermind.core.colors import Color

def feedback(secret: list[Color], guess: list[Color]) -> tuple[int, int]:

    if len(secret) != 4:
        raise ValueError("original should be of length 4")
    if len(guess) != 4:
        raise ValueError("answer should be of length 4")

    black_pegs: int = 0
    white_pegs: int = 0

    for idx, color in enumerate(guess):
        if secret[idx] == color:
            black_pegs += 1
        elif color in secret:
            white_pegs += 1

    return black_pegs, white_pegs

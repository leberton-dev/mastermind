from mastermind.core.colors import Color

def feedback(original: list[Color], answer: list[Color]) -> tuple[int, int]:

    if len(original) != 4:
        raise ValueError("original should be of length 4")
    if len(answer) != 4:
        raise ValueError("answer should be of length 4")

    correct_pos_and_color: int = 0
    correct_color: int = 0

    for idx, color in enumerate(answer):
        if original[idx] == color:
            correct_pos_and_color += 1
        elif color in original:
            correct_color += 1

    return correct_pos_and_color, correct_color

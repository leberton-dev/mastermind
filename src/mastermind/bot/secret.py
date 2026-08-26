import random

from mastermind.core.colors import Color


def random_code() -> list[Color]:
    code: list[Color] = []
    for _ in range(4):
        code.append(Color(random.randint(1, 6)))
    return code


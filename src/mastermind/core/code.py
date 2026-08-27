import random

from mastermind.core.colors import Color
from mastermind.core.feedback import Feedback


class Code:
    _LENGTH: int = 4

    def __init__(self, colors: list[Color]) -> None:
        if len(colors) != self._LENGTH:
            raise ValueError(f"Code must have {self._LENGTH} pegs")
        self._colors: list[Color] = list(colors)


    @classmethod
    def blank(cls) -> "Code":
        return cls([Color.WHITE] * 4)


    @classmethod
    def random(cls) -> "Code":
        return cls([Color(random.randint(1, 6)) for _ in range(cls._LENGTH)])


    def feedback(self, other: "Code") -> Feedback:
        secret: list[Color] = [c for c in self]
        guess: list[Color] = [c for c in other]

        black_pegs: int = self._calculate_black_pegs(secret, guess)
        white_pegs: int = self._calculate_white_pegs(secret, guess)

        return Feedback(black_pegs, white_pegs)


    def cycle(self, idx: int, direction: int) -> None:
        direction = 1 if direction > 0 else -1 if direction < 0 else 0
        new_idx = (self._colors[idx].value - 1 + direction) % len(Color)
        self._colors[idx] = Color(new_idx + 1)


    def __iter__(self):
        return iter(self._colors)

    def __getitem__(self, idx: int) -> Color:
        return self._colors[idx]

    def __len__(self) -> int:
        return len(self._colors)


    def _calculate_black_pegs(self, secret: list[Color], guess: list[Color]) -> int:
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


    def _calculate_white_pegs(self, secret: list[Color], guess: list[Color]) -> int:
        white_pegs: int = 0

        for gcolor in guess:
            for scolor in secret:
                if gcolor == scolor:
                    white_pegs += 1
                    secret.remove(scolor)

                    break

        return white_pegs

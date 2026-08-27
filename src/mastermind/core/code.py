import random

from mastermind.core.colors import Color


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

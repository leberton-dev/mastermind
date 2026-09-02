import random
from typing import override

from mastermind_kernel.colors import PegColor
from mastermind_kernel.feedback import CodeFeedback


class Code:
    _PEG_COUNT: int = 4

    def __init__(self, colors: list[PegColor]) -> None:
        if len(colors) != self._PEG_COUNT:
            raise ValueError(f"Code must have {self._PEG_COUNT} pegs")
        self._pegs: list[PegColor] = list(colors)


    @property
    def pegs(self) -> list[PegColor]:
        return self._pegs


    @classmethod
    def blank(cls) -> "Code":
        return cls([PegColor.WHITE] * 4)


    @classmethod
    def random(cls) -> "Code":
        return cls([PegColor(random.randint(1, 6)) for _ in range(cls._PEG_COUNT)])


    def feedback(self, other: "Code") -> CodeFeedback:
        secret: list[PegColor] = [c for c in self]
        guess: list[PegColor] = [c for c in other]

        black_pegs: int = self._count_black_pegs(secret, guess)
        white_pegs: int = self._count_white_pegs(secret, guess)

        return CodeFeedback(black_pegs, white_pegs)


    def cycle(self, idx: int, direction: int) -> None:
        direction = 1 if direction > 0 else -1 if direction < 0 else 0
        new_idx = (self._pegs[idx].value - 1 + direction) % len(PegColor)
        self._pegs[idx] = PegColor(new_idx + 1)


    def __iter__(self):
        return iter(self._pegs)

    def __getitem__(self, idx: int) -> PegColor:
        return self._pegs[idx]

    def __len__(self) -> int:
        return len(self._pegs)

    @override
    def __eq__(self, other: "Code") -> bool:
        if not isinstance(other, Code):
            return NotImplemented

        return self._pegs == other._pegs


    def _count_black_pegs(self, secret: list[PegColor], guess: list[PegColor]) -> int:
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


    def _count_white_pegs(self, secret: list[PegColor], guess: list[PegColor]) -> int:
        white_pegs: int = 0

        for gcolor in guess:
            for scolor in secret:
                if gcolor == scolor:
                    white_pegs += 1
                    secret.remove(scolor)

                    break

        return white_pegs

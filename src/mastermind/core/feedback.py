from typing import NamedTuple


class Feedback(NamedTuple):
    black: int
    white: int

    @property
    def won(self) -> bool:
        return self.black == 4 and self.white == 0


from typing import NamedTuple


class CodeFeedback(NamedTuple):
    black_pegs: int
    white_pegs: int

    @property
    def won(self) -> bool:
        return self.black_pegs == 4 and self.white_pegs == 0


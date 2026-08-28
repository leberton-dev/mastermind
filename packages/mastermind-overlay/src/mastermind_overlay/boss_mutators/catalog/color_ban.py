import random
from typing import override

from mastermind_kernel.colors import PegColor

from mastermind_overlay.boss_mutators.mutator import BossMutator


class ColorBan(BossMutator):
    def __init__(self) -> None:
        self._banned_color: PegColor = random.choice(list(PegColor))

    @property
    def banned_color(self) -> PegColor:
        return self._banned_color

    @property
    @override
    def description(self) -> str:
        return f"{self._banned_color.name.title()} is banned this round"


    def allowed_colors(self) -> set[PegColor] | None:
        return set(PegColor) - {self._banned_color}



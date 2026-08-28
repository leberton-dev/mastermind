from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from mastermind_kernel.colors import PegColor
from mastermind_kernel.feedback import CodeFeedback

if TYPE_CHECKING:
    from mastermind_overlay.run.gamestate import GameState


class BossMutator(ABC):
    @property
    @abstractmethod
    def description(self) -> str: ...


    def transform_feedback(self, feedback: CodeFeedback) -> CodeFeedback:
        return feedback


    def allowed_colors(self) -> set[PegColor] | None:
        return None


    def on_round_start(self, state: GameState) -> None:
        pass


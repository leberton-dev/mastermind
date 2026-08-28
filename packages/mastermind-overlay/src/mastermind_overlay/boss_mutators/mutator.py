from abc import ABC, abstractmethod

from mastermind_kernel.colors import PegColor
from mastermind_kernel.feedback import CodeFeedback

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


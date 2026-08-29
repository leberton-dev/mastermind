from typing import Protocol, Sequence

from mastermind_kernel.feedback import CodeFeedback
from mastermind_overlay.scoring.points import Points


class ScoringStage(Protocol):
    def on_guess(self, points: Points, mult: int, feedback: CodeFeedback) -> tuple[Points, int]: ...


class ScoringPipeline:
    def __init__(self, stages: Sequence[ScoringStage]) -> None:
        self._stages: Sequence[ScoringStage] = stages


    def run(self, points: Points, mult: int, feedback: CodeFeedback) -> tuple[Points, int]:
        for stage in self._stages:
            points, mult = stage.on_guess(points, mult, feedback)
        return points, mult

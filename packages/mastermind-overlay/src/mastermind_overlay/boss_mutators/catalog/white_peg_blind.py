from typing import override

from mastermind_kernel.feedback import CodeFeedback

from mastermind_overlay.boss_mutators.mutator import BossMutator


class WhitePegBlind(BossMutator):
    @property
    @override
    def description(self) -> str:
        return "White pegs are hidden this round"


    @override
    def transform_feedback(self, feedback: CodeFeedback) -> CodeFeedback:
        return feedback._replace(white_pegs=0)

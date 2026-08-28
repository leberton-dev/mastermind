from dataclasses import dataclass

from mastermind.core.feedback import CodeFeedback


@dataclass
class Points:
    value: int


def compute_points(feedback: CodeFeedback) -> Points:
    return Points(feedback.black_pegs * 2 + feedback.white_pegs)


def apply_multiplier(points: Points, multiplier: int) -> int:
    return points.value * multiplier

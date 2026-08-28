from mastermind_overlay.relics.relic import RelicGrade, RelicSpec
from mastermind_overlay.scoring.points import Points

SPEC = RelicSpec(
    "points_double_on_win",
    "Double the points on a winning guess",
    RelicGrade.EXPERT,
    lambda points, mult, fb: (Points(points.value * 2), mult) if fb.won else (points, mult),
)

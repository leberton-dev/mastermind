from mastermind_overlay.relics.relic import RelicGrade, RelicSpec
from mastermind_overlay.scoring.points import Points

SPEC = RelicSpec(
    "points_plus_one",
    "Add +1 to the points",
    RelicGrade.STANDARD,
    lambda points, mult, fb: (Points(points.value + 1), mult),
)

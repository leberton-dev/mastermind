from mastermind_overlay.relics.relic import RelicGrade, RelicSpec
from mastermind_overlay.scoring.points import Points

SPEC = RelicSpec(
    "points_per_peg",
    "Add +1 to the points for each peg",
    RelicGrade.STANDARD,
    lambda points, mult, fb: (Points(points.value + fb.black_pegs + fb.white_pegs), mult),
)

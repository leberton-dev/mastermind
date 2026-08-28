from mastermind_overlay.relics.relic import RelicGrade, RelicSpec
from mastermind_overlay.scoring.points import Points

SPEC = RelicSpec(
    "points_white_as_black",
    "Count white pegs as black pegs for points calculation",
    RelicGrade.EXPERT,
    lambda points, mult, fb: (Points(points.value + fb.white_pegs), mult),
)

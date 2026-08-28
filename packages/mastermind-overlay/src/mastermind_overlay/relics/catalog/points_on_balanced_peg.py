from mastermind_overlay.relics.relic import RelicGrade, RelicSpec
from mastermind_overlay.scoring.points import Points

SPEC = RelicSpec(
    "points_on_balanced_peg",
    "Add +2 to the points if black pegs equal white pegs",
    RelicGrade.STANDARD,
    lambda points, mult, fb: (points, mult) if fb.black_pegs != fb.white_pegs else (Points(points.value + 2), mult),
)

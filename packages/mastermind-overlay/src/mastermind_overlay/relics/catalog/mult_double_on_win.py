from mastermind_overlay.relics.relic import RelicGrade, RelicSpec

SPEC = RelicSpec(
    "mult_double_on_win",
    "Double the multiplier on a winning guess",
    RelicGrade.ADVANCED,
    lambda points, mult, fb: (points, mult * 2) if fb.won else (points, mult),
)

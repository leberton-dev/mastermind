from mastermind_overlay.relics.relic import RelicGrade, RelicSpec

SPEC = RelicSpec(
    "mult_plus_one",
    "Add +1 to the multiplier",
    RelicGrade.STANDARD,
    lambda points, mult, fb: (points, mult + 1),
)

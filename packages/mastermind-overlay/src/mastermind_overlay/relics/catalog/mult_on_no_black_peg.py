from mastermind_overlay.relics.relic import RelicGrade, RelicSpec

SPEC = RelicSpec(
    "mult_on_no_black_peg",
    "Add +1 to the multiplier if the guess has no black pegs",
    RelicGrade.STANDARD,
    lambda points, mult, fb: (points, mult) if fb.black_pegs > 0 else (points, mult + 1),
)

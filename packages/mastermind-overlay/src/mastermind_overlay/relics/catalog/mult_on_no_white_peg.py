from mastermind_overlay.relics.relic import RelicGrade, RelicSpec

SPEC = RelicSpec(
    "mult_on_no_white_peg",
    "Add +1 to the multiplier if the guess has no white pegs",
    RelicGrade.ADVANCED,
    lambda points, mult, fb: (points, mult) if fb.white_pegs != 0 else (points, mult + 1),
)

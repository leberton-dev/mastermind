from mastermind_overlay.relics.catalog import (
    mult_double_on_win,
    mult_on_no_black_peg,
    mult_on_no_white_peg,
    mult_plus_one,
    points_double_on_win,
    points_on_balanced_peg,
    points_per_black_peg,
    points_per_peg,
    points_per_white_peg,
    points_plus_one,
    points_white_as_black,
)
from mastermind_overlay.relics.relic import RelicSpec

RELICS: list[RelicSpec] = [
    mult_plus_one.SPEC,
    points_plus_one.SPEC,
    points_per_black_peg.SPEC,
    points_per_white_peg.SPEC,
    points_per_peg.SPEC,
    mult_on_no_black_peg.SPEC,
    points_on_balanced_peg.SPEC,
    mult_double_on_win.SPEC,
    mult_on_no_white_peg.SPEC,
    points_white_as_black.SPEC,
    points_double_on_win.SPEC,
]

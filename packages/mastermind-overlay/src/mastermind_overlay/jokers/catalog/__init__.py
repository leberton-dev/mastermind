from mastermind_overlay.jokers.catalog import (
    multicolor,
    lucky,
    greedy,
    gambler,
)
from mastermind_overlay.jokers.jokers import JokerSpec

JOKERS: list[JokerSpec] = [
    multicolor.SPEC,
    lucky.SPEC,
    greedy.SPEC,
    gambler.SPEC,
]

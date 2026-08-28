from mastermind_overlay.boss_mutators.catalog.color_ban import ColorBan
from mastermind_overlay.boss_mutators.catalog.white_peg_blind import WhitePegBlind
from mastermind_overlay.boss_mutators.mutator import BossMutator


BOSS_MUTATORS: list[type[BossMutator]] = [
    ColorBan,
    WhitePegBlind,
]


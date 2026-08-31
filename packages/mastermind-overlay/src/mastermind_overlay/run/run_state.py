import random

from mastermind_overlay.economy.currency import reward_for
from mastermind_overlay.events.bus import EventBus
from mastermind_overlay.events.catalog.round_started import RoundStarted
from mastermind_overlay.relics.relic import Relic
from mastermind_overlay.run.gamestate import GameState
from mastermind_overlay.run.round_tier import RoundTier
from mastermind_overlay.boss_mutators.catalog import BOSS_MUTATORS
from mastermind_overlay.boss_mutators.mutator import BossMutator


class RunState:
    _BASE_TARGET_SCORE: int = 9
    _BASE_GAMESTATE_MAX_TURNS: int = 10
    _TARGET_SCORE_GROWTH: float = 1.24
    _TIER_ORDER: tuple[RoundTier, ...] = (RoundTier.STANDARD, RoundTier.HARDENED, RoundTier.FINAL)
    _MAX_RUN_STAGES: int = 2


    def __init__(self) -> None:
        self._stage: int = 1
        self._relics: list[Relic] = []
        self._max_relics: int = 5
        self._currency: int = 0
        self._tier_idx: int = 0
        self._events: EventBus = EventBus()


    @property
    def stage(self) -> int:
        return self._stage

    @property
    def currency(self) -> int:
        return self._currency

    @property
    def relics(self) -> list[Relic]:
        return self._relics

    @property
    def tier(self) -> RoundTier:
        return self._TIER_ORDER[self._tier_idx]

    @property
    def events(self) -> EventBus:
        return self._events

    @property
    def max_relics(self) -> int:
        return self._max_relics

    @property
    def run_over(self) -> bool:
        return self._stage >= self._MAX_RUN_STAGES


    def advance_round_tier(self) -> None:
        self._tier_idx += 1
        if self._tier_idx >= len(self._TIER_ORDER):
            self._tier_idx = 0
            self._stage += 1


    def reward_round(self, state: GameState) -> None:
        margin = state.score - state.target_score
        self._currency += reward_for(state.turns_left, margin)


    def new_round(self) -> GameState:
        stage_base = self._BASE_TARGET_SCORE * self._TARGET_SCORE_GROWTH ** (self._stage - 1)
        target = round(stage_base * self.tier.multiplier)
        mutator: BossMutator | None = self._pick_mutator() if self.tier.is_final else None
        self._events.publish(RoundStarted(self.tier))
        return GameState(self._BASE_GAMESTATE_MAX_TURNS, target, self._relics, mutator)


    def _pick_mutator(self) -> BossMutator:
        return random.choice(BOSS_MUTATORS)()


    def spend(self, amount: int) -> None:
        self._currency -= amount


    def refund(self, amount: int) -> None:
        self._currency += amount


    def add_relic(self, relic: Relic) -> bool:
        if len(self._relics) >= self._max_relics:
            return False
        self._relics.append(relic)
        return True


    def sell_relic(self, relic: Relic) -> bool:
        if len(self._relics) == 0:
            return False
        self._relics.remove(relic)
        return True

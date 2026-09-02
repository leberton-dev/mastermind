import random

from mastermind_overlay.economy.currency import reward_for
from mastermind_overlay.events.bus import EventBus
from mastermind_overlay.events.catalog.round_started import RoundStarted
from mastermind_overlay.jokers.jokers import Joker
from mastermind_overlay.relics.relic import Relic
from mastermind_overlay.run.gamestate import GameState
from mastermind_overlay.run.round_tier import RoundTier
from mastermind_overlay.boss_mutators.catalog import BOSS_MUTATORS
from mastermind_overlay.boss_mutators.mutator import BossMutator


class RunState:
    _BASE_MAX_TURNS: int = 10
    _BASE_TARGET_SCORE: int = 15
    _TARGET_SCORE_GROWTH: float = 1.8
    _TIER_ORDER: tuple[RoundTier, ...] = (RoundTier.STANDARD, RoundTier.HARDENED, RoundTier.FINAL)
    _MAX_RUN_STAGES: int = 2


    def __init__(self) -> None:
        self._stage: int = 1
        self._relics: list[Relic] = []
        self._jokers: list[Joker] = []
        self._max_relics: int = 5
        self._currency: int = 30
        self._tier_idx: int = 0
        self._events: EventBus = EventBus()
        self._max_run_stages: int = self._MAX_RUN_STAGES


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
    def jokers(self) -> list[Joker]:
        return self._jokers

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
        return self.stage >= self._max_run_stages + 1


    def set_max_stages(self, amount: int) -> None:
        if amount <= self._max_run_stages:
            return
        self._max_run_stages = amount


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
        target_score = round(stage_base * self.tier.multiplier)
        max_turns = round(self._BASE_MAX_TURNS - (self._stage - 1))
        mutator: BossMutator | None = self._pick_mutator() if self.tier.is_final else None
        self._events.publish(RoundStarted(self.tier))
        return GameState(max_turns, target_score, self._relics, self._jokers, mutator)


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


    def add_joker(self, joker: Joker) -> bool:
        self._jokers.append(joker)
        return True


    def sell_relic(self, relic: Relic) -> bool:
        if len(self._relics) == 0:
            return False
        self._relics.remove(relic)
        return True

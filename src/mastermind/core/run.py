from mastermind.core.round_tier import RoundTier
from mastermind.core.currency import reward_for
from mastermind.core.gamestate import GameState
from mastermind.core.relic import Relic


class RunState:
    _BASE_TARGET_SCORE: int = 9
    _BASE_MAX_TURNS: int = 10
    _TARGET_SCORE_GROWTH: float = 1.24
    _TIER_ORDER: tuple[RoundTier, ...] = (RoundTier.STANDARD, RoundTier.HARDENED, RoundTier.FINAL)


    def __init__(self) -> None:
        self._stage: int = 1
        self._relics: list[Relic] = []
        self._max_relics: int = 5
        self._currency: int = 0
        self._tier_idx: int = 0


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
    def max_relics(self) -> int:
        return self._max_relics


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
        return GameState(self._BASE_MAX_TURNS, target, self._relics)


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

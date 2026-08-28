from mastermind.core.gamestate import GameState
from mastermind.core.relic import Relic
from mastermind.core.currency import reward_for
from mastermind.core.blind import Blind


class RunState:
    _BASE_TARGET_SCORE: int = 9
    _BASE_MAX_TURNS: int = 10
    _TARGET_SCORE_GROWTH: float = 1.24
    _BLIND_ORDER: tuple[Blind, ...] = (Blind.SMALL, Blind.BIG, Blind.BOSS)


    def __init__(self) -> None:
        self._ante: int = 1
        self._relics: list[Relic] = []
        self._currency: int = 0
        self._blind_idx: int = 0


    @property
    def ante(self) -> int:
        return self._ante

    @property
    def currency(self) -> int:
        return self._currency

    @property
    def relics(self) -> list[Relic]:
        return self._relics

    @property
    def blind(self) -> Blind:
        return self._BLIND_ORDER[self._blind_idx]


    def advance_blind(self) -> None:
        self._blind_idx += 1
        if self._blind_idx >= len(self._BLIND_ORDER):
            self._blind_idx = 0
            self._ante += 1


    def reward_round(self, state: GameState) -> None:
        margin = state.score - state.target_score
        self._currency += reward_for(state.turns_left, margin)


    def new_round(self) -> GameState:
        ante_base = self._BASE_TARGET_SCORE * self._TARGET_SCORE_GROWTH ** (self._ante - 1)
        target = round(ante_base * self.blind.multiplier)
        return GameState(self._BASE_MAX_TURNS, target, self._relics)

    
    def spend(self, amount: int) -> None:
        self._currency -= amount


    def add_relic(self, relic: Relic) -> None:
        self._relics.append(relic)

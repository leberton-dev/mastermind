from mastermind.core.gamestate import GameState
from mastermind.core.relic import Relic, MultPlusOneRelic


class RunState:
    def __init__(self) -> None:
        self._ante: int = 1
        self._relics: list[Relic] = [MultPlusOneRelic()]


    @property
    def ante(self) -> int:
        return self._ante


    def advance_ante(self) -> None:
        self._ante += 1


    def new_round(self) -> GameState:
        return GameState(10, 5, self._relics)


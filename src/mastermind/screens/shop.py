import random
from typing import override

from mastermind.core.run import RunState
from mastermind.engine.input_event import InputEvent
from mastermind.engine.renderer import Renderer
from mastermind.engine.screen import Screen
from mastermind.engine.screen_queue import ScreenQueue
from mastermind.engine.transition import ScreenTransition
from mastermind.core.relic import (
    ChipPerBlackPegRelic,
    ChipPerWhitePegRelic,
    ChipPlusOneRelic,
    MultPlusOneRelic,
    Relic,
)

_RELIC_PRICE = 10
_OFFER_SIZE: int = 3

_RELIC_CLASSES: tuple[type[Relic], ...] = (
    MultPlusOneRelic,
    ChipPlusOneRelic,
    ChipPerBlackPegRelic,
    ChipPerWhitePegRelic,
)

def generate_offer(owned: list[Relic]) -> list[Relic]:
    owned_types = {type(relic) for relic in owned}
    available = [cls for cls in _RELIC_CLASSES if cls not in owned_types]
    count = min(_OFFER_SIZE, len(available))
    return [cls() for cls in random.sample(available, count)]

class ShopScreen(Screen):
    def __init__(self, queue: ScreenQueue, renderer: Renderer, run_state: RunState) -> None:
        super().__init__(queue, False)
        self._renderer: Renderer = renderer
        self._run_state: RunState = run_state
        self._offer: list[Relic] = generate_offer(run_state.relics)
        self._current: int = 0


    @override
    def handle_input(self, event: InputEvent) -> None:
        leave_idx = len(self._offer)

        if  event == InputEvent.UP:
            self._current = (self._current - 1) % (leave_idx + 1)
        if  event == InputEvent.DOWN:
            self._current = (self._current + 1) % (leave_idx + 1)
        if event == InputEvent.CONFIRM:
            if self._current == leave_idx:
                self._queue.push(ScreenTransition.pop())
            else:
                self._buy_selected()
        if event == InputEvent.QUIT:
            self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass

    @override
    def render(self) -> None:
        self._renderer.render_shop(self._run_state.currency, self._offer, _RELIC_PRICE, self._current)


    def _buy_selected(self) -> None:
        if self._run_state.currency < _RELIC_PRICE:
            return

        relic = self._offer[self._current]
        self._run_state.spend(_RELIC_PRICE)
        self._run_state.add_relic(relic)
        del self._offer[self._current]

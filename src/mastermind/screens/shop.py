import random
from typing import override

from mastermind.core.gamestate import GameState
from mastermind.core.relic import RELICS, Relic
from mastermind.core.run import RunState
from mastermind.engine.input_event import InputEvent
from mastermind.engine.renderer import Renderer
from mastermind.engine.screen import Screen
from mastermind.engine.screen_queue import ScreenQueue
from mastermind.engine.transition import ScreenTransition

_RELIC_PRICE: int = 10
_OFFER_SIZE: int = 3
_EXTRA_GUESS_PRICE: int = 8

def generate_offer(owned: list[Relic]) -> list[Relic]:
    owned_keys = {relic.spec.key for relic in owned}
    available = [spec for spec in RELICS if spec.key not in owned_keys]
    count = min(_OFFER_SIZE, len(available))
    return [Relic(spec) for spec in random.sample(available, count)]


class ShopScreen(Screen):
    def __init__(self, queue: ScreenQueue, renderer: Renderer, run_state: RunState, next_state: GameState) -> None:
        super().__init__(queue, True)
        self._renderer: Renderer = renderer
        self._run_state: RunState = run_state
        self._next_state: GameState = next_state
        self._offer: list[Relic] = generate_offer(run_state.relics)
        self._current: int = 0


    @override
    def handle_input(self, event: InputEvent) -> None:
        owned_count = len(self._run_state.relics)
        extra_guess_idx = owned_count + len(self._offer)
        leave_idx = extra_guess_idx + 1

        if  event == InputEvent.LEFT:
            self._current = (self._current - 1) % (leave_idx + 1)
        if  event == InputEvent.RIGHT:
            self._current = (self._current + 1) % (leave_idx + 1)
        if event == InputEvent.CONFIRM:
            if self._current < owned_count:
                self._sell_relic()
            elif self._current < extra_guess_idx:
                self._buy_relic()
            elif self._current == extra_guess_idx:
                self._buy_extra_guess()
            else:
                self._queue.push(ScreenTransition.pop())
        if event == InputEvent.QUIT:
            self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass

    @override
    def render(self) -> None:
        self._renderer.render_shop(
            self._run_state.currency,
            self._offer,
            _EXTRA_GUESS_PRICE,
            self._current,
            self._run_state.relics,
            self._run_state.max_relics,
        )


    def _buy_relic(self) -> None:
        offer_idx = self._current - len(self._run_state.relics)
        relic = self._offer[offer_idx]
        if self._run_state.currency < relic.price:
            return

        if not self._run_state.add_relic(relic):
            return
        self._run_state.spend(relic.price)
        del self._offer[offer_idx]


    def _sell_relic(self) -> None:
        relic = self._run_state.relics[self._current]
        if not self._run_state.sell_relic(relic):
            return
        self._run_state.spend(-(relic.price // 2))


    def _buy_extra_guess(self) -> None:
        if self._run_state.currency < _EXTRA_GUESS_PRICE:
            return

        self._run_state.spend(_EXTRA_GUESS_PRICE)
        self._next_state.add_turn()

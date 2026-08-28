import random
from typing import override

from mastermind_overlay.relics.catalog import RELICS
from mastermind_overlay.relics.relic import Relic
from mastermind_overlay.run.gamestate import GameState
from mastermind_overlay.run.run_state import RunState

from mastermind.engine.input_event import InputEvent
from mastermind.engine.renderer import Renderer
from mastermind.engine.screen import Screen
from mastermind.engine.screen_queue import ScreenQueue
from mastermind.engine.transition import ScreenTransition

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
        self._cursor: int = 0


    @override
    def handle_input(self, event: InputEvent) -> None:
        owned_count = len(self._run_state.relics)
        extra_guess_idx = owned_count + len(self._offer)
        leave_idx = extra_guess_idx + 1

        if  event == InputEvent.LEFT:
            self._cursor = (self._cursor - 1) % (leave_idx + 1)
        if  event == InputEvent.RIGHT:
            self._cursor = (self._cursor + 1) % (leave_idx + 1)
        if event == InputEvent.CONFIRM:
            if self._cursor < owned_count:
                self._sell_relic()
            elif self._cursor < extra_guess_idx:
                self._buy_relic()
            elif self._cursor == extra_guess_idx:
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
            self._cursor,
            self._run_state.relics,
            self._run_state.max_relics,
        )


    def _buy_relic(self) -> None:
        offer_idx = self._cursor - len(self._run_state.relics)
        relic = self._offer[offer_idx]
        if self._run_state.currency < relic.price:
            return

        if not self._run_state.add_relic(relic):
            return
        self._run_state.spend(relic.price)
        del self._offer[offer_idx]


    def _sell_relic(self) -> None:
        relic = self._run_state.relics[self._cursor]
        if not self._run_state.sell_relic(relic):
            return
        self._run_state.refund(relic.price // 2)


    def _buy_extra_guess(self) -> None:
        if self._run_state.currency < _EXTRA_GUESS_PRICE:
            return

        self._run_state.spend(_EXTRA_GUESS_PRICE)
        self._next_state.add_turn()

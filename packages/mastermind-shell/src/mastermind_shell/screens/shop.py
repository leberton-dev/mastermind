import random
from typing import override

from mastermind_overlay.events.catalog.shop_entered import ShopEntered
from mastermind_overlay.relics.catalog import RELICS
from mastermind_overlay.relics.relic import Relic
from mastermind_overlay.run.gamestate import GameState
from mastermind_overlay.run.run_state import RunState

from mastermind_shell.engine.input_event import InputEvent
from mastermind_shell.engine.renderer import Renderer
from mastermind_shell.engine.screen import Screen
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.transition import ScreenTransition
from mastermind_shell.screens.boss_announcement import BossAnnouncementScreen
from mastermind_shell.screens.joker_booster import JokerBoosterShop

_OFFER_SIZE: int = 3
_EXTRA_GUESS_PRICE: int = 8
_JOKER_PRICE: int = 25

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
        run_state.events.publish(ShopEntered())


    @override
    def handle_input(self, event: InputEvent) -> None:
        owned_count = len(self._run_state.relics)
        extra_guess_idx = owned_count + len(self._offer)
        reroll_idx = extra_guess_idx + 1
        jokers_idx = reroll_idx + 1
        leave_idx = jokers_idx + 1

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
            elif self._cursor == reroll_idx:
                self._reroll_offers()
            elif self._cursor == jokers_idx:
                self._buy_joker()
            else:
                self._queue.push(ScreenTransition.pop())
                if self._next_state.mutator is not None:
                    self._queue.push(ScreenTransition.push(
                        BossAnnouncementScreen(self._queue, self._renderer, self._next_state.mutator)
                    ))
        if event == InputEvent.QUIT:
            if self._next_state.mutator is not None:
                self._queue.push(ScreenTransition.push(
                    BossAnnouncementScreen(self._queue, self._renderer, self._next_state.mutator)
                ))
                self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass

    @override
    def render(self) -> None:
        reroll_price = 5

        self._renderer.render_shop(
            self._run_state.currency,
            self._offer,
            _EXTRA_GUESS_PRICE,
            self._cursor,
            self._run_state.relics,
            self._run_state.max_relics,
            reroll_price,
            _JOKER_PRICE,
        )


    def _reroll_offers(self) -> None:
        if self._run_state.currency < 5:
            return
        self._run_state.spend(5)
        self._offer = generate_offer(self._run_state.relics)


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


    def _buy_joker(self) -> None:
        if self._run_state.currency < _JOKER_PRICE:
            return

        self._run_state.spend(_JOKER_PRICE)
        self._queue.push(ScreenTransition.push(JokerBoosterShop(self._queue, self._renderer, self._run_state)))


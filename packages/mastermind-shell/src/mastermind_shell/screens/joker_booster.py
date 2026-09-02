import random
from typing import override

from mastermind_overlay.jokers.catalog import JOKERS
from mastermind_overlay.jokers.jokers import Joker
from mastermind_overlay.run.run_state import RunState
from mastermind_shell.engine.input_event import InputEvent
from mastermind_shell.engine.renderer import Renderer
from mastermind_shell.engine.screen import Screen
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.transition import ScreenTransition, TransitionKind


def generate_jokers() -> list[Joker]:
    available = [spec for spec in JOKERS]
    return [Joker(spec) for spec in random.sample(available, 5)]


class JokerBoosterShop(Screen):
    def __init__(self, queue: ScreenQueue, renderer: Renderer, run_state: RunState) -> None:
        super().__init__(queue, True)
        self._renderer: Renderer = renderer
        self._run_state: RunState = run_state
        self._cursor: int = 0
        self._jokers: list[Joker] = generate_jokers()


    @override
    def handle_input(self, event: InputEvent) -> None:
        if event == InputEvent.LEFT:
            self._cursor = (self._cursor - 1) % 5
        if event == InputEvent.RIGHT:
            self._cursor = (self._cursor + 1) % 5
        if event == InputEvent.CONFIRM:
            self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        self._renderer.render_joker_booster(self._jokers, self._cursor)


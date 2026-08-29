from typing import override

from mastermind_overlay.boss_mutators.mutator import BossMutator
from mastermind_shell.engine.input_event import InputEvent
from mastermind_shell.engine.renderer import Renderer
from mastermind_shell.engine.screen import Screen
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.transition import ScreenTransition


class BossAnnouncementScreen(Screen):
    def __init__(self, queue: ScreenQueue, renderer: Renderer, mutator: BossMutator) -> None:
        super().__init__(queue, True)
        self._renderer: Renderer = renderer
        self._mutator: BossMutator = mutator


    @override
    def handle_input(self, event: InputEvent) -> None:
        self._queue.push(ScreenTransition.pop())


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        self._renderer.render_boss_announcement("BOSS ROUND", self._mutator.description)

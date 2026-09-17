from typing import override

from mastermind_overlay.run.run_state import RunState

from mastermind_shell.engine.input_event import InputEvent
from mastermind_shell.engine.renderer import Renderer
from mastermind_shell.engine.screen import Screen
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.transition import ScreenTransition
from mastermind_shell.screens.gameplay import GameplayScreen


class MenuScreen(Screen):

    def __init__(self, queue: ScreenQueue, renderer: Renderer) -> None:
        super().__init__(queue, True)
        self._renderer: Renderer = renderer
        self._current: int = 0
        self._run_state: RunState = RunState()


    @override
    def handle_input(self, event: InputEvent) -> None:
        if event == InputEvent.QUIT:
            self._queue.push(ScreenTransition.quit())
        if event == InputEvent.CONFIRM:
            if self._current == 0:
                gameplay_screen = GameplayScreen(self._queue, self._renderer, self._run_state)
                self._queue.push(ScreenTransition.push(gameplay_screen))
            elif self._current == 1:
                self._queue.push(ScreenTransition.quit())
        if event == InputEvent.PLAY:
            gameplay_screen = GameplayScreen(self._queue, self._renderer, self._run_state)
            self._queue.push(ScreenTransition.push(gameplay_screen))
        if event == InputEvent.EXIT:
            self._queue.push(ScreenTransition.quit())
        if event == InputEvent.UP:
            self._current = (self._current + 1) % 2
        if event == InputEvent.DOWN:
            self._current = (self._current - 1) % 2


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        self._renderer.render_menu(self._current)


from typing import override

from mastermind_overlay.run.run_state import RunState

from mastermind_shell.engine.input_event import InputEvent
from mastermind_shell.engine.renderer import Renderer
from mastermind_shell.engine.screen import Screen
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.transition import ScreenTransition
from mastermind_shell.screens.gameplay import GameplayScreen


class MenuScreen(Screen):
    _PLAY_STR: str = """
   ___  __   _____  __
  / _ \\/ /  / _ \\ \\/ /
 / ___/ /__/ __ |\\  /
/_/  /____/_/ |_|/_/
"""

    _QUIT_STR: str = """
   ___  _   _ ___ _____
  / _ \\| | | |_ _|_   _|
 | (_) | |_| || |  | |
  \\__\\_\\\\___/|___| |_|
"""

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
        if event == InputEvent.UP:
            self._current = (self._current + 1) % 2
        if event == InputEvent.DOWN:
            self._current = (self._current - 1) % 2


    @override
    def update(self) -> None:
        pass


    @override
    def render(self) -> None:
        self._renderer.clear()

        lines, _ = self._renderer.dimensions()

        height_play = 0
        for _ in self._PLAY_STR.strip("\n").splitlines():
            height_play += 1

        start_y = (lines // 2) - height_play - 1
        self._render_big_str(start_y, self._PLAY_STR, self._current == 0)
        start_y += height_play + 1
        self._render_big_str(start_y, self._QUIT_STR, self._current == 1)

        self._renderer.refresh()


    def _render_big_str(self, start_y: int, big_text: str, highlighted: bool) -> None:
        lines_list = big_text.strip('\n').splitlines()
        max_len = max(len(line) for line in lines_list)
        _, cols = self._renderer.dimensions()
        start_x = (cols - max_len) // 2

        for line in lines_list:
            self._renderer.draw_text(start_y, start_x, line, highlighted)
            start_y += 1

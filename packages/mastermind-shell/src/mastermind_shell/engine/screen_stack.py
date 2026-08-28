from mastermind_shell.engine.input_source import InputSource
from mastermind_shell.engine.screen import Screen
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.transition import TransitionKind


class ScreenStack:
    def __init__(self, input_source: InputSource, queue: ScreenQueue, initial: Screen) -> None:
        self._input_source: InputSource = input_source
        self._queue: ScreenQueue = queue
        self._screens: list[Screen] = [initial]
        self._running: bool = True


    @property
    def top(self) -> Screen:
        return self._screens[-1]


    def push(self, screen: Screen) -> None:
        self._screens.append(screen)
        self.top.on_enter()


    def pop(self) -> None:
        self.top.on_exit()
        self._screens.remove(self.top)


    def render(self) -> None:
        first_no_opaque_idx = 0

        for i, screen in enumerate(reversed(self._screens)):
            if screen.opaque:
                first_no_opaque_idx = len(self._screens) - i - 1
                break

        for i in range(first_no_opaque_idx, len(self._screens)):
            self._screens[i].render()


    def step(self) -> bool:
        self.render()
        event = self._input_source.next_event()

        if event is not None:
            self.top.handle_input(event)
        self.top.update()

        for transition in self._queue.drain():
            match transition.kind:
                case TransitionKind.PUSH:
                    assert transition.screen is not None
                    self.push(transition.screen)
                case TransitionKind.POP:
                    self.pop()
                case TransitionKind.QUIT:
                    self._running = False

        return self._running

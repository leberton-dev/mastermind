import curses

from mastermind.screens.queue import ScreenQueue
from mastermind.screens.screen import Screen
from mastermind.screens.transition import TransitionKind


class ScreenStack:
    def __init__(self, stdscr: curses.window, queue: ScreenQueue, initial: Screen) -> None:
        self._stdscr: curses.window = stdscr
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
        key = self._stdscr.getch()
        self.top.handle_input(key)
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


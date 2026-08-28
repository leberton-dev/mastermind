from mastermind_shell.engine.transition import ScreenTransition


class ScreenQueue:
    def __init__(self) -> None:
        self._pending: list[ScreenTransition] = []


    def push(self, transition: ScreenTransition) -> None:
        self._pending.append(transition)


    def drain(self) -> list[ScreenTransition]:
        pending = self._pending
        self._pending = []
        return pending

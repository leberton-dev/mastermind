import curses

from mastermind.engine.input_event import InputEvent

_DIRECTION_KEYS: dict[int, InputEvent] = {
    curses.KEY_UP: InputEvent.UP,
    curses.KEY_DOWN: InputEvent.DOWN,
    curses.KEY_LEFT: InputEvent.LEFT,
    curses.KEY_RIGHT: InputEvent.RIGHT,
}


def keycode_to_event(key: int) -> InputEvent | None:
    if key in _DIRECTION_KEYS:
        return _DIRECTION_KEYS[key]
    if key == curses.KEY_ENTER or key == ord('\n') or key == ord('\r'):
        return InputEvent.CONFIRM
    if key == ord('q'):
        return InputEvent.QUIT
    return None

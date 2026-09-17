import pygame

from mastermind_shell.engine.input_event import InputEvent

_DIRECTION_KEYS: dict[int, InputEvent] = {
    pygame.K_UP: InputEvent.UP,
    pygame.K_DOWN: InputEvent.DOWN,
    pygame.K_LEFT: InputEvent.LEFT,
    pygame.K_RIGHT: InputEvent.RIGHT,
}


def keycode_to_event(key: int) -> InputEvent | None:
    if key in _DIRECTION_KEYS:
        return _DIRECTION_KEYS[key]
    if key == pygame.K_RETURN:
        return InputEvent.CONFIRM
    if key == pygame.K_q:
        return InputEvent.QUIT
    return None

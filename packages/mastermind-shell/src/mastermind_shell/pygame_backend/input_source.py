import pygame
import pygame_gui

from mastermind_shell.pygame_backend.keymap import keycode_to_event
from mastermind_shell.engine.input_event import InputEvent


class PygameInputSource:
    def __init__(self, manager: pygame_gui.UIManager, virtual_size: tuple[int, int]) -> None:
        self._manager: pygame_gui.UIManager = manager
        self._virtual_size: tuple[int, int] = virtual_size
        self._ui_actions: dict[pygame_gui.core.UIElement, InputEvent] = {}

    def register_ui_action(self, element: pygame_gui.core.UIElement, action: InputEvent) -> None:
        self._ui_actions[element] = action

    def next_event(self) -> InputEvent | None:
        result: InputEvent | None = None

        for event in pygame.event.get():
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                event = self._to_virtual_coords(event)

            self._manager.process_events(event)

            if event.type == pygame.QUIT:
                result = InputEvent.QUIT
            elif event.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                mapped = keycode_to_event(event.key)
                if mapped is not None:
                    result = mapped
            elif event.type == pygame_gui.UI_BUTTON_PRESSED:
                mapped = self._ui_actions.get(event.ui_element)
                if mapped is not None:
                    result = mapped

        return result

    def _to_virtual_coords(self, event: pygame.event.Event) -> pygame.event.Event:
        window = pygame.display.get_surface()
        window_w, window_h = window.get_size()
        virtual_w, virtual_h = self._virtual_size
        scale_x = virtual_w / window_w
        scale_y = virtual_h / window_h

        pos = (int(event.pos[0] * scale_x), int(event.pos[1] * scale_y))
        if event.type == pygame.MOUSEMOTION:
            rel = (int(event.rel[0] * scale_x), int(event.rel[1] * scale_y))
            return pygame.event.Event(event.type, pos=pos, rel=rel, buttons=event.buttons)
        return pygame.event.Event(event.type, pos=pos, button=event.button)

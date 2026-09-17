from pathlib import Path

import pygame
import pygame_gui

from mastermind_shell.pygame_backend.renderer import PygameRenderer
from mastermind_shell.pygame_backend.input_source import PygameInputSource
from mastermind_shell.engine.input_event import InputEvent
from mastermind_shell.engine.screen_queue import ScreenQueue
from mastermind_shell.engine.screen_stack import ScreenStack
from mastermind_shell.screens.menu import MenuScreen

VIRTUAL_SIZE = (1920, 1280)


def main(virtual_surface: pygame.Surface, manager: pygame_gui.UIManager):
    renderer: PygameRenderer = PygameRenderer(virtual_surface, manager)
    input_source: PygameInputSource = PygameInputSource(manager, VIRTUAL_SIZE)
    input_source.register_ui_action(renderer.play_button, InputEvent.PLAY)
    input_source.register_ui_action(renderer.exit_button, InputEvent.EXIT)

    queue: ScreenQueue = ScreenQueue()
    menu: MenuScreen = MenuScreen(queue, renderer)
    stack: ScreenStack = ScreenStack(input_source, queue, menu)

    clock = pygame.time.Clock()
    running = True
    while running:
        dt = clock.tick(60) / 1000
        manager.update(dt)
        running = stack.step()

        window = pygame.display.get_surface()
        scaled = pygame.transform.smoothscale(virtual_surface, window.get_size())
        _ = window.blit(scaled, (0, 0))
        pygame.display.flip()


def run():
    _ = pygame.init()
    pygame.font.init()

    virtual_surface: pygame.Surface = pygame.Surface(VIRTUAL_SIZE)
    _ = pygame.display.set_mode(VIRTUAL_SIZE, pygame.RESIZABLE)

    theme_path = Path(__file__).resolve().parent / "pygame_backend" / "theme.json"
    manager: pygame_gui.UIManager = pygame_gui.UIManager(VIRTUAL_SIZE, theme_path=str(theme_path))

    main(virtual_surface, manager)

    pygame.quit()

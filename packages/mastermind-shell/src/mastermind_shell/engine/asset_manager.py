from dataclasses import dataclass
from pathlib import Path

import pygame


_ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


@dataclass
class PegAsset:
    white: pygame.Surface
    purple: pygame.Surface
    red: pygame.Surface
    green: pygame.Surface
    blue: pygame.Surface
    yellow: pygame.Surface


class AssetManager:
    def __init__(self) -> None:
        self._pegs: PegAsset 
        self._background: pygame.Surface

        self._init_pegs(_ASSETS_DIR / "peg")
        self._init_background()


    @property
    def pegs(self) -> PegAsset:
        return self._pegs

    @property
    def background(self) -> pygame.Surface:
        return self._background

    def _init_pegs(self, peg_path: Path) -> None:
        white = pygame.image.load(peg_path / "white.png").convert_alpha()
        purple = pygame.image.load(peg_path / "purple.png").convert_alpha()
        red = pygame.image.load(peg_path / "red.png").convert_alpha()
        green = pygame.image.load(peg_path / "green.png").convert_alpha()
        blue = pygame.image.load(peg_path / "blue.png").convert_alpha()
        yellow = pygame.image.load(peg_path / "yellow.png").convert_alpha()

        white = pygame.transform.scale(white, (128, 128))
        purple = pygame.transform.scale(purple, (128, 128))
        red = pygame.transform.scale(red, (128, 128))
        green = pygame.transform.scale(green, (128, 128))
        blue = pygame.transform.scale(blue, (128, 128))
        yellow = pygame.transform.scale(yellow, (128, 128))

        self._pegs = PegAsset(white, purple, red, green, blue, yellow)

    def _init_background(self) -> None:
        background = pygame.image.load(_ASSETS_DIR / "background.png").convert()

        self._background = background


import pygame
import pygame_gui

from mastermind_kernel.colors import PegColor
from mastermind_shell.engine.asset_manager import AssetManager
from mastermind_overlay.jokers.jokers import Joker
from mastermind_overlay.relics.relic import Relic
from mastermind_overlay.run.gamestate import GameState

from mastermind_overlay.run.run_state import RunState


class LayoutHelper:
    def __init__(self, width: int, height: int) -> None:
        self._width: int = width
        self._height: int = height

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def margin(self, ratio: float) -> int:
        return int(self._width * ratio)

    def center_x(self, obj_width: int) -> int:
        return (self._width - obj_width) // 2

    def center_y(self, obj_height: int) -> int:
        return (self._height - obj_height) // 2

    def rect(self, x_ratio: float, y_ratio: float, w_ratio: float, h_ratio: float) -> pygame.Rect:
        x = int(self._width * x_ratio)
        y = int(self.height * y_ratio)
        w = int(self._width * w_ratio)
        h = int(self._height * h_ratio)
        return pygame.rect.Rect(x, y, w, h)

    def rect_centered(self, w_ratio: float, h_ratio: float) -> pygame.Rect:
        w = int(self._width * w_ratio)
        h = int(self._height * h_ratio)
        x = self.center_x(w)
        y = self.center_y(h)
        return pygame.rect.Rect(x, y, w, h)


class GameRenderer:
    def __init__(self, surface: pygame.Surface, asset_manager: AssetManager) -> None:
        self._surface: pygame.Surface = surface
        self._font: pygame.font.Font = pygame.font.SysFont("Corbel", 64)
        self._font_small: pygame.font.Font = pygame.font.SysFont("Corbel", 32)
        self._asset_manager: AssetManager = asset_manager

        self._layout: LayoutHelper = LayoutHelper(*surface.get_size())
        margin = self._layout.margin(1/20)
        left_width = self._layout.width // 3.5
        right_width = self._layout.width - left_width - margin
        self._left_surface: pygame.Surface = surface.subsurface((margin, 0, left_width, self._layout.height))
        self._right_surface: pygame.Surface = surface.subsurface((left_width + margin, 0, right_width, self._layout.height))
        self._left_layout: LayoutHelper = LayoutHelper(*self._left_surface.get_size())
        self._right_layout: LayoutHelper = LayoutHelper(*self._right_surface.get_size())


    @property
    def dimensions(self) -> tuple[int, int]:
        return self._surface.get_size()

    @property
    def dimensions_left(self) -> tuple[int, int]:
        return self._left_surface.get_size()

    @property
    def dimensions_right(self) -> tuple[int, int]:
        return self._right_surface.get_size()


    def render(self, game_state: GameState, run_state: RunState) -> None:
        _ = self._surface.blit(self._asset_manager.background, (0, 0))
        _ = self._left_surface.fill((47, 58, 60))

        self._render_current_guess(game_state)
        self._render_passed_guesses(game_state)
        self._render_tier(run_state)
        self._render_score_to_reach(game_state)
        self._render_round_score(game_state)
        self._render_turns_left(game_state)
        self._render_points_and_mult(game_state)

    def _render_current_guess(self, game_state: GameState) -> None:
        sprite_size = 128
        offset = 32
        sprite_and_offset = sprite_size + offset
        all_pegs_width = sprite_and_offset * 4
        x = self._right_layout.center_x(all_pegs_width) + self._left_layout.width
        y = self._right_layout.height - sprite_and_offset
        for peg_color in game_state.current_code:
            _ = self._surface.blit(self._peg_color_to_asset(peg_color), (x, y))
            x += sprite_and_offset

    def _render_passed_guesses(self, game_state: GameState) -> None:
        sprite_size = 64
        offset = 16
        sprite_and_offset = sprite_size + offset
        all_pegs_width = sprite_and_offset * 4
        x = self._right_layout.center_x(all_pegs_width) + self._left_layout.width
        y = sprite_and_offset
        for guess in game_state.guessed_codes:
            for peg_color in guess:
                _ = self._surface.blit(self._peg_color_to_asset(peg_color), (x, y))
                x += sprite_and_offset


    def _render_tier(self, run_state: RunState) -> None:
        rect = self._left_layout.rect(0.1, 0.05, 0.8, 0.1)
        _ = pygame.draw.rect(self._left_surface, (84, 69, 26), rect, border_radius=20)
        _ = pygame.draw.rect(self._left_surface, (84, 69, 26), rect, width=5, border_radius=20)
        tier_text = self._font.render(run_state.tier.label, True, (255, 255, 255))
        tier_rect = tier_text.get_rect(center=rect.center)
        _ = self._left_surface.blit(tier_text, tier_rect)


    def _render_score_to_reach(self, game_state: GameState) -> None:
        outer_rect = self._left_layout.rect(0.02, 0.16, 0.96, 0.2)
        _ = pygame.draw.rect(self._left_surface, (84, 69, 26), outer_rect, border_radius=20)

        panel_rect = self._left_layout.rect(0.5, 0.18, 0.35, 0.14)
        _ = pygame.draw.rect(self._left_surface, (47, 58, 60), panel_rect, border_radius=20)

        label = self._font_small.render("Score at least", True, (255, 255, 255))
        label_rect = label.get_rect(center=(panel_rect.centerx, panel_rect.y + panel_rect.height * 0.15))
        _ = self._left_surface.blit(label, label_rect)

        score = self._font_small.render(str(game_state.target_score), True, (255, 255, 255))
        score_rect = score.get_rect(center=(panel_rect.centerx, panel_rect.y + panel_rect.height * 0.4))
        _ = self._left_surface.blit(score, score_rect)

        label = self._font_small.render("Reward: $$$$", True, (255, 255, 255))
        label_rect = label.get_rect(center=(panel_rect.centerx, panel_rect.y + panel_rect.height * 0.7))
        _ = self._left_surface.blit(label, label_rect)



    def _render_round_score(self, game_state: GameState) -> None:
        outer_rect = self._left_layout.rect(0.02, 0.37, 0.96, 0.07)
        _ = pygame.draw.rect(self._left_surface, (26, 37, 39), outer_rect, border_radius=20)

        label_top = self._font_small.render("Round", True, (255, 255, 255))
        label_down = self._font_small.render("Score", True, (255, 255, 255))
        _ = self._left_surface.blit(label_top, label_top.get_rect(topleft=(outer_rect.x + 10, outer_rect.y + 5)))
        _ = self._left_surface.blit(label_down, label_down.get_rect(topleft=(outer_rect.x + 10, outer_rect.y + 20)))

        panel_rect = self._left_layout.rect(0.4, 0.375, 0.5, 0.06)
        _ = pygame.draw.rect(self._left_surface, (47, 58, 60), panel_rect, border_radius=20)

        score_label = self._font.render(str(game_state.score), True, (255, 255, 255))
        score_rect = score_label.get_rect(center=panel_rect.center)
        _ = self._left_surface.blit(score_label, score_rect)


    def _render_points_and_mult(self, game_state: GameState) -> None:
        margin_horizontal = self.dimensions_left[0] // 50

        width = self.dimensions_left[0] - margin_horizontal * 2
        height = self.dimensions_left[1] // 5
        x = margin_horizontal
        y = int(self.dimensions_left[1] * 0.37)
        outer_rect = pygame.rect.Rect(x, y, width, height)
        _ = pygame.draw.rect(self._left_surface, (26, 37, 39), outer_rect, border_radius=20)



    def _render_turns_left(self, game_state: GameState) -> None:
        outer_rect = self._left_layout.rect(0.425, 0.58, 0.25, 0.1)
        _ = pygame.draw.rect(self._left_surface, (26, 37, 39), outer_rect, border_radius=20)

        label = self._font_small.render("Turns", True, (255, 255, 255))
        _ = self._left_surface.blit(label, label.get_rect(center=(outer_rect.centerx, outer_rect.y + outer_rect.height // 8)))

        panel_rect = self._left_layout.rect(0.45, 0.61, 0.2, 0.06)
        _ = pygame.draw.rect(self._left_surface, (47, 58, 60), panel_rect, border_radius=20)

        turns_label = self._font.render(str(game_state.turns_left), True, (255, 255, 255))
        turns_rect = turns_label.get_rect(center=panel_rect.center)
        _ = self._left_surface.blit(turns_label, turns_rect)


    def _peg_color_to_asset(self, peg_color: PegColor) -> pygame.Surface:
        peg_to_color_dict = {
            PegColor.WHITE: self._asset_manager.pegs.white,
            PegColor.PURPLE: self._asset_manager.pegs.purple,
            PegColor.RED: self._asset_manager.pegs.red,
            PegColor.GREEN: self._asset_manager.pegs.green,
            PegColor.BLUE: self._asset_manager.pegs.blue,
            PegColor.ORANGE: self._asset_manager.pegs.yellow,
        }
        return peg_to_color_dict[peg_color]




class PygameRenderer:
    def __init__(self, surface: pygame.Surface, manager: pygame_gui.UIManager) -> None:
        self._surface: pygame.Surface = surface
        self._manager: pygame_gui.UIManager = manager
        self._asset_manager: AssetManager = AssetManager()

        self._game_renderer: GameRenderer = GameRenderer(surface, self._asset_manager)

        s_width, s_height = self.dimensions()
        self._play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, s_height // 3), (320, 100)),
            text="Play",
            manager=self._manager,
            anchors={"centerx": "centerx"}
        )
        self._exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, (s_height // 3) * 2), (320, 100)),
            text="Exit",
            manager=self._manager,
            anchors={"centerx": "centerx"}
        )


    @property
    def play_button(self) -> pygame_gui.elements.UIButton:
        return self._play_button

    @property
    def exit_button(self) -> pygame_gui.elements.UIButton:
        return self._exit_button

    def dimensions(self) -> tuple[int, int]:
        return self._surface.get_size()

    def clear(self) -> None: ...
    def refresh(self) -> None: ...
    def draw_text(self, y: int, x: int, text: str, highlighted: bool = False) -> None: ...

    def render_menu(self, current: int) -> None:
        _ = self._surface.fill((52, 78, 91))

        if current == 1:
            self._play_button.select()
            self._exit_button.unselect()
        else:
            self._play_button.unselect()
            self._exit_button.select()

        self._manager.draw_ui(self._surface)


    def render_gameplay(self, state: GameState, stage: int, tier_label: str, relics: list[Relic], jokers: list[Joker], run_state: RunState) -> None:
        self._game_renderer.render(state, run_state)


    def _draw_guess_code(self, game_state: GameState) -> None:
        pass


    def render_win(self, correct_guess_str: str) -> None: ...
    def render_loose(self, correct_guess_str: str) -> None: ...
    def render_run_over(self, selected: int) -> None: ...
    def render_shop(self, currency: int, offer: list[Relic], extra_guess_price: int, selected: int, owned_relics: list[Relic], max_relics: int, reroll_price: int, joker_price: int) -> None: ...
    def render_boss_announcement(self, title: str, description: str) -> None: ...
    def render_joker_booster(self, jokers: list[Joker], selected: int) -> None: ...
    def error(self, message: str) -> None: ...



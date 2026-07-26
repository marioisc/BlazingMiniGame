"""
==========================================================
Project : Operation Phoenix
Version : 0.1.0

Escena principal.

En esta versión únicamente muestra un menú muy simple.

Controles
----------
ENTER : Iniciar juego
ESC   : Salir
==========================================================
"""

from __future__ import annotations

import pygame

from config import (
    BACKGROUND_COLOR,
    DEFAULT_FONT,
    DEFAULT_FONT_SIZE,
    HUD_COLOR,
)

from scenes.scene import Scene
from scenes.gameplay import Gameplay


class Menu(Scene):
    """
    Menú principal.
    """

    def __init__(self, game) -> None:

        super().__init__(game)

        self.title_font = pygame.font.SysFont(
            DEFAULT_FONT,
            56,
            bold=True
        )

        self.menu_font = pygame.font.SysFont(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE
        )

    # =====================================================
    # EVENTS
    # =====================================================

    def handle_events(
        self,
        events: list[pygame.event.Event]
    ) -> None:

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    self.game.change_scene(
                        Gameplay(self.game)
                    )

                elif event.key == pygame.K_ESCAPE:

                    self.game.running = False

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        delta_time: float
    ) -> None:
        """
        El menú no necesita actualizar lógica
        en esta versión.
        """
        pass

    # =====================================================
    # DRAW
    # =====================================================

    def draw(
        self,
        screen: pygame.Surface
    ) -> None:

        screen.fill(BACKGROUND_COLOR)

        title = self.title_font.render(
            "OPERATION PHOENIX",
            True,
            HUD_COLOR
        )

        press_start = self.menu_font.render(
            "Presiona ENTER para comenzar",
            True,
            HUD_COLOR
        )

        exit_text = self.menu_font.render(
            "ESC para salir",
            True,
            HUD_COLOR
        )

        screen.blit(
            title,
            (
                (screen.get_width() - title.get_width()) // 2,
                180,
            ),
        )

        screen.blit(
            press_start,
            (
                (screen.get_width() - press_start.get_width()) // 2,
                340,
            ),
        )

        screen.blit(
            exit_text,
            (
                (screen.get_width() - exit_text.get_width()) // 2,
                390,
            ),
        )
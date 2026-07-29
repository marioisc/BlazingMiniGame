from __future__ import annotations

import pygame

from config import (
    BACKGROUND_COLOR,
    DEFAULT_FONT,
    DEFAULT_FONT_SIZE,
    HUD_COLOR,
)

from scenes.scene import Scene


class GameOver(Scene):

    def __init__(
        self,
        game,
    ) -> None:

        super().__init__(game)

        self.title_font = pygame.font.SysFont(
            DEFAULT_FONT,
            64,
        )

        self.text_font = pygame.font.SysFont(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        )

    def handle_events(
        self,
        events: list[pygame.event.Event],
    ) -> None:

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.game.running = False

    def update(
        self,
        delta_time: float,
    ) -> None:

        pass

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:

        screen.fill(BACKGROUND_COLOR)

        title = self.title_font.render(
            "GAME OVER",
            True,
            HUD_COLOR,
        )

        message = self.text_font.render(
            "Press ESC to exit",
            True,
            HUD_COLOR,
        )

        screen.blit(
            title,
            (
                (screen.get_width() - title.get_width()) // 2,
                220,
            ),
        )

        screen.blit(
            message,
            (
                (screen.get_width() - message.get_width()) // 2,
                340,
            ),
        )
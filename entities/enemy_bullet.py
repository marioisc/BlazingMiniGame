from __future__ import annotations

import pygame

from config import (
    SCREEN_WIDTH,
)

from entities.bullet_base import BulletBase


class EnemyBullet(BulletBase):

    WIDTH = 14
    HEIGHT = 4

    SPEED = -450

    COLOR = (255, 80, 80)

    def __init__(
        self,
        x: float,
        y: float,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            speed_x=self.SPEED,
            speed_y=0.0,
        )

    def update(
        self,
        delta_time: float,
    ) -> None:

        super().update(delta_time)

        if self.rect.right < 0:

            self.destroy()

    def draw(
        self,
        surface: pygame.Surface,
    ) -> None:

        pygame.draw.rect(
            surface,
            self.COLOR,
            self.rect,
        )
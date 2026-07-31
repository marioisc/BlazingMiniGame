"""
Bullet entity.

This module defines the base projectile used by the gameplay.
The implementation is intentionally simple and will be expanded
in future functional units with collisions, animations, damage,
particle effects and different projectile types.
"""

from __future__ import annotations

from pygame import Color
import pygame

from config import SCREEN_WIDTH
from entities.bullet_base import BulletBase


class Bullet(BulletBase):
    """
    Basic projectile entity.
    """

    WIDTH: int = 8
    HEIGHT: int = 8
    COLOR: Color = Color("gold")
    SPEED: float = 600.0

    def __init__(
        self,
        x: float,
        y: float,
        direction_x: float = 1.0,
        direction_y: float = 0.0,
    ) -> None:
        """
        Create a new bullet.

        Parameters
        ----------
        x:
            Initial X position.
        y:
            Initial Y position.
        direction_x:
            Horizontal direction.
        direction_y:
            Vertical direction.
        """
        super().__init__(
            x=x,
            y=y,
            speed_x=self.SPEED,
            speed_y=0.0,
        )

        self.direction_x: float = direction_x
        self.direction_y: float = direction_y

        self.active: bool = True

    
    def update(self, delta_time: float) -> None:
        """
        Update bullet position.

        Parameters
        ----------
        delta_time:
            Time elapsed since previous frame.
        """
        super().update(delta_time)

        self.sync_rect()
        if self.rect.left > SCREEN_WIDTH:
            self.destroy()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the bullet.

        Parameters
        ----------
        surface:
            Destination surface.
        """
        pygame.draw.rect(
            surface,
            self.COLOR,
            self.rect,
        )

    def deactivate(self) -> None:
        """
        Mark the bullet as inactive.

        Future versions will remove inactive bullets from
        the entity manager.
        """
        self.destroy()

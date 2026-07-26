"""
Enemy entity.

This module defines the first enemy implementation used by the
gameplay scene. The current version only provides downward movement
and basic rendering. Future functional units will extend this class
with health, AI, animations, collisions and attack behaviors.
"""

from __future__ import annotations

import pygame

from entities.entity import Entity


class Enemy(Entity):
    """
    Basic enemy entity.
    """

    WIDTH: int = 32
    HEIGHT: int = 32

    COLOR: pygame.Color = pygame.Color("crimson")

    SPEED: float = 120.0

    def __init__(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Initialize an enemy.

        Parameters
        ----------
        x:
            Initial horizontal position.
        y:
            Initial vertical position.
        """
        super().__init__(
            x=x,
            y=y,
            width=self.WIDTH,
            height=self.HEIGHT,
        )

        self.active: bool = True

    def update(
        self,
        delta_time: float,
    ) -> None:
        """
        Update the enemy.

        Parameters
        ----------
        delta_time:
            Time elapsed since previous frame.
        """
        self.x -= self.SPEED * delta_time
        
        self.sync_rect()
        if self.rect.right < 0:
                    self.destroy()

    def draw(
        self,
        surface: pygame.Surface,
    ) -> None:
        """
        Draw the enemy.

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
        Mark the enemy as inactive.
        """
        self.destroy()


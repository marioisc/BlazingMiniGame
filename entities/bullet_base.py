from __future__ import annotations

from entities.entity import Entity


class BulletBase(Entity):
    """
    Base class for every projectile in the game.
    """

    WIDTH = 16
    HEIGHT = 4

    def __init__(
        self,
        x: float,
        y: float,
        speed_x: float,
        speed_y: float,
    ) -> None:

        super().__init__(
            x=x,
            y=y,
            width=self.WIDTH,
            height=self.HEIGHT,
        )

        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(
        self,
        delta_time: float,
    ) -> None:

        self.x += self.speed_x * delta_time
        self.y += self.speed_y * delta_time

        self.sync_rect()
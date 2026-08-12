"""
Explorer Drone enemy for Operation Phoenix.

Sprint 4-D2
-----------
- Fast low-resistance enemy.
- Spawned as groups of five.
- All drones in a group move together.
- All drones fire their simple shot simultaneously.
- Group reward/power-up logic is intentionally not implemented yet.
"""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from entities.enemy import Enemy
from entities.enemy_bullet import EnemyBullet


@dataclass
class ExplorerDroneGroup:
    """
    Shared state for one group of Explorer Drones.
    """

    fire_cooldown: float = 2.0
    fire_timer: float = 2.0

    def update(
        self,
        delta_time: float,
    ) -> bool:
        """
        Advance the group fire timer.

        Returns True when the whole group must fire.
        """

        self.fire_timer -= delta_time

        if self.fire_timer > 0:
            return False

        self.fire_timer = self.fire_cooldown

        return True


class ExplorerDrone(Enemy):
    """
    Fast Explorer Drone.

    Five instances share one ExplorerDroneGroup so their
    simple shots are synchronized.
    """

    WIDTH: int = 40
    HEIGHT: int = 40

    COLOR: pygame.Color = pygame.Color("limegreen")

    SPEED: float = 220.0

    MAX_HEALTH: int = 30
    CONTACT_DAMAGE: int = 1
    SCORE_VALUE: int = 100

    FIRE_COOLDOWN: float = 2.0

    def __init__(
        self,
        x: float,
        y: float,
        group: ExplorerDroneGroup,
    ) -> None:
        """
        Initialize an Explorer Drone and assign its group.
        """

        super().__init__(
            x=x,
            y=y,
        )

        self._group = group

    def update(
        self,
        delta_time: float,
    ) -> None:
        """
        Update movement and synchronized group firing.

        Only the first active drone of a group should advance
        the shared group timer. The group controller is normally
        updated by the owner of the group.
        """

        self.x -= self.SPEED * delta_time

        self.sync_rect()

        if self.rect.right < 0:
            self.destroy()

        for bullet in self._bullets:
            bullet.update(delta_time)

        self.cleanup_bullets()

    def fire(
        self,
    ) -> None:
        """
        Fire one simple projectile.
        """

        if not self.is_active:
            return

        bullet = EnemyBullet(
            self.rect.left,
            self.rect.centery,
        )

        self._bullets.append(bullet)

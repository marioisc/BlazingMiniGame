"""
Sniper Enemy for Operation Phoenix.

Sprint 4-D6
-----------
Long-range enemy with a slow, powerful single shot.
"""

from __future__ import annotations

import pygame

from entities.enemy import Enemy
from entities.enemy_bullet import EnemyBullet


class SniperBullet(EnemyBullet):
    """Slow projectile fired by the Sniper Enemy."""

    SPEED: float = -260.0

    def __init__(self, x: float, y: float) -> None:
        """Create a Sniper projectile."""
        super().__init__(x=x, y=y)

    def update(self, delta_time: float) -> None:
        """Update the projectile."""
        self.x += self.SPEED * delta_time
        self.sync_rect()

        if self.rect.right < 0:
            self.destroy()


class SniperEnemy(Enemy):
    """
    Long-range enemy.

    It advances to a firing position, stops there and periodically
    fires one slow, powerful projectile.
    """

    WIDTH: int = 72
    HEIGHT: int = 40
    COLOR: pygame.Color = pygame.Color("firebrick")

    SPEED: float = 45.0

    MAX_HEALTH: int = 15
    CONTACT_DAMAGE: int = 1
    SCORE_VALUE: int = 400

    FIRE_COOLDOWN: float = 3.5
    STOP_X: int = 650

    def __init__(self, x: float, y: float) -> None:
        """Initialize the Sniper Enemy."""
        super().__init__(x=x, y=y)

        self._health = self.MAX_HEALTH
        self._stopped = False
        self._fire_timer = self.FIRE_COOLDOWN
        self._bullets = []

    @property
    def health(self) -> int:
        """Return current health."""
        return self._health

    def take_damage(self, damage: int) -> bool:
        """
        Apply damage.

        Returns True when the enemy is destroyed.
        """
        if not self.is_active:
            return False

        self._health = max(
            0,
            self._health - max(1, damage),
        )

        if self._health <= 0:
            self.destroy()
            return True

        return False

    def update(self, delta_time: float) -> None:
        """Update movement, firing and projectiles."""

        if not self._stopped:
            self.x -= self.SPEED * delta_time
            self.sync_rect()

            if self.rect.left <= self.STOP_X:
                self._stopped = True
                self._fire_timer = self.FIRE_COOLDOWN

        else:
            self._fire_timer -= delta_time

            if self._fire_timer <= 0:
                self._shoot()
                self._fire_timer = self.FIRE_COOLDOWN

        if self.rect.right < 0:
            self.destroy()

        for bullet in self._bullets:
            bullet.update(delta_time)

        self._bullets = [
            bullet
            for bullet in self._bullets
            if bullet.is_active
        ]

    def _shoot(self) -> None:
        """Fire one slow and powerful projectile."""
        self._bullets.append(
            SniperBullet(
                self.rect.left,
                self.rect.centery,
            ),
        )

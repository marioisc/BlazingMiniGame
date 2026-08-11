"""
Enemy base entity for Operation Phoenix.
"""

from __future__ import annotations

import pygame

from entities.entity import Entity
from entities.enemy_bullet import EnemyBullet


class Enemy(Entity):
    """
    Base class for all enemy entities.
    """

    WIDTH: int = 32
    HEIGHT: int = 32

    COLOR: pygame.Color = pygame.Color("crimson")

    SPEED: float = 120.0
    FIRE_COOLDOWN: float = 2.0

    MAX_HEALTH: int = 1
    CONTACT_DAMAGE: int = 1
    SCORE_VALUE: int = 100

    def __init__(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Initialize the enemy entity.
        """

        super().__init__(
            x=x,
            y=y,
            width=self.WIDTH,
            height=self.HEIGHT,
        )

        self.active = True
        self._health = self.MAX_HEALTH
        self._fire_timer = self.FIRE_COOLDOWN
        self._bullets: list[EnemyBullet] = []

    @property
    def health(self) -> int:
        """
        Return the current health.
        """

        return self._health

    @property
    def max_health(self) -> int:
        """
        Return the maximum health.
        """

        return self.MAX_HEALTH

    @property
    def contact_damage(self) -> int:
        """
        Return the contact damage.
        """

        return self.CONTACT_DAMAGE

    @property
    def score_value(self) -> int:
        """
        Return the score awarded when destroyed.
        """

        return self.SCORE_VALUE

    @property
    def bullets(self) -> list[EnemyBullet]:
        """
        Return the enemy bullets.
        """

        return self._bullets

    def take_damage(self, damage: int = 1) -> bool:
        """
        Apply damage and return whether the enemy was destroyed.
        """

        if not self.is_active:
            return False

        self._health -= damage

        if self._health <= 0:
            self._health = 0
            self.destroy()
            return True

        return False

    def update(self, delta_time: float) -> None:
        """
        Update the default enemy behavior.
        """

        self.x -= self.SPEED * delta_time
        self.sync_rect()

        if self.rect.right < 0:
            self.destroy()

        self._fire_timer -= delta_time

        if self._fire_timer <= 0:
            self._shoot()
            self._fire_timer = self.FIRE_COOLDOWN

        for bullet in self._bullets:
            bullet.update(delta_time)

        self.cleanup_bullets()

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the enemy and its bullets.
        """

        pygame.draw.rect(
            surface,
            self.COLOR,
            self.rect,
        )

        for bullet in self._bullets:
            bullet.draw(surface)

    def deactivate(self) -> None:
        """
        Deactivate the enemy.
        """

        self.destroy()

    def _shoot(self) -> None:
        """
        Create the default enemy projectile.
        """

        bullet = EnemyBullet(
            self.rect.left,
            self.rect.centery,
        )

        self._bullets.append(bullet)

    def cleanup_bullets(self) -> None:
        """
        Remove inactive enemy bullets.
        """


        self._bullets = [
            bullet
            for bullet in self._bullets
            if bullet.is_active
        ]
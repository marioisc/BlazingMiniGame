"""
Interceptor Angel enemy for Operation Phoenix.

Sprint 4-D7
-----------
Extremely fast interceptor with dive attacks and rapid bursts.
"""

from __future__ import annotations

import pygame

from entities.bullet_base import BulletBase
from entities.enemy import Enemy


class InterceptorBullet(BulletBase):
    """Fast projectile used by the Interceptor Angel."""

    WIDTH: int = 10
    HEIGHT: int = 5
    SPEED_X: float = -520.0
    COLOR: pygame.Color = pygame.Color("cyan")

    def __init__(self, x: float, y: float, speed_y: float) -> None:
        """Create an interceptor projectile."""
        super().__init__(
            x=x,
            y=y,
            speed_x=self.SPEED_X,
            speed_y=speed_y,
        )

    def update(self, delta_time: float) -> None:
        """Update the projectile."""
        super().update(delta_time)

        screen_height = pygame.display.get_surface().get_height()

        if (
            self.rect.right < 0
            or self.rect.bottom < 0
            or self.rect.top > screen_height
        ):
            self.destroy()

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the interceptor projectile."""
        pygame.draw.rect(
            surface,
            self.COLOR,
            self.rect,
        )


class InterceptorAngel(Enemy):
    """
    Extremely fast interceptor.

    It dives downward from above, fires a rapid three-projectile
    burst, recovers upward and repeats the cycle while moving
    across the screen.
    """

    WIDTH: int = 56
    HEIGHT: int = 56
    COLOR: pygame.Color = pygame.Color("royalblue")

    SPEED: float = 320.0

    MAX_HEALTH: int = 25
    CONTACT_DAMAGE: int = 2
    SCORE_VALUE: int = 300

    DIVE_SPEED: float = 430.0
    DIVE_DURATION: float = 0.85
    RECOVERY_DURATION: float = 0.55

    FIRE_COOLDOWN: float = 1.15
    BURST_SPREAD: float = 85.0

    def __init__(self, x: float, y: float) -> None:
        """Initialize the Interceptor Angel."""
        super().__init__(x=x, y=y)

        self._health = self.MAX_HEALTH
        self._dive_timer = 0.0
        self._recovery_timer = 0.0
        self._fire_timer = self.FIRE_COOLDOWN
        self._diving = True
        self._bullets = []

    @property
    def health(self) -> int:
        """Return current health."""
        return self._health

    def take_damage(self, damage: int) -> bool:
        """Apply damage and return True when destroyed."""
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
        """Update movement, dive cycle and rapid fire."""
        self.x -= self.SPEED * delta_time

        if self._diving:
            self.y += self.DIVE_SPEED * delta_time
            self._dive_timer += delta_time

            if self._dive_timer >= self.DIVE_DURATION:
                self._diving = False
                self._recovery_timer = 0.0

        else:
            self.y -= (
                self.DIVE_SPEED
                * 0.85
                * delta_time
            )
            self._recovery_timer += delta_time

            if self._recovery_timer >= self.RECOVERY_DURATION:
                self._diving = True
                self._dive_timer = 0.0

        self.sync_rect()

        screen_height = pygame.display.get_surface().get_height()

        if (
            self.rect.right < 0
            or self.rect.top > screen_height
        ):
            self.destroy()
            return

        self._fire_timer -= delta_time

        if self._fire_timer <= 0:
            self._shoot()
            self._fire_timer = self.FIRE_COOLDOWN

        for bullet in self._bullets:
            bullet.update(delta_time)

        self._bullets = [
            bullet
            for bullet in self._bullets
            if bullet.is_active
        ]

    def _shoot(self) -> None:
        """Fire a rapid three-projectile burst."""
        center_y = self.rect.centery

        for speed_y in (
            -self.BURST_SPREAD,
            0.0,
            self.BURST_SPREAD,
        ):
            self._bullets.append(
                InterceptorBullet(
                    self.rect.left,
                    center_y,
                    speed_y,
                ),
            )

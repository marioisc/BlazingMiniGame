"""
Heavy Ship enemy for Operation Phoenix.

Sprint 5-C3.5
-----------
- Slow and highly resistant enemy.
- Appears individually in Wave 3.
- Stops before firing.
- Fires a five-projectile spread.
- Advances toward the player after the burst.
- Repeats the behavior cycle.
"""

from __future__ import annotations

import pygame

from entities.bullet_base import BulletBase
from entities.enemy import Enemy


class HeavyShipBullet(BulletBase):
    """
    Projectile used exclusively by the Heavy Ship.

    The projectile keeps the horizontal shooter direction while allowing
    a vertical component so five projectiles can form a light spread.
    """

    WIDTH: int = 14
    HEIGHT: int = 6

    SPEED_X: float = -360.0
    COLOR: pygame.Color = pygame.Color("red")

    def __init__(
        self,
        x: float,
        y: float,
        speed_y: float,
    ) -> None:
        """
        Create one Heavy Ship projectile.
        """

        super().__init__(
            x=x,
            y=y,
            speed_x=self.SPEED_X,
            speed_y=speed_y,
        )

    def update(
        self,
        delta_time: float,
    ) -> None:
        """
        Update projectile movement and remove it when it leaves the screen.
        """

        super().update(
            delta_time,
        )

        if (
            self.rect.right < 0
            or self.rect.top > pygame.display.get_surface().get_height()
            or self.rect.bottom < 0
        ):
            self.destroy()

    def draw(
        self,
        surface: pygame.Surface,
    ) -> None:
        """
        Draw the Heavy Ship projectile.
        """

        pygame.draw.rect(
            surface,
            self.COLOR,
            self.rect,
        )


class HeavyShip(Enemy):
    """
    Slow and highly resistant enemy.

    Behavior cycle:
        1. Enters the screen.
        2. Stops at its firing position.
        3. Fires five projectiles in a spread.
        4. Advances toward the player.
        5. Repeats the cycle.
    """

    WIDTH: int = 72
    HEIGHT: int = 72

    COLOR: pygame.Color = pygame.Color("darkred")

    SPEED: float = 80.0

    MAX_HEALTH: int = 30
    CONTACT_DAMAGE: int = 2
    SCORE_VALUE: int = 500

    FIRE_COOLDOWN: float = 3.0

    STOP_X: int = 620
    ATTACK_DURATION: float = 10.0

    SHOT_SPEED_Y: float = 90.0

    def __init__(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Initialize the Heavy Ship.
        """

        super().__init__(
            x=x,
            y=y,
        )

        self._health = self.MAX_HEALTH

        self._stopped = False
        self._attack_timer = 0.0
        self._advancing = False

        self._attack_position_y = self.y
        self._moving_to_attack_position = False

        # The first shot occurs after the ship reaches its firing position.
        self._fire_timer = self.FIRE_COOLDOWN

        # Replace the base Enemy projectile list with a list dedicated
        # to Heavy Ship projectiles.
        self._bullets = []

    @property
    def health(
        self,
    ) -> int:
        """
        Return the current Heavy Ship health.
        """

        return self._health

    def take_damage(
        self,
        damage: int,
    ) -> bool:
        """
        Apply damage to the Heavy Ship.

        Returns:
            True when the Heavy Ship is destroyed.
            False while it remains active.
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

    def set_attack_position(
        self,
        target_y: float,
    ) -> None:
        """
        Set the vertical attack position for the Heavy Ship.
        """

        self._attack_position_y = float(target_y)
        self._moving_to_attack_position = True

    def update(
        self,
        delta_time: float,
    ) -> None:
        """
        Update movement, firing cycle and projectiles.
        """

        if self._moving_to_attack_position:

            vertical_speed = self.SPEED

            if self.y < self._attack_position_y:

                self.y = min(
                    self.y + vertical_speed * delta_time,
                    self._attack_position_y,
                )

            else:

                self.y = max(
                    self.y - vertical_speed * delta_time,
                    self._attack_position_y,
                )

            if abs(
                self.y - self._attack_position_y
            ) < 0.5:

                self.y = self._attack_position_y
                self._moving_to_attack_position = False
                self._stopped = True
                self._attack_timer = 0.0
                self._fire_timer = self.FIRE_COOLDOWN

            self.sync_rect()

        elif not self._stopped:

            self.x -= self.SPEED * delta_time

            self.sync_rect()

            if self.rect.left <= self.STOP_X:

                self._stopped = True
                self._attack_timer = 0.0
                self._fire_timer = 0.0

        elif not self._advancing:

            self._attack_timer += delta_time
            self._fire_timer -= delta_time

            if self._fire_timer <= 0:

                self._shoot()

                self._fire_timer = self.FIRE_COOLDOWN

            if self._attack_timer >= self.ATTACK_DURATION:

                self._advancing = True

        else:

            self.x -= self.SPEED * delta_time

            self.sync_rect()

            if self.rect.right < 0:

                self.destroy()

        if self.rect.right < 0:

            self.destroy()

        for bullet in self._bullets:

            bullet.update(
                delta_time,
            )

        self._bullets = [
            bullet
            for bullet in self._bullets
            if bullet.is_active
        ]

    def _shoot(
        self,
    ) -> None:
        """
        Fire a five-projectile spread.
        """

        spread = (
            -2,
            -1,
            0,
            1,
            2,
        )

        for direction in spread:

            bullet = HeavyShipBullet(
                self.rect.left,
                self.rect.centery,
                direction * self.SHOT_SPEED_Y,
            )

            self._bullets.append(
                bullet,
            )

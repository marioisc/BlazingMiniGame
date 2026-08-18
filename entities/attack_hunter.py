"""
Attack Hunter enemy for Operation Phoenix.

Sprint 5-B2
-----------
- Enters from the right side of the screen.
- One Hunter enters from above and one from below.
- Starts firing immediately after entering the screen.
- Moves toward the player's current position.
- Turns back before reaching the player's hitbox.
- Retreats through the same right-side entry route.
- A Hunter is discarded after completing its retreat.
"""

from __future__ import annotations

import pygame

from config import SCREEN_WIDTH
from entities.enemy import Enemy
from entities.enemy_bullet import EnemyBullet


class AttackHunter(Enemy):
    """
    Mobile attack enemy that performs a single attack run.
    """

    WIDTH: int = 48
    HEIGHT: int = 48

    COLOR: pygame.Color = pygame.Color("orange")

    SPEED: float = 260.0

    MAX_HEALTH: int = 80
    CONTACT_DAMAGE: int = 1
    SCORE_VALUE: int = 200

    FIRE_COOLDOWN: float = 2.5

    # Distance from the player's center at which the Hunter
    # abandons the attack run and starts retreating.
    SAFE_DISTANCE: float = 110.0

    PHASE_APPROACH: int = 0
    PHASE_RETREAT: int = 1

    def __init__(
        self,
        x: float,
        y: float,
        player,
    ) -> None:
        """
        Initialize an Attack Hunter.
        """

        super().__init__(
            x=x,
            y=y,
        )

        self._player = player
        self._phase = self.PHASE_APPROACH

        # The first shot is intentionally immediate once the
        # Hunter becomes visible.
        self._fire_timer = 0.0
        self._has_entered_screen = False

    def update(
        self,
        delta_time: float,
    ) -> None:
        """
        Update movement, firing and retreat state.
        """

        if not self.is_active:
            return

        if self._phase == self.PHASE_APPROACH:
            self._update_approach(delta_time)
        else:
            self._update_retreat(delta_time)

        self.sync_rect()

        self._update_firing(delta_time)

        for bullet in self._bullets:
            bullet.update(delta_time)

        self._bullets = [
            bullet
            for bullet in self._bullets
            if bullet.is_active
        ]

    def _update_approach(
        self,
        delta_time: float,
    ) -> None:
        """
        Move toward the player but turn around before impact.
        """

        target_x = float(self._player.x)
        target_y = float(self._player.y)

        dx = target_x - self.x
        dy = target_y - self.y

        distance = (dx * dx + dy * dy) ** 0.5

        if distance <= self.SAFE_DISTANCE:
            self._phase = self.PHASE_RETREAT
            return

        if distance <= 0.0:
            self._phase = self.PHASE_RETREAT
            return

        self.x += (
            dx / distance
        ) * self.SPEED * delta_time

        self.y += (
            dy / distance
        ) * self.SPEED * delta_time

    def _update_retreat(
        self,
        delta_time: float,
    ) -> None:
        """
        Return through the right side of the screen.
        """

        self.x += self.SPEED * delta_time

        if self.x > SCREEN_WIDTH:
            self.destroy()

    def _update_firing(
        self,
        delta_time: float,
    ) -> None:
        """
        Fire immediately after entering the screen and then
        continue firing while performing the attack run.
        """

        if not self._has_entered_screen:

            if self.rect.left <= SCREEN_WIDTH:

                self._has_entered_screen = True
                self._shoot()

                self._fire_timer = self.FIRE_COOLDOWN

            return

        self._fire_timer -= delta_time

        if self._fire_timer <= 0.0:

            self._shoot()

            self._fire_timer = self.FIRE_COOLDOWN

    def _shoot(
        self,
    ) -> None:
        """
        Fire two simple projectiles simultaneously.
        """

        self._bullets.append(
            EnemyBullet(
                self.rect.left,
                self.rect.centery - 10,
            )
        )

        self._bullets.append(
            EnemyBullet(
                self.rect.left,
                self.rect.centery + 10,
            )
        )

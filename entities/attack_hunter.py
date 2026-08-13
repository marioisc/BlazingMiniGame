"""
Attack Hunter enemy for Operation Phoenix.

Sprint 4-D4
-----------
- Medium-speed combat enemy.
- Medium resistance.
- Fires two simple projectiles simultaneously.
- Uses the existing EnemyBullet implementation.
"""

from __future__ import annotations

import pygame

from entities.enemy import Enemy
from entities.enemy_bullet import EnemyBullet


class AttackHunter(Enemy):
    """
    Attack Hunter enemy.

    The Attack Hunter keeps the base enemy movement behavior and
    replaces the default single-shot attack with a simultaneous
    two-projectile attack.
    """

    WIDTH: int = 48
    HEIGHT: int = 48

    COLOR: pygame.Color = pygame.Color("orange")

    SPEED: float = 150.0

    MAX_HEALTH: int = 80
    CONTACT_DAMAGE: int = 1
    SCORE_VALUE: int = 200

    FIRE_COOLDOWN: float = 2.5

    SHOT_OFFSET_Y: int = 10

    def _shoot(
        self,
    ) -> None:
        """
        Fire two simple projectiles simultaneously.
        """

        upper_bullet = EnemyBullet(
            self.rect.left,
            self.rect.centery - self.SHOT_OFFSET_Y,
        )

        lower_bullet = EnemyBullet(
            self.rect.left,
            self.rect.centery + self.SHOT_OFFSET_Y,
        )

        self._bullets.append(
            upper_bullet,
        )

        self._bullets.append(
            lower_bullet,
        )

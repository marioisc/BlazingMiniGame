"""
Sniper enemy for Operation Phoenix.

Design source:
- Long-range enemy.
- Keeps its distance.
- Single slow and powerful shot.
- Medium-high resistance.
"""

from __future__ import annotations

import pygame

from entities.enemy import Enemy


class SniperEnemy(Enemy):
    """
    Long-range enemy with a slow, powerful single shot.
    """

    WIDTH: int = 72
    HEIGHT: int = 40

    COLOR: pygame.Color = pygame.Color("firebrick")

    SPEED: float = 45.0

    MAX_HEALTH: int = 120
    CONTACT_DAMAGE: int = 1
    SCORE_VALUE: int = 400

    FIRE_COOLDOWN: float = 3.5

    BULLET_SPEED: float = -260.0
    BULLET_DAMAGE: int = 3

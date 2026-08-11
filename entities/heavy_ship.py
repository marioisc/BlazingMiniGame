"""
Heavy Ship enemy for Operation Phoenix.
"""

from __future__ import annotations

import pygame

from entities.enemy import Enemy


class HeavyShip(Enemy):
    """
    Slow and highly resistant enemy.
    """

    WIDTH: int = 72
    HEIGHT: int = 72

    COLOR: pygame.Color = pygame.Color("darkred")

    SPEED: float = 80.0

    MAX_HEALTH: int = 200
    CONTACT_DAMAGE: int = 2
    SCORE_VALUE: int = 500

    FIRE_COOLDOWN: float = 3.0

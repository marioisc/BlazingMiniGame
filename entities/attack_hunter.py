"""
Attack Hunter enemy for Operation Phoenix.
"""

from __future__ import annotations

import pygame

from entities.enemy import Enemy


class AttackHunter(Enemy):
    """
    Balanced enemy with medium resistance.
    """

    WIDTH: int = 48
    HEIGHT: int = 48

    COLOR: pygame.Color = pygame.Color("orange")

    SPEED: float = 150.0

    MAX_HEALTH: int = 80
    CONTACT_DAMAGE: int = 1
    SCORE_VALUE: int = 200

    FIRE_COOLDOWN: float = 2.5
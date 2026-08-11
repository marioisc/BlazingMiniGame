"""
Explorer Drone enemy for Operation Phoenix.
"""

from __future__ import annotations

import pygame

from entities.enemy import Enemy


class ExplorerDrone(Enemy):
    """
    Fast, low-resistance enemy used in groups of five.
    """

    WIDTH: int = 40
    HEIGHT: int = 40

    COLOR: pygame.Color = pygame.Color("limegreen")

    SPEED: float = 220.0

    MAX_HEALTH: int = 30
    CONTACT_DAMAGE: int = 1
    SCORE_VALUE: int = 100

    FIRE_COOLDOWN: float = 2.0

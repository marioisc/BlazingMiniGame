"""
Interceptor Angel enemy for Operation Phoenix.

Design source:
- Hunts the player relentlessly.
- Extremely fast and agile.
- Attacks in dives from above.
- Low resistance.
- Uses rapid linear bursts during dive attacks.
"""

from __future__ import annotations

import pygame

from entities.enemy import Enemy


class InterceptorAngel(Enemy):
    """
    Extremely fast interceptor designed around dive attacks.
    """

    WIDTH: int = 56
    HEIGHT: int = 56

    COLOR: pygame.Color = pygame.Color("royalblue")

    SPEED: float = 320.0

    MAX_HEALTH: int = 25
    CONTACT_DAMAGE: int = 2
    SCORE_VALUE: int = 300

    FIRE_COOLDOWN: float = 0.55

    DIVE_SPEED: float = 430.0
    DIVE_DURATION: float = 0.9
    RECOVERY_DURATION: float = 0.45

    BULLET_SPEED: float = -360.0
    BULLET_DAMAGE: int = 1

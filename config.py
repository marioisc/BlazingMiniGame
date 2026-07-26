"""
Global configuration for Operation Phoenix.

This module stores all configurable constants used by the game.
"""

from __future__ import annotations

import pygame

# ----------------------------------------------------------------------
# Window
# ----------------------------------------------------------------------

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

GAME_TITLE = "Operation Phoenix"

FPS = 60
# ----------------------------------------------------------------------
# Fonts
# ----------------------------------------------------------------------

DEFAULT_FONT = "arial"

DEFAULT_FONT_SIZE = 28
# ----------------------------------------------------------------------
# Colors
# ----------------------------------------------------------------------

BACKGROUND_COLOR: pygame.Color = pygame.Color(15, 18, 30)

PLAYER_COLOR: pygame.Color = pygame.Color(70, 180, 255)
HUD_COLOR = (240, 240, 240)

# ----------------------------------------------------------------------
# Player
# ----------------------------------------------------------------------

PLAYER_WIDTH: int = 48
PLAYER_HEIGHT: int = 48

PLAYER_SPEED: float = 320.0

# ----------------------------------------------------------------------
# Gameplay
# ----------------------------------------------------------------------

ENEMY_SPAWN_INTERVAL: float = 1.5

# ----------------------------------------------------------------------
# Score System
# ----------------------------------------------------------------------

# Points awarded for destroying one enemy.
SCORE_ENEMY_DESTROYED: int = 100

# Initial player score.
INITIAL_SCORE: int = 0

# Reserved for future combo system.
COMBO_START: int = 1

# Reserved for future score multiplier system.
SCORE_MULTIPLIER: float = 1.0

# Reserved for future bonus every N enemies destroyed.
BONUS_ENEMY_THRESHOLD: int = 10

# Reserved for future bonus reward.
BONUS_SCORE: int = 1000

# ----------------------------------------------------------------------
# Lives System (Functional Unit 6)
# ----------------------------------------------------------------------

# Initial number of player lives.
PLAYER_INITIAL_LIVES: int = 3

# Maximum number of lives the player can have.
PLAYER_MAX_LIVES: int = 5

# Points required to earn an extra life.
EXTRA_LIFE_SCORE: int = 10000

# Invulnerability time (seconds) after losing a life.
PLAYER_INVULNERABILITY_TIME: float = 2.0

# Reserved for future respawn delay.
PLAYER_RESPAWN_DELAY: float = 1.5

# Reserved for future Game Over delay.
GAME_OVER_DELAY: float = 3.0

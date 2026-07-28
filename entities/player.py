"""
Player entity.

Implements player movement, shooting and the first version
of the lives system.
"""

from __future__ import annotations

from typing import Sequence

import pygame

from config import (
    PLAYER_COLOR,
    PLAYER_HEIGHT,
    PLAYER_INITIAL_LIVES,
    PLAYER_INVULNERABILITY_TIME,
    PLAYER_MAX_LIVES,
    PLAYER_SPEED,
    PLAYER_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from entities.bullet import Bullet
from entities.entity import Entity


class Player(Entity):
    """
    Player controlled entity.
    """

    FIRE_COOLDOWN: float = 0.20

    def __init__(
        self,
        x: float,
        y: float,
    ) -> None:
        super().__init__(
            x=x,
            y=y,
            width=PLAYER_WIDTH,
            height=PLAYER_HEIGHT,
        )

        self._speed: float = PLAYER_SPEED

        self._fire_timer: float = 0.0

        self._bullets: list[Bullet] = []

        # ------------------------------------------------------------------
        # Lives system (Functional Unit 6)
        # ------------------------------------------------------------------
        self._lives: int = PLAYER_INITIAL_LIVES
        self._invulnerability_timer: float = 0.0

    def update(
        self,
        delta_time: float,
        keys: Sequence[bool],
    ) -> None:
        """
        Update player.
        """
        dx = 0.0
        dy = 0.0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self._speed * delta_time

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self._speed * delta_time

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self._speed * delta_time

        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self._speed * delta_time

        self.x += dx
        self.y += dy

        self.x = max(
            0,
            min(self.x, SCREEN_WIDTH - PLAYER_WIDTH),
        )

        self.y = max(
            0,
            min(self.y, SCREEN_HEIGHT - PLAYER_HEIGHT),
        )

        self.sync_rect()

        # Fire cooldown.
        if self._fire_timer > 0.0:
            self._fire_timer -= delta_time

        if keys[pygame.K_SPACE] and self._fire_timer <= 0.0:
            self._shoot()
            self._fire_timer = self.FIRE_COOLDOWN

        # Invulnerability timer.
        if self._invulnerability_timer > 0.0:
            self._invulnerability_timer -= delta_time

        # Update bullets.
        for bullet in self._bullets:
            bullet.update(delta_time)

        self._bullets = [
            bullet
            for bullet in self._bullets
            if bullet.is_active
            and bullet.rect.right > 0
            and bullet.rect.left < SCREEN_WIDTH
        ]

    def draw(
        self,
        surface: pygame.Surface,
    ) -> None:
        """
        Draw player.
        """
        # Blink while invulnerable.
        if (
            self.is_invulnerable
            and (pygame.time.get_ticks() // 100) % 2 == 0
        ):
            pass
        else:
            pygame.draw.rect(
                surface,
                PLAYER_COLOR,
                self.rect,
            )

        for bullet in self._bullets:
            bullet.draw(surface)

    def _shoot(self) -> None:
        """
        Spawn a new bullet.
        """
        bullet = Bullet(
            x=self.x + (PLAYER_WIDTH / 2),
            y=self.y,
        )

        self._bullets.append(bullet)

    def lose_life(self) -> bool:
        """
        Remove one life from the player.

        Returns:
            True if a life was lost.
            False if the player was invulnerable.
        """
        if self.is_invulnerable:
            return False

        if self._lives > 0:
            self._lives -= 1

        self._invulnerability_timer = PLAYER_INVULNERABILITY_TIME

        return True

    def add_life(self) -> None:
        """
        Increase player lives up to the maximum.
        """
        self._lives = min(
            self._lives + 1,
            PLAYER_MAX_LIVES,
        )

    @property
    def bullets(self) -> list[Bullet]:
        """
        Active bullets.
        """
        return self._bullets

    @property
    def lives(self) -> int:
        """
        Current player lives.
        """
        return self._lives

    @property
    def is_invulnerable(self) -> bool:
        """
        True while the player is temporarily invulnerable.
        """
        return self._invulnerability_timer > 0.0

    @property
    def is_alive(self) -> bool:
        """
        True if the player still has lives remaining.
        """
        return self._lives > 0

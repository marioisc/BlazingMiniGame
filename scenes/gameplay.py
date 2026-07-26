"""
Gameplay scene.

Main gameplay implementation.

Functional Unit 6 - Part C
- Enemy/player collisions.
- Player lives display.
- Basic Game Over state.
"""

from __future__ import annotations

import random

import pygame

from config import (
    BACKGROUND_COLOR,
    ENEMY_SPAWN_INTERVAL,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

from entities.enemy import Enemy
from entities.player import Player

from scenes.scene import Scene


class Gameplay(Scene):

    def __init__(self, game) -> None:

        super().__init__(game)

        self.player = Player(
            100,
            SCREEN_HEIGHT // 2,
        )

        self.enemies: list[Enemy] = []

        self.enemy_spawn_timer = 0.0

    def handle_events(
        self,
        events: list[pygame.event.Event],
    ) -> None:

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.game.running = False

    def update(
        self,
        delta_time: float,
    ) -> None:

        keys = pygame.key.get_pressed()

        self.player.update(
            delta_time,
            keys,
        )

        self.enemy_spawn_timer += delta_time

        if self.enemy_spawn_timer >= ENEMY_SPAWN_INTERVAL:

            self.spawn_enemy()

            self.enemy_spawn_timer = 0.0

        for enemy in self.enemies:

            enemy.update(delta_time)

        self.enemies = [
            enemy
            for enemy in self.enemies
            if enemy.is_active
        ]

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:

        screen.fill(BACKGROUND_COLOR)

        self.player.draw(screen)

        for enemy in self.enemies:

            enemy.draw(screen)

    def spawn_enemy(self) -> None:

        enemy = Enemy(
            SCREEN_WIDTH,
            random.randint(
                0,
                SCREEN_HEIGHT - Enemy.HEIGHT,
            ),
        )

        self.enemies.append(enemy)
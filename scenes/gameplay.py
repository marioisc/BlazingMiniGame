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
    DEFAULT_FONT,
    DEFAULT_FONT_SIZE,
    ENEMY_SPAWN_INTERVAL,
    HUD_COLOR,
    INITIAL_SCORE,
    SCORE_ENEMY_DESTROYED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

from entities.enemy import Enemy
from entities.player import Player

from scenes.scene import Scene


class Gameplay(Scene):

    def __init__(
        self,
        game,
    ) -> None:

        super().__init__(game)

        self.player = Player(
            100,
            SCREEN_HEIGHT // 2,
        )

        self.enemies: list[Enemy] = []

        self.enemy_spawn_timer = 0.0

        self.score = INITIAL_SCORE

        self.font = pygame.font.SysFont(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        )

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

            enemy.update(
                delta_time,
            )

        self.check_bullet_enemy_collisions()

        self.check_player_enemy_collisions()

        self.check_enemy_bullet_collisions()

        self.enemies = [

            enemy

            for enemy in self.enemies

            if enemy.is_active

        ]

        for enemy in self.enemies:

            enemy._bullets = [

                bullet

                for bullet in enemy.bullets

                if bullet.is_active

            ]

        self.player._bullets = [

            bullet

            for bullet in self.player.bullets

            if bullet.is_active

        ]

        if not self.player.is_alive:

            self.game.show_game_over()

            return

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:

        screen.fill(
            BACKGROUND_COLOR,
        )

        self.player.draw(
            screen,
        )

        for enemy in self.enemies:

            enemy.draw(
                screen,
            )

        self.draw_hud(
            screen,
        )

    def spawn_enemy(
        self,
    ) -> None:

        enemy = Enemy(

            SCREEN_WIDTH,

            random.randint(

                0,

                SCREEN_HEIGHT - Enemy.HEIGHT,

            ),

        )

        self.enemies.append(
            enemy,
        )
    def check_bullet_enemy_collisions(
        self,
    ) -> None:

        for bullet in self.player.bullets:

            if not bullet.is_active:

                continue

            for enemy in self.enemies:

                if not enemy.is_active:

                    continue

                if bullet.collides_with(enemy):

                    bullet.destroy()

                    enemy.destroy()

                    self.score += SCORE_ENEMY_DESTROYED

                    break

    def check_player_enemy_collisions(
        self,
    ) -> None:

        if self.player.is_invulnerable:

            return

        for enemy in self.enemies:

            if not enemy.is_active:

                continue

            if self.player.collides_with(enemy):

                enemy.destroy()

                self.player.lose_life()

                break

    def check_enemy_bullet_collisions(
        self,
    ) -> None:

        if self.player.is_invulnerable:

            return

        for enemy in self.enemies:

            for bullet in enemy.bullets:

                if not bullet.is_active:

                    continue

                if bullet.collides_with(self.player):

                    bullet.destroy()

                    self.player.lose_life()

                    return

    def draw_hud(
        self,
        screen: pygame.Surface,
    ) -> None:

        score_surface = self.font.render(

            f"Score: {self.score}",

            True,

            HUD_COLOR,

        )

        lives_surface = self.font.render(

            f"Lives: {self.player.lives}",

            True,

            HUD_COLOR,

        )

        screen.blit(

            score_surface,

            (
                20,
                20,
            ),

        )

        screen.blit(

            lives_surface,

            (
                20,
                60,
            ),

        )                    
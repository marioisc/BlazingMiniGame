"""
Gameplay scene.

Sprint 4-D5
-----------
Heavy Ship integration.

Wave 1 uses Explorer Drone formations.
Wave 2 uses individual Attack Hunters.
Wave 3 uses individual Heavy Ships.
Wave 4 uses Sniper Enemies and Interceptor Angels.

Explorer Drone rules:
- One formation contains five drones.
- Wave 1 has ten enemy slots, therefore two formations are spawned.
- The five drones share movement timing and fire simultaneously.
- Power-up logic is intentionally not implemented yet.
"""

from __future__ import annotations

import random

import pygame

from config import (
    BACKGROUND_COLOR,
    DEFAULT_FONT,
    DEFAULT_FONT_SIZE,
    HUD_COLOR,
    INITIAL_SCORE,
    SCORE_ENEMY_DESTROYED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)

from entities.enemy import Enemy
from entities.explorer_drone import ExplorerDrone
from entities.attack_hunter import AttackHunter
from entities.heavy_ship import HeavyShip
from entities.sniper_enemy import SniperEnemy
from entities.interceptor_angel import InterceptorAngel
from entities.explorer_drone_formation import ExplorerDroneFormation
from entities.player import Player

from scenes.scene import Scene


class Gameplay(Scene):
    """
    Main gameplay scene.
    """

    def __init__(
        self,
        game,
    ) -> None:
        """
        Initialize the gameplay scene.
        """

        from systems.mission_manager import MissionManager

        self.mission = MissionManager()
        self.mission.start()

        super().__init__(game)

        self.player = Player(
            100,
            SCREEN_HEIGHT // 2,
        )

        # Individual enemies remain in this collection so the existing
        # collision system can continue working without knowing about
        # formation objects.
        self.enemies: list[Enemy] = []

        # Explorer Drone formations are managed separately because one
        # formation represents five individual enemies.
        self._explorer_formations: list[ExplorerDroneFormation] = []

        self.enemy_spawn_timer = 0.0

        self.score = INITIAL_SCORE

        self.font = pygame.font.SysFont(
            DEFAULT_FONT,
            DEFAULT_FONT_SIZE,
        )

    # ==============================================================
    # Public
    # ==============================================================

    def handle_events(
        self,
        events: list[pygame.event.Event],
    ) -> None:
        """
        Process gameplay events.
        """

        for event in events:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(
        self,
        delta_time: float,
    ) -> None:
        """
        Update all gameplay systems.
        """

        self.mission.update(
            delta_time,
        )

        self.update_player(
            delta_time,
        )

        self.spawn_enemies(
            delta_time,
        )

        self.update_enemies(
            delta_time,
        )

        self.update_collisions()

        self.cleanup_entities()

        self.update_game_state()

    def draw(
        self,
        screen: pygame.Surface,
    ) -> None:
        """
        Draw the complete gameplay scene.
        """

        self.draw_background(
            screen,
        )

        self.draw_entities(
            screen,
        )

        self.draw_hud(
            screen,
        )

        self.draw_mission_message(
            screen,
        )

    # ==============================================================
    # Update
    # ==============================================================

    def update_player(
        self,
        delta_time: float,
    ) -> None:
        """
        Update the player.
        """

        keys = pygame.key.get_pressed()

        self.player.update(
            delta_time,
            keys,
        )

    def spawn_enemies(
        self,
        delta_time: float,
    ) -> None:
        """
        Spawn enemies according to the current wave.

        Wave 1 uses five-drone Explorer formations.
        Wave 2 uses individual Attack Hunters.
        Wave 3 uses individual Heavy Ships.
        Wave 4 keeps the previous single-Enemy behavior until its
        dedicated enemy integration sprint.
        """

        self.enemy_spawn_timer += delta_time

        if (
            self.enemy_spawn_timer
            < self.mission.current_wave.spawn_interval
        ):
            return

        if not self.mission.should_spawn_enemy():
            return

        spawned_count = self.spawn_enemy()

        if spawned_count <= 0:
            return

        for _ in range(spawned_count):
            self.mission.enemy_spawned()

        self.enemy_spawn_timer = 0.0

    def update_enemies(
        self,
        delta_time: float,
    ) -> None:
        """
        Update formations and standalone enemies.

        Explorer Drones are updated by their formation controller.
        They are skipped in the standalone enemy loop to avoid updating
        them twice per frame.

        Attack Hunters, Heavy Ships, Sniper Enemies, Interceptor Angels and the base Enemy are
        updated through the normal standalone enemy path.
        """

        for formation in self._explorer_formations:
            formation.update(
                delta_time,
            )

        for enemy in self.enemies:

            if isinstance(
                enemy,
                ExplorerDrone,
            ):
                continue

            enemy.update(
                delta_time,
            )

    def update_collisions(
        self,
    ) -> None:
        """
        Run all gameplay collision checks.
        """

        self.check_bullet_enemy_collisions()

        self.check_player_enemy_collisions()

        self.check_enemy_bullet_collisions()

    def cleanup_entities(
        self,
    ) -> None:
        """
        Remove inactive entities and finished Explorer formations.
        """

        self.player.cleanup_bullets()

        for enemy in self.enemies:
            enemy.cleanup_bullets()

        self.enemies = [
            enemy
            for enemy in self.enemies
            if enemy.is_active
        ]

        self._explorer_formations = [
            formation
            for formation in self._explorer_formations
            if formation.is_active
        ]

    def update_game_state(
        self,
    ) -> None:
        """
        Handle the current player mission state.
        """

        if not self.player.is_alive:

            self.mission.fail()

            self.game.show_game_over()

            return

    # ==============================================================
    # Draw
    # ==============================================================

    def draw_background(
        self,
        screen: pygame.Surface,
    ) -> None:
        """
        Draw the gameplay background.
        """

        screen.fill(
            BACKGROUND_COLOR,
        )

    def draw_entities(
        self,
        screen: pygame.Surface,
    ) -> None:
        """
        Draw the player and all active enemies.
        """

        self.player.draw(
            screen,
        )

        for enemy in self.enemies:

            enemy.draw(
                screen,
            )

            if isinstance(
                enemy,
                (HeavyShip, SniperEnemy, InterceptorAngel),
            ):

                self.draw_enemy_health(
                    screen,
                    enemy,
                )

    def draw_enemy_health(
        self,
        screen: pygame.Surface,
        enemy,
    ) -> None:
        """
        Draw a health bar above a multi-hit enemy.
        """

        bar_width = enemy.WIDTH
        bar_height = 5

        x = enemy.rect.left
        y = enemy.rect.top - 8

        pygame.draw.rect(
            screen,
            pygame.Color("black"),
            (
                x,
                y,
                bar_width,
                bar_height,
            ),
        )

        health_ratio = (
            enemy.health / enemy.MAX_HEALTH
        )

        pygame.draw.rect(
            screen,
            pygame.Color("red"),
            (
                x,
                y,
                int(bar_width * health_ratio),
                bar_height,
            ),
        )

    def draw_hud(
        self,
        screen: pygame.Surface,
    ) -> None:
        """
        Draw score and lives.
        """

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

    def draw_mission_message(
        self,
        screen: pygame.Surface,
    ) -> None:
        """
        Draw the current mission message when visible.
        """

        if not self.mission.is_message_visible:
            return

        message_surface = self.font.render(
            self.mission.mission_message,
            True,
            HUD_COLOR,
        )

        message_rect = message_surface.get_rect(
            center=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
            ),
        )

        screen.blit(
            message_surface,
            message_rect,
        )

    # ==============================================================
    # Collision Detection
    # ==============================================================

    def check_bullet_enemy_collisions(
        self,
    ) -> None:
        """
        Check player projectile collisions against enemies.
        """

        for bullet in self.player.bullets:

            if not bullet.is_active:
                continue

            for enemy in self.enemies:

                if not enemy.is_active:
                    continue

                if bullet.collides_with(enemy):

                    bullet.destroy()

                    if isinstance(
                        enemy,
                        (HeavyShip, SniperEnemy, InterceptorAngel),
                    ):

                        if enemy.take_damage(1):

                            self.mission.enemy_destroyed()

                            self.score += enemy.SCORE_VALUE

                    else:

                        enemy.destroy()

                        self.mission.enemy_destroyed()

                        self.score += (
                            getattr(
                                enemy,
                                "SCORE_VALUE",
                                SCORE_ENEMY_DESTROYED,
                            )
                        )

                    break

    def check_player_enemy_collisions(
        self,
    ) -> None:
        """
        Check direct player/enemy collisions.
        """

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
        """
        Check enemy projectile collisions against the player.
        """

        if self.player.is_invulnerable:
            return

        for enemy in self.enemies:

            for bullet in enemy.bullets:

                if not bullet.is_active:
                    continue

                if bullet.collides_with(
                    self.player,
                ):

                    bullet.destroy()

                    self.player.lose_life()

                    return

    # ==============================================================
    # Helpers
    # ==============================================================

    def spawn_enemy(
        self,
    ) -> int:
        """
        Spawn an enemy unit.

        Returns the number of individual enemies registered with the
        MissionManager.

        Wave 1:
            Creates one Explorer Drone formation containing five drones.

        Wave 2:
            Creates one Attack Hunter.

        Wave 3:
            Creates one Heavy Ship.

        Wave 4:
            Creates one Sniper Enemy.

        Other waves:
            Creates one standard Enemy.
        """

        if self.mission.current_wave_number == 1:

            remaining = (
                self.mission.current_wave.enemy_count
                - self.mission.stage.enemies_spawned
            )

            if remaining >= ExplorerDroneFormation.GROUP_SIZE:

                formation = ExplorerDroneFormation(
                    SCREEN_WIDTH,
                    random.randint(
                        80,
                        SCREEN_HEIGHT - 120,
                    ),
                )

                self._explorer_formations.append(
                    formation,
                )

                self.enemies.extend(
                    formation.drones,
                )

                return ExplorerDroneFormation.GROUP_SIZE

        if self.mission.current_wave_number == 2:

            enemy = AttackHunter(
                SCREEN_WIDTH,
                random.randint(
                    0,
                    SCREEN_HEIGHT - AttackHunter.HEIGHT,
                ),
            )

            self.enemies.append(
                enemy,
            )

            return 1

        if self.mission.current_wave_number == 3:

            enemy = HeavyShip(
                SCREEN_WIDTH,
                random.randint(
                    0,
                    SCREEN_HEIGHT - HeavyShip.HEIGHT,
                ),
            )

            self.enemies.append(
                enemy,
            )

            return 1

        if self.mission.current_wave_number == 4:

            if random.random() < 0.5:

                enemy = SniperEnemy(
                    SCREEN_WIDTH,
                    random.randint(
                        0,
                        SCREEN_HEIGHT - SniperEnemy.HEIGHT,
                    ),
                )

            else:

                enemy = InterceptorAngel(
                    SCREEN_WIDTH,
                    random.randint(
                        40,
                        180,
                    ),
                )

            self.enemies.append(
                enemy,
            )

            return 1

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

        return 1

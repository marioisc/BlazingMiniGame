"""
Gameplay scene.

Sprint 4-D3
-----------
Explorer Drone integration.

This version keeps the existing Gameplay responsibilities while adding
Explorer Drone formations to Wave 1 only. Other waves continue using the
base Enemy until their dedicated enemy integration sprints.

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

        Wave 1 is integrated with the five-drone Explorer formation.
        Other waves keep the previous single-Enemy behavior until their
        dedicated enemy integration sprints are implemented.
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

                    enemy.destroy()

                    self.mission.enemy_destroyed()

                    self.score += SCORE_ENEMY_DESTROYED

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

        Other waves:
            Creates one standard Enemy.
        """

        if self.mission.current_wave_number == 1:

            remaining = (
                self.mission.current_wave.enemy_count
                - self.mission.stage.enemies_spawned
            )

            # A formation always contains five drones. Do not create a
            # formation when fewer than five slots remain.
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

"""
==========================================================
Project : Operation Phoenix
Version : 0.4.0

Archivo:
    stage_manager.py

Responsabilidades
-----------------
- Administrar las oleadas del escenario.
- Llevar el progreso del Stage.
- Controlar la transición entre oleadas.

No crea enemigos.

No conoce Gameplay.

No conoce Player.

No conoce Enemy.
==========================================================
"""

from __future__ import annotations
from systems.wave import Wave


class StageManager:

    TOTAL_WAVES = 4

    WAVES = (

        Wave(
            enemy_count=10,
            spawn_interval=1.50,
        ),

        Wave(
            enemy_count=15,
            spawn_interval=1.35,
        ),

        Wave(
            enemy_count=20,
            spawn_interval=1.20,
        ),

        Wave(
            enemy_count=25,
            spawn_interval=1.00,
        ),
    )

    def __init__(
        self,
    ) -> None:

        self._current_wave = 1

        self._enemies_spawned = 0

        self._enemies_destroyed = 0

    @property
    def current_wave(
        self,
    ) -> int:

        return self._current_wave

    @property
    def current_wave_data(
        self,
    ) -> Wave:

        return self.WAVES[
            self._current_wave - 1
        ]

    @property
    def enemies_spawned(
        self,
    ) -> int:

        return self._enemies_spawned

    @property
    def enemies_destroyed(
        self,
    ) -> int:

        return self._enemies_destroyed

    @property
    def enemies_remaining(
        self,
    ) -> int:

        return max(
            0,
            self.current_wave_data.enemy_count
            - self._enemies_destroyed,
        )

    @property
    def can_spawn_enemy(
        self,
    ) -> bool:

        return (
            self._enemies_spawned
            < self.current_wave_data.enemy_count
        )

    @property
    def wave_completed(
        self,
    ) -> bool:

        return (
            self._enemies_destroyed
            >= self.current_wave_data.enemy_count
        )

    @property
    def stage_completed(
        self,
    ) -> bool:

        return (
            self.wave_completed
            and self._current_wave
            >= self.TOTAL_WAVES
        )

    def enemy_spawned(
        self,
    ) -> None:

        self._enemies_spawned += 1

    def enemy_destroyed(
        self,
    ) -> None:

        self._enemies_destroyed += 1

    def next_wave(
        self,
    ) -> None:

        if self.stage_completed:

            return

        self._current_wave += 1

        self._enemies_spawned = 0

        self._enemies_destroyed = 0
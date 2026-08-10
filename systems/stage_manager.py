"""
==========================================================
Project : Operation Phoenix
Version : 0.4.0

Archivo:
    stage_manager.py

Responsabilidades
-----------------
- Administrar las oleadas del escenario.
- Llevar el progreso de las oleadas.
- Controlar la cantidad de enemigos que
  corresponden a cada oleada.

No crea enemigos.

No controla Gameplay.

No conoce Player.

No conoce Enemy.

No controla temporizadores de transición.
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
            duration=10.0,
        ),

        Wave(
            enemy_count=15,
            spawn_interval=1.35,
            duration=10.0,
        ),

        Wave(
            enemy_count=20,
            spawn_interval=1.20,
            duration=10.0,
        ),

        Wave(
            enemy_count=25,
            spawn_interval=1.00,
            duration=10.0,
            message="Get ready for the boss!",
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
    def can_spawn_enemy(
        self,
    ) -> bool:

        return (
            self._enemies_spawned
            < self.current_wave_data.enemy_count
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
    ) -> bool:

        if self._current_wave >= self.TOTAL_WAVES:

            return False

        self._current_wave += 1

        self._enemies_spawned = 0

        self._enemies_destroyed = 0

        return True

    def should_spawn_enemy(
        self,
    ) -> bool:

        return self.can_spawn_enemy

    @property
    def wave_name(
        self,
    ) -> str:

        return f"Wave {self.current_wave}"
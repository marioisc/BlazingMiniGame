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
    TRANSITION_TIME = 2.0

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

        self._is_transitioning = False

        self._transition_timer = 0.0

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
            self.all_enemies_spawned and self.active_enemies == 0
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

    def should_spawn_enemy(
        self,
    ) -> bool:

        return (
                self.can_spawn_enemy and not self._is_transitioning
        )
    
    @property
    def wave_name(self) -> str:
        return f"Wave {self.current_wave}"

    @property
    def is_transitioning(
        self,
    ) -> bool:

        return self._is_transitioning
    
    def start_transition(
        self,
    ) -> None:

        self._is_transitioning = True

        self._transition_timer = self.TRANSITION_TIME

    def update(
        self,
        delta_time: float,
    ) -> None:

        if not self._is_transitioning:

            return

        self._transition_timer -= delta_time

        if self._transition_timer > 0:

            return

        self._is_transitioning = False

        self.next_wave()
    @property
    def all_enemies_spawned(
        self,
    ) -> bool:

        return (

            self._enemies_spawned

            >=

            self.current_wave_data.enemy_count

        )
    @property
    def active_enemies(
        self,
    ) -> int:

        return (

            self._enemies_spawned

            -

            self._enemies_destroyed

        )
    
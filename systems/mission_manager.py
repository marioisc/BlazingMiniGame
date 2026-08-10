"""
==========================================================
Project : Operation Phoenix
Version : 0.4.0

Archivo:
    mission_manager.py

Responsabilidades
-----------------
- Administrar el flujo completo de la misión.
- Controlar el estado actual.
- Controlar el tiempo de cada oleada.
- Mantener el StageManager como responsable
  de las oleadas.

No crea enemigos.

No conoce Gameplay.

No conoce Player.

No conoce Enemy.
==========================================================
"""

from __future__ import annotations

from systems.mission_state import MissionState
from systems.stage_manager import StageManager


class MissionManager:

    def __init__(
        self,
    ) -> None:

        self._state = MissionState.MISSION_START

        self._stage = StageManager()

        self._remaining_wave_time = 0.0

    @property
    def state(
        self,
    ) -> MissionState:

        return self._state

    @property
    def stage(
        self,
    ) -> StageManager:

        return self._stage

    @property
    def is_playing(
        self,
    ) -> bool:

        return self._state == MissionState.WAVE

    def start(
        self,
    ) -> None:

        self._state = MissionState.WAVE

        self._remaining_wave_time = (
            self.current_wave.duration
        )

    def complete(
        self,
    ) -> None:

        self._state = MissionState.MISSION_COMPLETE

    def fail(
        self,
    ) -> None:

        self._state = MissionState.MISSION_FAILED

    def update(
        self,
        delta_time: float,
    ) -> None:

        if self._state != MissionState.WAVE:

            return

        self._remaining_wave_time -= delta_time

        if self._remaining_wave_time > 0:

            return

        self._advance_wave()

    def should_spawn_enemy(
        self,
    ) -> bool:

        return self._stage.should_spawn_enemy()

    def enemy_spawned(
        self,
    ) -> None:

        self._stage.enemy_spawned()

    def enemy_destroyed(
        self,
    ) -> None:

        self._stage.enemy_destroyed()

    @property
    def current_wave(
        self,
    ) -> Wave:

        return self._stage.current_wave_data

    @property
    def current_wave_number(
        self,
    ) -> int:

        return self._stage.current_wave

    def next_wave(
        self,
    ) -> None:

        if not self._stage.next_wave():

            self._state = MissionState.BOSS_WARNING

            return

        self._remaining_wave_time = (
            self.current_wave.duration
        )

    @property
    def enemies_remaining(
        self,
    ) -> int:

        return self._stage.active_enemies

    @property
    def remaining_wave_time(
        self,
    ) -> float:

        return self._remaining_wave_time

    def _advance_wave(
        self,
    ) -> None:

        if not self._stage.next_wave():

            self._state = MissionState.BOSS_WARNING

            return

        self._remaining_wave_time = (
            self.current_wave.duration
        )
        
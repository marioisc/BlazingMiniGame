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
from systems.wave import Wave


class MissionManager:
    MESSAGE_DURATION = 3.0

    def __init__(
        self,
    ) -> None:

        self._state = MissionState.MISSION_START

        self._stage = StageManager()

        self._remaining_wave_time = 0.0
        self._mission_message = None
        self._message_timer = 0.0

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
    @property
    def mission_message(
        self,
    ) -> str | None:

        return self._mission_message
    
    @property
    def is_message_visible(
        self,
    ) -> bool:

        return (
            self._state == MissionState.BOSS_WARNING
            and self._mission_message is not None
            and self._message_timer > 0
        )
    
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

        if self._state == MissionState.WAVE:
            self._remaining_wave_time -= delta_time

            if self._remaining_wave_time <= 0:

                self._advance_wave()
            return
        if self._state == MissionState.BOSS_WARNING:
            if self._message_timer > 0:
                self._message_timer -= delta_time
                if self._message_timer < 0:
                    self._message_timer = 0.0
                
        

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

    @property
    def remaining_wave_time(
        self,
    ) -> float:

        return self._remaining_wave_time

    def _advance_wave(
        self,
    ) -> None:

        if not self._stage.next_wave():
            self._mission_message = (self.current_wave.message)
            self._message_timer = (self.MESSAGE_DURATION)

            self._state = MissionState.BOSS_WARNING

            return

        self._remaining_wave_time = (
            self.current_wave.duration
        )
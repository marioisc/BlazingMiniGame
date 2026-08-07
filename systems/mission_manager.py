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

        self._stage.update(
            delta_time,
        )
        
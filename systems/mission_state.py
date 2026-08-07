"""
==========================================================
Project : Operation Phoenix
Version : 0.4.0

Archivo:
    mission_state.py

Descripción
-----------
Estados posibles del flujo de una misión.
==========================================================
"""

from enum import Enum
from enum import auto


class MissionState(Enum):

    MISSION_START = auto()

    WAVE = auto()

    TRANSITION = auto()

    BOSS_WARNING = auto()

    BOSS = auto()

    MISSION_COMPLETE = auto()

    MISSION_FAILED = auto()

    EXIT = auto()
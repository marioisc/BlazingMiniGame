from __future__ import annotations


class Wave:

    def __init__(
        self,
        enemy_count: int,
        spawn_interval: float,
        duration: float,
        message: str | None = None,
        message_time: float | None = None,
    ) -> None:

        self._enemy_count = enemy_count

        self._spawn_interval = spawn_interval

        self._duration = duration

        self._message = message

        self._message_time = message_time

    @property
    def enemy_count(
        self,
    ) -> int:

        return self._enemy_count

    @property
    def spawn_interval(
        self,
    ) -> float:

        return self._spawn_interval

    @property
    def duration(
        self,
    ) -> float:

        return self._duration

    @property
    def message(
        self,
    ) -> str | None:

        return self._message
    @property
    def message_time(
        self,
    ) -> float | None:

        return self._message_time
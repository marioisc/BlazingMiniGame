from __future__ import annotations


class Wave:

    def __init__(
        self,
        enemy_count: int,
        spawn_interval: float,
        message: str | None = None,
    ) -> None:

        self._enemy_count = enemy_count

        self._spawn_interval = spawn_interval

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

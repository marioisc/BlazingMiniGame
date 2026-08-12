"""
Explorer Drone group support for Operation Phoenix.

Sprint 4-D3 Hotfix
------------------
Keeps the five Explorer Drones synchronized for movement timing
and simultaneous firing.

The formation is horizontal: all drones share the same Y position
and enter the screen one behind another on the X axis.
"""

from __future__ import annotations

from entities.explorer_drone import ExplorerDrone, ExplorerDroneGroup


class ExplorerDroneFormation:
    """
    Controls one group of five Explorer Drones.

    The five drones form a horizontal line and move together from
    right to left. They share one firing timer so all active drones
    fire simultaneously.
    """

    GROUP_SIZE: int = 5

    HORIZONTAL_SPACING: int = 52

    def __init__(
        self,
        x: float,
        y: float,
    ) -> None:
        """
        Create a five-drone horizontal formation.
        """

        self._group = ExplorerDroneGroup()

        self._drones = [
            ExplorerDrone(
                x=x + index * self.HORIZONTAL_SPACING,
                y=y,
                group=self._group,
            )
            for index in range(self.GROUP_SIZE)
        ]

    @property
    def drones(
        self,
    ) -> list[ExplorerDrone]:
        """
        Return the drones belonging to this formation.
        """

        return self._drones

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return whether at least one drone remains active.
        """

        return any(
            drone.is_active
            for drone in self._drones
        )

    def update(
        self,
        delta_time: float,
    ) -> None:
        """
        Update the group and synchronize its firing.
        """

        self._group.fire_timer -= delta_time

        if self._group.fire_timer <= 0:
            self._group.fire_timer = self._group.fire_cooldown

            for drone in self._drones:
                drone.fire()

        for drone in self._drones:
            drone.update(delta_time)

    def draw(
        self,
        surface,
    ) -> None:
        """
        Draw every drone in the formation.
        """

        for drone in self._drones:
            drone.draw(surface)

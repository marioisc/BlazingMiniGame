"""
Explorer Drone formation for Operation Phoenix.

Sprint 5-A1
-----------
- Five drones per horizontal row.
- Two rows spawn together as one ten-drone batch.
- Rows perform a full-screen vertical zig-zag.
- Initial firing starts three seconds after the batch appears.
- All active drones in each row fire simultaneously.
"""

from __future__ import annotations

from entities.explorer_drone import ExplorerDrone, ExplorerDroneGroup


class ExplorerDroneFormation:
    """
    Controls one horizontal row of five Explorer Drones.

    Two instances of this formation are created by Gameplay for
    each Wave 1 batch.
    """

    GROUP_SIZE: int = 5

    HORIZONTAL_SPACING: int = 52

    ZIGZAG_SPEED: float = 180.0

    TOP_MARGIN: int = 20
    BOTTOM_MARGIN: int = 60

    INITIAL_FIRE_DELAY: float = 3.0

    def __init__(
        self,
        x: float,
        y: float,
        vertical_direction: int = 1,
    ) -> None:
        """
        Create a five-drone horizontal formation.

        Args:
            x: Initial horizontal position.
            y: Initial vertical position.
            vertical_direction: 1 moves downward first,
                -1 moves upward first.
        """

        self._group = ExplorerDroneGroup()

        # The original group cooldown remains 2 seconds. Only the
        # first firing is delayed by three seconds.
        self._group.fire_timer = self.INITIAL_FIRE_DELAY

        self._y = float(y)

        self._vertical_direction = (
            1 if vertical_direction >= 0 else -1
        )

        self._drones = [
            ExplorerDrone(
                x=x + index * self.HORIZONTAL_SPACING,
                y=self._y,
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
        Update horizontal movement, zig-zag movement and firing.
        """

        self._update_vertical_position(
            delta_time,
        )

        self._group.fire_timer -= delta_time

        if self._group.fire_timer <= 0:

            self._group.fire_timer = (
                self._group.fire_cooldown
            )

            for drone in self._drones:
                drone.fire()

        for drone in self._drones:

            drone.y = self._y

            drone.update(
                delta_time,
            )

            # ExplorerDrone.update() synchronizes the rect after
            # moving horizontally. Restore the formation Y after it.
            drone.y = self._y
            drone.sync_rect()

    def _update_vertical_position(
        self,
        delta_time: float,
    ) -> None:
        """
        Move the formation vertically and bounce at screen limits.
        """

        from config import SCREEN_HEIGHT

        self._y += (
            self.ZIGZAG_SPEED
            * self._vertical_direction
            * delta_time
        )

        max_y = (
            SCREEN_HEIGHT
            - self.BOTTOM_MARGIN
        )

        if self._y >= max_y:

            self._y = float(max_y)
            self._vertical_direction = -1

        elif self._y <= self.TOP_MARGIN:

            self._y = float(self.TOP_MARGIN)
            self._vertical_direction = 1

    def draw(
        self,
        surface,
    ) -> None:
        """
        Draw every drone in the formation.
        """

        for drone in self._drones:
            drone.draw(surface)

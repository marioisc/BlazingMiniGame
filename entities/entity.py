"""
==========================================================
Project : Operation Phoenix
Version : 0.1.0

Archivo:
    entity.py

Descripción:
    Clase base para todas las entidades del videojuego.

Todas las entidades del juego deberán heredar de esta clase.

Ejemplos:

    Player
    Enemy
    Bullet
    Boss
    Explosion
    PowerUp

Responsabilidades

    • Posición
    • Tamaño
    • Velocidad
    • Estado
    • Colisiones
    • Actualización
    • Renderizado

La clase NO conoce nada sobre escenas, teclado,
mouse o cualquier otro sistema del juego.
==========================================================
"""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

import pygame


class Entity(ABC):
    """
    Clase base de todas las entidades del juego.

    Esta clase encapsula únicamente el comportamiento
    común entre todas las entidades.
    """

    def __init__(
        self,
        x: float,
        y: float,
        width: int,
        height: int
    ) -> None:

        # ==================================================
        # Transform
        # ==================================================

        self.x: float = x
        self.y: float = y

        # ==================================================
        # Size
        # ==================================================

        self.width: int = width
        self.height: int = height

        # ==================================================
        # Velocity
        # ==================================================

        self.velocity_x: float = 0.0
        self.velocity_y: float = 0.0

        # ==================================================
        # State
        # ==================================================

        self.active: bool = True

        # ==================================================
        # Collision
        # ==================================================

        self.rect = pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    # ======================================================
    # Update
    # ======================================================

    def update(
        self,
        delta_time: float
    ) -> None:
        """
        Actualiza la posición utilizando
        la velocidad actual.
        """

        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time

        self.sync_rect()

    # ======================================================
    # Draw
    # ======================================================

    @abstractmethod
    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        """
        Cada entidad es responsable
        de dibujarse a sí misma.
        """
        pass

    # ======================================================
    # Collision
    # ======================================================

    def collides_with(
        self,
        other: "Entity"
    ) -> bool:
        """
        Comprueba la colisión entre dos entidades.
        """

        return self.rect.colliderect(other.rect)

    # ======================================================
    # Helpers
    # ======================================================

    def sync_rect(self) -> None:
        """
        Sincroniza el rectángulo de colisión con
        la posición real de la entidad.
        """

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def center(self) -> tuple[int, int]:
        """
        Devuelve el centro actual de la entidad.
        """

        return self.rect.center

    def position(self) -> tuple[float, float]:
        """
        Devuelve la posición actual.
        """

        return (
            self.x,
            self.y
        )

    def size(self) -> tuple[int, int]:
        """
        Devuelve el tamaño de la entidad.
        """

        return (
            self.width,
            self.height
        )

    def set_position(
        self,
        x: float,
        y: float
    ) -> None:
        """
        Cambia la posición de la entidad.
        """

        self.x = x
        self.y = y

        self.sync_rect()

    def set_velocity(
        self,
        velocity_x: float,
        velocity_y: float
    ) -> None:
        """
        Cambia la velocidad de la entidad.
        """

        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

    # ======================================================
    # Lifecycle
    # ======================================================

    def destroy(self) -> None:
        """
        Marca la entidad como inactiva.

        Gameplay será responsable de eliminar
        posteriormente las entidades inactivas.
        """

        self.active = False
    @property
    def is_active(self) -> bool:
        """
        Indica si la entidad continúa activa.
        """

        return self.active
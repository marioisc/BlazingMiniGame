"""
==========================================================
Project : Operation Phoenix
Version : 0.1.0

Clase base para todas las escenas del videojuego.

Todas las escenas deben heredar de esta clase.

Responsabilidades
-----------------
- Procesar eventos.
- Actualizar la lógica.
- Dibujar la escena.

Las clases hijas implementarán el comportamiento
específico de cada estado del juego.
==========================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    """
    Clase base abstracta para todas las escenas.
    """

    def __init__(self, game) -> None:
        self.game = game

    # =====================================================
    # EVENTS
    # =====================================================

    @abstractmethod
    def handle_events(
        self,
        events: list[pygame.event.Event]
    ) -> None:
        """
        Procesa los eventos recibidos desde Game.
        """
        pass

    # =====================================================
    # UPDATE
    # =====================================================

    @abstractmethod
    def update(
        self,
        delta_time: float
    ) -> None:
        """
        Actualiza la lógica de la escena.
        """
        pass

    # =====================================================
    # DRAW
    # =====================================================

    @abstractmethod
    def draw(
        self,
        screen: pygame.Surface
    ) -> None:
        """
        Dibuja la escena.
        """
        pass
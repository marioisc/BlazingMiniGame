"""
==========================================================
Project : Operation Phoenix
Version : 0.1.0

Motor principal del videojuego.

Responsabilidades
-----------------
- Inicializar pygame.
- Crear la ventana principal.
- Administrar el Game Loop.
- Procesar eventos globales.
- Actualizar la escena activa.
- Dibujar la escena activa.
- Controlar el tiempo entre cuadros (Delta Time).
- Permitir el cambio de escenas.
==========================================================
"""

from __future__ import annotations

import pygame

from config import (
    FPS,
    GAME_TITLE,
    SCREEN_SIZE,
)

from scenes.menu import Menu
from scenes.scene import Scene
from scenes.gameover import GameOver

class Game:
    """
    Clase principal del videojuego.

    Coordina el funcionamiento del motor y mantiene
    la escena actualmente activa.
    """

    def __init__(self) -> None:

        # -------------------------------------------------
        # Inicialización de pygame
        # -------------------------------------------------

        pygame.init()

        # -------------------------------------------------
        # Ventana principal
        # -------------------------------------------------

        self.screen = pygame.display.set_mode(
            SCREEN_SIZE
        )

        pygame.display.set_caption(GAME_TITLE)

        # -------------------------------------------------
        # Reloj principal
        # -------------------------------------------------

        self.clock = pygame.time.Clock()

        # -------------------------------------------------
        # Estado del juego
        # -------------------------------------------------

        self.running = True

        self.delta_time = 0.0

        # -------------------------------------------------
        # Escena activa
        # -------------------------------------------------

        self.current_scene: Scene | None = None

        self.change_scene(Menu(self))

    # =====================================================
    # Scene Management
    # =====================================================

    def change_scene(self, scene: Scene) -> None:
        """
        Cambia la escena activa.
        """

        self.current_scene = scene

    # =====================================================
    # Events
    # =====================================================
    def show_game_over(self) -> None:

        self.current_scene = GameOver(self)
    
    def process_events(self) -> list[pygame.event.Event]:

        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:

                self.running = False

        return events

    # =====================================================
    # Update
    # =====================================================

    def update(self) -> None:

        if self.current_scene is not None:

            self.current_scene.update(
                self.delta_time
            )

    # =====================================================
    # Draw
    # =====================================================

    def draw(self) -> None:

        if self.current_scene is not None:

            self.current_scene.draw(
                self.screen
            )

        pygame.display.flip()

    # =====================================================
    # FPS
    # =====================================================

    def update_window_title(self) -> None:
        """
        Actualiza el título de la ventana
        mostrando los FPS actuales.
        """

        fps = self.clock.get_fps()

        pygame.display.set_caption(
            f"{GAME_TITLE} | FPS: {fps:.2f}"
        )

    # =====================================================
    # Main Loop
    # =====================================================

    def run(self) -> None:
        """
        Game Loop principal.
        """

        while self.running:

            # ---------------------------------------------
            # Delta Time
            # ---------------------------------------------

            self.delta_time = (
                self.clock.tick(FPS) / 1000.0
            )

            # ---------------------------------------------
            # Eventos
            # ---------------------------------------------

            events = self.process_events()

            if self.current_scene is not None:

                self.current_scene.handle_events(
                    events
                )

            # ---------------------------------------------
            # Lógica
            # ---------------------------------------------

            self.update()

            # ---------------------------------------------
            # Render
            # ---------------------------------------------

            self.draw()

            # ---------------------------------------------
            # FPS
            # ---------------------------------------------

            self.update_window_title()

        pygame.quit()
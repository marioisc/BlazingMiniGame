
"""
==========================================================
Project : Operation Phoenix
Version : 0.1.0

Punto de entrada del videojuego.

Responsabilidades:

- Crear la instancia principal del juego.
- Ejecutar el Game Loop.
==========================================================
"""

from game import Game


def main() -> None:
    """
    Función principal del videojuego.
    """

    game = Game()

    game.run()


if __name__ == "__main__":
    main()
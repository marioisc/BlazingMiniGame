from scenes.Scene import Scene


class GameOver(Scene):

    def __init__(self, game):
        super().__init__(game)

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, screen):

        screen.fill((60, 0, 0))
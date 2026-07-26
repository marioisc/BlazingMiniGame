class Timer:

    def __init__(self):

        self.time = 0

    def update(self, dt):

        self.time += dt

    def reset(self):

        self.time = 0
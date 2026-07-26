import os
import pygame


class AssetManager:

    def __init__(self):

        self.images = {}
        self.sounds = {}
        self.fonts = {}

    # ---------------------------------
    # IMÁGENES
    # ---------------------------------

    def load_image(self, key, path):

        if key not in self.images:

            image = pygame.image.load(path).convert_alpha()

            self.images[key] = image

        return self.images[key]

    def get_image(self, key):

        return self.images.get(key)

    # ---------------------------------
    # SONIDOS
    # ---------------------------------

    def load_sound(self, key, path):

        if key not in self.sounds:

            self.sounds[key] = pygame.mixer.Sound(path)

        return self.sounds[key]

    def get_sound(self, key):

        return self.sounds.get(key)

    # ---------------------------------
    # FUENTES
    # ---------------------------------

    def load_font(self, key, path, size):

        if key not in self.fonts:

            self.fonts[key] = pygame.font.Font(path, size)

        return self.fonts[key]

    def get_font(self, key):

        return self.fonts.get(key)
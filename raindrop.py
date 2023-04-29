import pygame
from pygame.sprite import Sprite

class Raindrop(Sprite):

    def __init__(self, zs_game, x, y):
        super().__init__()
        self.screen = zs_game.screen
        self.settings = zs_game.settings

        self.image = pygame.image.load('images/raindrop.bmp')
        self.rect = self.image.get_rect()
        self.y = y
        self.x = x - self.rect.width

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.update_y(self.settings.rain_speed)

    def update_y(self, y):
        self.y += y
        self.rect.y = self.y

    def update_x(self, x):
        self.x += x
        self.rect.x += x

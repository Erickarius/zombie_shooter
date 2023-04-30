import pygame
from pygame.sprite import Sprite

class Raindrop(Sprite):

    def __init__(self, zs_game, x, y):
        super().__init__()
        self.screen = zs_game.screen
        self.settings = zs_game.settings

        # Load the image of the raindrop and set its position
        self.image = pygame.image.load('images/raindrop.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width
        self.rect.y = y

        # Initialize the x and y positions of the raindrop
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        # Update the y position of the raindrop based on the rain speed setting
        self.y += self.settings.rain_speed
        self.rect.y = self.y

    def update_x(self, x):
        # Update the x position of the raindrop
        self.x += x
        self.rect.x += x

import pygame
from random import randint

class ZombieHand(pygame.sprite.Sprite):

    def __init__(self, zs_game):
        super().__init__()  # Initialize parent class
        self.screen = zs_game.screen
        self.settings = zs_game.settings
        self.image = pygame.image.load('images/zombie_hand.bmp')  # Load the image for the zombie hand sprite
        self.rect = self.image.get_rect()

        # Set the position of the sprite randomly on the screen
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = randint(0, self.settings.screen_height - self.rect.height)




import pygame
from random import randint

class ZombieHand(pygame.sprite.Sprite):

    def __init__(self, zs_game):
        super().__init__()
        self.screen = zs_game.screen
        self.settings = zs_game.settings
        self.image = pygame.image.load('images/zombie_hand.bmp')
        self.rect = self.image.get_rect()

        # Ustaw pozycję obrazu na losowej wysokości na ekranie
        self.rect.x = randint(0, self.settings.screen_width - self.rect.width)
        self.rect.y = randint(0, self.settings.screen_height - self.rect.height)


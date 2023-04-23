import pygame
from pygame.sprite import Sprite

class Zombie(Sprite):

	def __init__(self, soldier):
		super().__init__()
		self.screen = soldier.screen
		self.image = pygame.image.load('images/zombie.bmp')
		self.rect = self.image.get_rect()

		self.rect.x = self.rect.width
		self.rect.y - self.rect.height

		#Przechowywanie dokładnego poziomu położenia obceg.
		self.y = float(self.rect.y)
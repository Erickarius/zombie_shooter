import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	def __init__(self, soldier):
		super().__init__()
		self.screen = soldier.screen
		self.settings = soldier.settings
		self.color = self.settings.bullet_color

		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, 
			self.settings.bullet_height)
		self.rect.midright = soldier.soldier.rect.midright

		self.x = float(self.rect.x)

	def update(self):
		self.x += self.settings.bullet_speed

		self.rect.x = self.x

	def draw_bullet(self):
		pygame.draw.rect(self.screen, self.color, self.rect)
import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
	def __init__(self, zs_game):
		super().__init__() #Initialize parent class
		self.screen = zs_game.screen
		self.settings = zs_game.settings
		self.color = self.settings.bullet_color

		# Create a bullet rectangle object and set its position to the soldier's right side
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
		self.rect.midright = zs_game.soldier.rect.midright

		self.x = float(self.rect.x)

	def update(self):
	    # Update bullet position by adding the bullet speed to x position
	    self.x += self.settings.bullet_speed
	    self.rect.x = self.x

	def draw_bullet(self):
	    # Draw bullet as a rectangle with bullet color
	    pygame.draw.rect(self.screen, self.color, self.rect)
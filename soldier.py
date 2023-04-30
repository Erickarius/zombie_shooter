import pygame
from pygame.sprite import Sprite

class Soldier(Sprite):

	def __init__(self, zs_game):
		super().__init__()
		self.screen = zs_game.screen
		self.settings = zs_game.settings
		self.screen_rect = zs_game.screen.get_rect()

	    # Load the soldier image and create a rectangle object for it
		self.image = pygame.image.load('images/soldier.bmp')
		self.rect = self.image.get_rect()

	    # Set the initial position of the soldier to the mid-left of the screen
		self.rect.midleft = self.screen_rect.midleft
		self.x = float(self.rect.x)
		self.y = float(self.rect.y)

	    # Set the initial values of movement flags to False
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

	def update(self):
	    # Update the position of the soldier based on the movement flags and the soldier speed
	    if self.moving_right and self.rect.right < self.screen_rect.right:
	        self.x += self.settings.soldier_speed
	    if self.moving_left and self.rect.left > 0:
	        self.x -= self.settings.soldier_speed
	    if self.moving_up and self.rect.top > 0:
	        self.y -= self.settings.soldier_speed
	    if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
	        self.y += self.settings.soldier_speed

	    self.rect.x = self.x
	    self.rect.y = self.y

	def blitme(self):
	    # Draw the soldier image onto the screen
	    self.screen.blit(self.image, self.rect)

	def center_soldier(self):
	    # Set the soldier position to the bottom-left corner of the screen
	    self.rect.bottomleft = self.screen_rect.bottomleft
	    self.x = float(self.rect.x)
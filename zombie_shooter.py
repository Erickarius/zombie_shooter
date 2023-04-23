import sys

import pygame

from soldier import Soldier
from settings_zombie_shooter import Settings
from soldier_bullet import Bullet
from zombie import Zombie

class ZombieShooter():

	def __init__(self):
		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width,
			self.settings.screen_height))
		pygame.display.set_caption("Zombie Schooter")

		self.soldier = Soldier(self)
		self.bullets = pygame.sprite.Group()

		self.zombies = pygame.sprite.Group() 

		self._create_zombie_group()

	def run_game(self):

		while True: 
			self._check_screen()
			self.soldier.update()
			self._update_bullets()
			self._update_screen()

	def _check_screen(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)

	def _check_keydown_events(self, event):
		
		if event.key == pygame.K_d:
			self.soldier.moving_right = True
		elif event.key == pygame.K_a:
			self.soldier.moving_left = True
		elif event.key == pygame.K_w:
			self.soldier.moving_up = True
		elif event.key == pygame.K_s:
			self.soldier.moving_down = True
		elif event.key == pygame.K_ESCAPE:
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()

	def _check_keyup_events(self, event):
		
		if event.key == pygame.K_d:
			self.soldier.moving_right = False
		elif event.key == pygame.K_a:
			self.soldier.moving_left = False
		elif event.key == pygame.K_w:
			self.soldier.moving_up = False
		elif event.key == pygame.K_s:
			self.soldier.moving_down = False

	def _fire_bullet(self):
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		self.bullets.update()

		for bullet in self.bullets.copy():
			if bullet.rect.right > 1200:
				self.bullets.remove(bullet)

	def _create_zombie_group(self):

		zombie = Zombie(self)
		zombie_width, zombie_height = zombie.rect.size
		available_space_y = self.settings.screen_height - (2 * zombie_height)
		number_zombie_y = available_space_y // (2 * zombie_height)

		soldier_width = self.soldier.rect.width
		available_space_x = (self.settings.screen_width - (3 * zombie_width) 
			- soldier_width)
		number_row = available_space_x // (2 * zombie_width)

		for row_number in range(number_row):
			for zombie_number in range(number_zombie_y):
				self._create_zombie(zombie_number, row_number)

	def _create_zombie(self, zombie_number, row_number):
		zombie = Zombie(self)
		zombie_height = zombie.rect.height
		zombie.y = zombie_height + 2 * zombie_height * zombie_number
		zombie.rect.y = zombie.y
		zombie.rect.x = zombie.rect.width + 2 * zombie.rect.width * row_number
		self.zombies.add(zombie)

	def _update_screen(self):
		self.screen.fill(self.settings.bg_color)
		self.soldier.blitme()

		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		self.zombies.draw(self.screen)

		pygame.display.flip()

if __name__ == '__main__':
	soldier = ZombieShooter()
	soldier.run_game()
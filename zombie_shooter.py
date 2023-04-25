import sys

import pygame

import random

import math

from soldier import Soldier
from settings_zombie_shooter import Settings
from soldier_bullet import Bullet
from zombie import Zombie
from zombie_hand import ZombieHand

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
		self.zombiehands = pygame.sprite.Group()

		self._create_zombie_group()
		self._create_zombiehand_group()

	def run_game(self):
		while True: 
			self._check_screen()
			self.soldier.update()
			self._update_bullets()
			self._update_zombies()
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
		self._check_group_edges()
		self.bullets.update()

		for bullet in self.bullets.copy():
			if bullet.rect.right > 1200:
				self.bullets.remove(bullet)

	def _update_zombies(self):
		self.zombies.update()

	def _create_zombie_group(self):
		scr_w = self.settings.screen_width
		scr_h = self.settings.screen_height
		clear_area_x = self.settings.clear_area_x
		clear_area_y = self.settings.clear_area_y
		zombies_in_row = self.settings.zombies_in_row
		zombies_in_column = self.settings.zombies_in_column
		for x_pos in range(self.settings.screen_width, clear_area_x, -math.ceil(
			(scr_w - clear_area_x)/zombies_in_row)):
			for y_pos in range(0, self.settings.screen_height - clear_area_y, 
				math.ceil((scr_h - clear_area_y )/zombies_in_column)):
				self._create_zombie(x_pos, y_pos)


	def _create_zombie(self, x, y):
		zombie = Zombie(self, x, y)
		self.zombies.add(zombie)

	def _check_group_edges(self):
		for zombie in self.zombies.sprites():
			if zombie.check_edges():
				self._change_group_direction()
				break

	def _change_group_direction(self):
		for zombie in self.zombies.sprites():
			zombie.update_x(-self.settings.zombies_drop_speed)
		self.settings.zombies_direction *= -1

	def _create_zombiehand_group(self):
	    for i in range(10):
	        zombiehand = ZombieHand(self)
	        zombiehand_width, zombiehand_height = zombiehand.rect.size
	        
	        while True:
	            zombiehand.x = random.randint(zombiehand_width, 
	                self.settings.screen_width - zombiehand_width)
	            zombiehand.rect.x = zombiehand.x
	            zombiehand.rect.y = random.randint(zombiehand_height, 
	                self.settings.screen_height - zombiehand_height)
	                
	            # Sprawdź, czy nowo wylosowana pozycja koliduje z innym obiektem
	            if not pygame.sprite.spritecollide(zombiehand, self.zombies, False) and not pygame.sprite.spritecollide(zombiehand, self.zombiehands, False):
	                break
	                
	        self.zombiehands.add(zombiehand)


	def _update_screen(self):
		self.screen.fill(self.settings.bg_color)
		self.zombiehands.draw(self.screen)
		self.zombies.draw(self.screen)
		self.soldier.blitme()

		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		pygame.display.flip()

if __name__ == '__main__':
	zs = ZombieShooter()
	zs.run_game()
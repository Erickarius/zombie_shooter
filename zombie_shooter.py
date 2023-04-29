import sys
from time import sleep

import pygame

import random


from settings  import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from soldier import Soldier
from bullet import Bullet
from zombie import Zombie
from zombie_hand import ZombieHand
from raindrop import Raindrop
from sound import Sound

class ZombieShooter():

	def __init__(self):
		pygame.init()

		self.settings = Settings()

		self.screen = pygame.display.set_mode((self.settings.screen_width,
			self.settings.screen_height))
		pygame.display.set_caption("Zombie Schooter")

		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		self.soldier = Soldier(self)
		self.bullets = pygame.sprite.Group()
		self.rain = pygame.sprite.Group()
		self.sound = Sound()

		self.zombies = pygame.sprite.Group() 
		self.zombiehands = pygame.sprite.Group() 

		self._create_zombie_group()
		self._create_zombiehand_group()
		self._create_rain()
		self.button = Button(self, self.screen, msg="Start", msg2 = "Controls")
	

	def run_game(self):
		while True: 
			self._check_events()

			if self.stats.game_active:
				self._rain_update()
				self.soldier.update()
				self._update_bullets()
				self._update_zombies()

			self._update_screen()

	def _check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.stats.save_high_score()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
			elif event.type == pygame.KEYUP:
				self._check_keyup_events(event)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_button(mouse_pos)

	def _start_game(self):
	    if not self.stats.game_active:
	        self._reset_game()
	        self.stats.game_active = True
	        pygame.mouse.set_visible(False)

	def _check_button(self, mouse_pos):
	    if self.button.rect.collidepoint(mouse_pos):
	        self._start_game()
	    elif self.button.rect2.collidepoint(mouse_pos):
	    	self.button.show_control()

	def _reset_game(self):
	    self.settings.initalize_dynamic_settings()
	    self.stats.reset_stats()
	    self.sb.prep_score()
	    self.sb.prep_level()
	    self.sb.prep_soldiers()

	    self.zombies.empty()
	    self.bullets.empty()

	    self._create_zombie_group()
	    self.soldier.center_soldier()


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
			self.stats.save_high_score()
			sys.exit()
		elif event.key == pygame.K_SPACE:
			self.sound.shot.play() 
			self._fire_bullet()
		elif event.key == pygame.K_g:
			self._start_game()

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

		self._check_bullet_zombie_collisions()

	def _check_bullet_zombie_collisions(self):

		collisions = pygame.sprite.groupcollide(self.bullets, self.zombies, 
			True, True)
		if collisions:
			for zombies in collisions.values():
				self.stats.score += self.settings.zombie_points * len(zombies)
			self.sound.zombie_dead.play() 
			self.sb.prep_score()
			self.sb.check_high_score()

		if not self.zombies:
			self.bullets.empty()
			self._create_zombie_group()
			self.settings.increase_speed()

			self.stats.level += 1
			self.sb.prep_level()

	def _update_zombies(self):
		self.zombies.update()

		if pygame.sprite.spritecollideany(self.soldier, self.zombies):
			self._soldier_hit()

		self._check_zombies_left()
	
	def _soldier_hit(self):
		if self.stats.soldier_left > 0:
			self.stats.soldier_left -= 1
			self.sound.soldier_dead.play()
			self.sb.prep_soldiers()
			self.zombies.empty()
			self.bullets.empty()
			self._create_zombie_group()
			self.soldier.center_soldier()
			sleep(0.5)
		else:
			self.stats.game_active = False
			pygame.mouse.set_visible(True)

	def _check_zombies_left(self):
		screen_rect = self.screen.get_rect()
		for zombie in self.zombies.sprites():
			if zombie.rect.left <= screen_rect.left:
				self._soldier_hit()
				break

	def _create_zombie_group(self):
		scr_w, scr_h = self.settings.screen_width, self.settings.screen_height
		clear_area_x, clear_area_y = self.settings.clear_area_x, self.settings.clear_area_y
		zombies_in_row, zombies_in_column = self.settings.zombies_in_row, self.settings.zombies_in_column

		for x_pos in range(scr_w, clear_area_x, -(
			(scr_w - clear_area_x) // zombies_in_row)):
		    
		    for y_pos in range(0, scr_h - clear_area_y, 
		    	(scr_h - clear_area_y) // zombies_in_column):
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
		for _ in range(10):
			zombiehand = ZombieHand(self)
			zombiehand_width, zombiehand_height = zombiehand.rect.size

			while True:
			    zombiehand.x = random.randint(zombiehand_width, 
			    	self.settings.screen_width - zombiehand_width)
			    zombiehand.rect.x, zombiehand.rect.y = zombiehand.x, random.randint(
			    	zombiehand_height, self.settings.screen_height - zombiehand_height)
			    if not pygame.sprite.spritecollide(zombiehand, self.zombies, 
			    	False) and not pygame.sprite.spritecollide(zombiehand, self.zombiehands, False):
			        break
			        
			self.zombiehands.add(zombiehand)

	def _create_rain(self):
	    scr_w, scr_h = self.settings.screen_width, self.settings.screen_height
	    clear_rain_area_x, clear_rain_area_y = self.settings.clear_rain_area_x, self.settings.clear_rain_area_y
	    raindrop_in_row, raindrop_in_column = self.settings.raindrop_in_row, self.settings.raindrop_in_column

	    for x_pos in range(scr_w, clear_rain_area_x, -(
	        (scr_w - clear_rain_area_x) // raindrop_in_row)):

	        for y_pos in range(0, scr_h - clear_rain_area_y,
	            (scr_h - clear_rain_area_y) // raindrop_in_column):
	            self._create_raindrop(x_pos, y_pos)


	def _create_raindrop(self, x, y):
	    raindrop = Raindrop(self, x, y)
	    self.rain.add(raindrop)

	def _rain_update(self):
		self.rain.update()

		for raindrop in self.rain.copy():
			if raindrop.rect.bottom >= self.settings.screen_height:
				self.rain.remove(raindrop)

		if len(self.rain) == 0:
			self._create_rain()

	def _update_screen(self):
		self.screen.fill(self.settings.bg_color)
		self.rain.draw(self.screen)
		self.zombiehands.draw(self.screen)
		self.zombies.draw(self.screen)
		self.soldier.blitme()

		self.sb.show_score()

		if not self.stats.game_active:
			self.button.draw_button()
			self.button.draw_button2()

		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		pygame.display.flip()

if __name__ == '__main__':
	zs = ZombieShooter()
	zs.run_game()
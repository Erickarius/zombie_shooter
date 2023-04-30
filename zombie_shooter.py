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
	    # Initialize pygame
	    pygame.init()

	    # Create an instance of the Settings class
	    self.settings = Settings()

	    # Set up the screen
	    self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
	    pygame.display.set_caption("Zombie Schooter")

	    # Create instances of GameStats and Scoreboard
	    self.stats = GameStats(self)
	    self.sb = Scoreboard(self)

	    # Create instances of Soldier, Bullet, Raindrop and Sound
	    self.soldier = Soldier(self)
	    self.bullets = pygame.sprite.Group()
	    self.rain = pygame.sprite.Group()
	    self.sound = Sound()

	    # Create sprite groups for zombies and zombie hands
	    self.zombies = pygame.sprite.Group()
	    self.zombiehands = pygame.sprite.Group()

	    # Call the functions to create zombie groups, zombie hand groups, and rain
	    self._create_zombie_group()
	    self._create_zombiehand_group()
	    self._create_rain()
	    self.button = Button(self, self.screen, msg="Start", msg2 = "Controls")
	    

	def run_game(self):
	    """Main game loop"""
	    while True:
	        self._check_events()

	        if self.stats.game_active:
	            self._rain_update()
	            self.soldier.update()
	            self._update_bullets()
	            self._update_zombies()

	        self._update_screen()

	def _check_events(self):
	    """Check and respond to events"""
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
	    """Starts the game"""
	    if not self.stats.game_active:
	        self._reset_game()
	        self.stats.game_active = True
	        pygame.mouse.set_visible(False)

	def _check_button(self, mouse_pos):
	    """Checks if buttons are pressed"""
	    if self.button.rect.collidepoint(mouse_pos):
	        self._start_game()
	    elif self.button.rect2.collidepoint(mouse_pos):
	        self.button.show_control()

	def _reset_game(self):
	    """Resets the game when game over"""
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
	    """Check key down events"""
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
		"""Respond to key releases."""
		if event.key == pygame.K_d:
			self.soldier.moving_right = False
		elif event.key == pygame.K_a:
			self.soldier.moving_left = False
		elif event.key == pygame.K_w:
			self.soldier.moving_up = False
		elif event.key == pygame.K_s:
			self.soldier.moving_down = False

	def _fire_bullet(self):
		"""Fire a bullet if limit not reached yet."""
		if len(self.bullets) < self.settings.bullets_allowed:
			new_bullet = Bullet(self)
			self.bullets.add(new_bullet)

	def _update_bullets(self):
		"""Update position of bullets and get rid of old bullets."""
		self._check_group_edges()
		self.bullets.update()

		for bullet in self.bullets.copy():
			if bullet.rect.right > 1200:
				self.bullets.remove(bullet)

		self._check_bullet_zombie_collisions()

	def _check_bullet_zombie_collisions(self):
		"""Respond to bullet-zombie collisions."""
		collisions = pygame.sprite.groupcollide(self.bullets, self.zombies, True, True)
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
		"""Update the positions of all zombies in the group."""
		self.zombies.update()

		if pygame.sprite.spritecollideany(self.soldier, self.zombies):
			self._soldier_hit()

		self._check_zombies_left()

	def _soldier_hit(self):
		"""Respond to the soldier being hit by a zombie."""
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
		# Get the rectangular area of the screen
		screen_rect = self.screen.get_rect()
		
		# Check if any zombie has reached the left edge of the screen
		for zombie in self.zombies.sprites():
			if zombie.rect.left <= screen_rect.left:
				# Reduce the number of remaining soldiers if a zombie has reached the left edge
				self._soldier_hit()
				break

	def _create_zombie_group(self):
		# Get the screen width and height and the size of the clear area where zombies won't spawn
		scr_w, scr_h = self.settings.screen_width, self.settings.screen_height
		clear_area_x, clear_area_y = self.settings.clear_area_x, self.settings.clear_area_y
		zombies_in_row, zombies_in_column = self.settings.zombies_in_row, self.settings.zombies_in_column

		# Spawn zombies on the right side of the screen with a fixed gap between them
		for x_pos in range(scr_w, clear_area_x, -((scr_w - clear_area_x) // zombies_in_row)):
		    for y_pos in range(0, scr_h - clear_area_y, (scr_h - clear_area_y) // zombies_in_column):
		        self._create_zombie(x_pos, y_pos)

	def _create_zombie(self, x, y):
		# Create a new zombie and add it to the zombies group
		zombie = Zombie(self, x, y)
		self.zombies.add(zombie)

	def _check_group_edges(self):
		# Check if any zombie in the group has reached the edges of the screen
		for zombie in self.zombies.sprites():
			if zombie.check_edges():
				# Change the direction of the zombies' movement if they've reached the edges
				self._change_group_direction()
				break

	def _change_group_direction(self):
		# Reverse the direction of the zombies' movement and move them down
		for zombie in self.zombies.sprites():
			zombie.update_x(-self.settings.zombies_drop_speed)
		self.settings.zombies_direction *= -1

	def _create_zombiehand_group(self):
		# Create a group of zombie hands
		for _ in range(10):
			# Create a new zombie hand and position it randomly on the screen
			zombiehand = ZombieHand(self)
			zombiehand_width, zombiehand_height = zombiehand.rect.size

			# Keep finding a new position for the zombie hand until it doesn't overlap with any zombie or zombie hand
			while True:
			    zombiehand.x = random.randint(zombiehand_width, 
			    	self.settings.screen_width - zombiehand_width)
			    zombiehand.rect.x, zombiehand.rect.y = zombiehand.x, random.randint(zombiehand_height, 
			    	self.settings.screen_height - zombiehand_height)
			    if not pygame.sprite.spritecollide(zombiehand, self.zombies, 
			    	False) and not pygame.sprite.spritecollide(zombiehand, self.zombiehands, False):
			        break
			        
			# Add the new zombie hand to the zombie hands group
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


	def _create_rain(self):
	    # Unpack settings
	    scr_w, scr_h = self.settings.screen_width, self.settings.screen_height
	    clear_rain_area_x, clear_rain_area_y = self.settings.clear_rain_area_x, self.settings.clear_rain_area_y
	    raindrop_in_row, raindrop_in_column = self.settings.raindrop_in_row, self.settings.raindrop_in_column

	    # Create raindrops in a grid pattern
	    for x_pos in range(scr_w, clear_rain_area_x, -((scr_w - clear_rain_area_x) // raindrop_in_row)):
	        for y_pos in range(0, scr_h - clear_rain_area_y, (scr_h - clear_rain_area_y) // raindrop_in_column):
	            self._create_raindrop(x_pos, y_pos)


	def _create_raindrop(self, x, y):
	    # Create a new raindrop at the given position
	    raindrop = Raindrop(self, x, y)
	    self.rain.add(raindrop)


	def _rain_update(self):
	    # Update all raindrops
	    self.rain.update()

	    # Remove raindrops that have fallen off the bottom of the screen
	    for raindrop in self.rain.copy():
	        if raindrop.rect.bottom >= self.settings.screen_height:
	            self.rain.remove(raindrop)

	    # If there are no raindrops left, create a new batch
	    if len(self.rain) == 0:
	        self._create_rain()


	def _update_screen(self):
	    # Redraw the screen
	    self.screen.fill(self.settings.bg_color)

	    # Draw all raindrops
	    self.rain.draw(self.screen)

	    # Draw other game elements
	    self.zombiehands.draw(self.screen)
	    self.zombies.draw(self.screen)
	    self.soldier.blitme()
	    self.sb.show_score()

	    # If the game is not active, draw the start button
	    if not self.stats.game_active:
	        self.button.draw_button()
	        self.button.draw_button2()

	    # Draw all bullets
	    for bullet in self.bullets.sprites():
	        bullet.draw_bullet()

	    # Update the display
	    pygame.display.flip()


if __name__ == '__main__':
    # Create a new instance of the game and run it
    zs = ZombieShooter()
    zs.run_game()

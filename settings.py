class Settings:
	def __init__(self):
		#Screen settings
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (0, 153, 0)
		
		#Soldier settings
		self.soldier_limit = 3

		#Bullet settings
		self.bullet_width = 15
		self.bullet_height = 3
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 5

		#Zombie settings
		self.zombies_in_row = 6
		self.zombies_in_column = 5
		self.clear_area_x = 400
		self.clear_area_y = 100
		self.zombies_drop_speed = 10

		#Easy game speed change
		self.speedup_scale = 1.1

		#Easy game point change
		self.score_scale = 1.5

		self.initalize_dynamic_settings()

	def initalize_dynamic_settings(self):
		#Initialization setting that change when the game is active.

		self.soldier_speed = 1.5
		self.bullet_speed = 3.0
		self.zombie_speed = 1.0

		self.zombies_direction = 1

		self.zombie_points = 50

	def increase_speed(self):
		self.soldier_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.zombie_speed *= self.speedup_scale

		self.zombie_points = int(self.zombie_points * self.score_scale)
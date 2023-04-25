class Settings:
	def __init__(self):
		
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (0, 153, 0)
		self.soldier_speed = 1.6

		self.bullet_speed = 1.0
		self.bullet_width = 15
		self.bullet_height = 3
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 5

		self.zombies_in_row = 6
		self.zombies_in_column = 4
		self.clear_area_x = 400
		self.clear_area_y = 100
		self.zombie_speed = 1
		self.zombies_drop_speed = 10
		self.zombies_direction = 1
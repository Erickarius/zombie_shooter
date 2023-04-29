import pygame

class Sound():

	def __init__(self):
		self.shot = pygame.mixer.Sound("sounds/shot.mp3")
		self.zombie_dead = pygame.mixer.Sound("sounds/zombie_dead.mp3")
		self.soldier_dead = pygame.mixer.Sound("sounds/soldier_dead.mp3")
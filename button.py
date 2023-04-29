import pygame.font
from time import sleep

class Button():

	def __init__(self, zs_game, screen, msg, msg2):

		self.screen = zs_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = zs_game.settings


		self.width, self.height = 200, 50
		self.button_color = (0, 0, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		self.rect2 = pygame.Rect(0, 0, self.width, self.height)
		self.rect2.centerx = self.screen_rect.centerx
		self.rect2.top = self.rect.bottom + 10


		self._prep_msg(msg)
		self._prep_msg2(msg2)

	def _prep_msg(self, msg):

		self.msg_image = self.font.render(msg, True, self.text_color,
			self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
	
	def _prep_msg2(self, msg):

		self.msg2_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg2_image_rect = self.msg2_image.get_rect()
		self.msg2_image_rect.center = self.rect2.center

	def show_control(self):
	    self.screen.fill(self.settings.bg_color)
	    font = pygame.font.SysFont(None, 60)
	    text = font.render("", True, (255, 255, 255), self.settings.bg_color)
	    text_rect = text.get_rect()
	    text_rect.center = self.screen.get_rect().center
	    self.screen.blit(text, text_rect)

	    font = pygame.font.SysFont(None, 40)
	    texts = [
	        ("Move: WASD", self.screen.get_rect().centery - 60),
	        ("Shoot: SPACE", self.screen.get_rect().centery),
	        ("Start Game: G", self.screen.get_rect().centery + 60)
	    ]
	    for message, y in texts:
	        text = font.render(message, True, (255, 255, 255), self.settings.bg_color)
	        text_rect = text.get_rect()
	        text_rect.center = (self.screen.get_rect().centerx, y)
	        self.screen.blit(text, text_rect)

	    pygame.display.flip()

	    while True:
	        for event in pygame.event.get():
	            if event.type == pygame.MOUSEBUTTONUP:
	                self.draw_button()
	                sleep(5)
	                return



	def draw_button(self):
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)

	def draw_button2(self):
		self.screen.fill(self.button_color, self.rect2)
		self.screen.blit(self.msg2_image, self.msg2_image_rect)
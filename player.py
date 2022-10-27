import pygame 
from load_file import * 
from setting import *

class Player(pygame.sprite.Sprite):
	def __init__(self,pos):
		super().__init__()
		self.animation_speed = 0.15 # fast or slow -> slow motion
		self.image = pygame.transform.scale(load_image('ball.png'), (24,24))
		self.rect = self.image.get_rect(topleft = pos)

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0 #0.8

	def normalize(self):
		if self.direction.x != 0 and self.direction.y != 0:
			ss = (self.direction.x ** 2 + self.direction.y ** 2) ** 0.5
			self.direction.x = self.direction.x / ss
			self.direction.y = self.direction.y / ss
		

	def get_pos(self):
		return self.pos

	def move(self):
		self.rect.x += self.direction.x * self.speed
		self.rect.y += self.direction.y * self.speed

	def get_input(self):
		mouse_down = pygame.mouse.get_pressed()[0]
		if mouse_down: #get the mouse position and change direction
			mouse_pos = pygame.mouse.get_pos()
			print(mouse_pos)
			cenx = self.rect.centerx
			ceny = self.rect.centery

			self.direction.x = mouse_pos[0] - cenx
			self.direction.y = mouse_pos[1] - ceny
			self.normalize()


	def apply_gravity(self):
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

	def update(self):
		self.get_input()
		self.move()
	
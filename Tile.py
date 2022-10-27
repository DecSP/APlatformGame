import pygame 
from load_file import *

# Shake screen
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size,img_path):
		super().__init__()
		self.image = pygame.transform.scale(load_image(img_path), (size, size))
		self.rect = self.image.get_rect(topleft = pos)

	def update(self,x_shift,y_shift):
		self.rect.x += x_shift
		self.rect.y += y_shift
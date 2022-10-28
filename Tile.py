import pygame 
from load_file import *

# Shake screen
class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size,img_path,game):
		super().__init__()
		self.image = pygame.transform.scale(load_image(img_path), (size, size))
		self.rect = self.image.get_rect(topleft = pos)
		self.game=game
	
	def update(self,*args):
		pass
import pygame 
from Tile import *

# Shake screen
class Wall(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'wall.png',game)
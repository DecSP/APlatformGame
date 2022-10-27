import pygame 
from Tile import *

# Shake screen
class Wall(Tile):
	def __init__(self,pos,size):
		super().__init__(pos,size,'wall.png')
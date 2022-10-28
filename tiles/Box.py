import pygame 
from Tile import *

class Box(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'box.png',game)


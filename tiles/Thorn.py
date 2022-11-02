import pygame 
from Tile import *

class Thorn(Tile):
	def __init__(self,pos,size,game,wall_type: str):
		if wall_type == 'U':
			super().__init__(pos,size,'triangle-up.png',game)
		elif wall_type == 'L':
			super().__init__(pos,size,'triangle-left.png',game)
		elif wall_type == 'R':
			super().__init__(pos,size,'triangle-right.png',game)
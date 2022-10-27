import pygame 
from Tile import *

class Thorn(Tile):
	def __init__(self,pos,size,wall_type: str):
		if wall_type == 'U':
			super().__init__(pos,size,'triangle-up.png')
		elif wall_type == 'L':
			super().__init__(pos,size,'triangle-left.png')
		elif wall_type == 'R':
			super().__init__(pos,size,'triangle-right.png')
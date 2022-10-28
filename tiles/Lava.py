import pygame 
from Tile import *

class Lava(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'lava.png',game)

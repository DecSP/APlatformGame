import pygame 
from Tile import *

class Lava(Tile):
	def __init__(self,pos,size):
		super().__init__(pos,size,'lava.png')

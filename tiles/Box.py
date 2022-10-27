import pygame 
from Tile import *

class Box(Tile):
	def __init__(self,pos,size):
		super().__init__(pos,size,'box.png')


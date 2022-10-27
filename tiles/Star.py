import pygame 
from Tile import *

class Star(Tile):
	def __init__(self,pos,size):
		super().__init__(pos,size,'star.png')
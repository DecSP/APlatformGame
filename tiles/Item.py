from Tile import *
from setting import *

class Star(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'star.png',game)
class Potion(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'potion.png',game)

class Box(Tile):
	def __init__(self,pos,game):
		super().__init__(pos,tile_size,'box.png',game)

class MedKit(Tile):
	def __init__(self,pos,game):
		super().__init__(pos,item_size,'medkit.png',game)

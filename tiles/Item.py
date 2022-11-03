from Tile import *

class Star(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'star.png',game)

class Box(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'box.png',game)

class MedKit(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'medkit.png',game)

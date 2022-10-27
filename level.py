from re import L
import pygame 
from tiles.Lava import Lava 
from tiles.Thorn import Thorn
from tiles.Box import Box
from tiles.Wall import Wall
from tiles.Star import Star
from setting import *
from player import Player

class Level:
	def __init__(self,level_data,surface):
		
		# level setup
		self.level_data = level_data
		self.display_surface = surface 
		self.tiles = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.thorn_left = pygame.sprite.GroupSingle()
		self.thorn_right = pygame.sprite.GroupSingle()
		self.thorn_up = pygame.sprite.GroupSingle()
		self.lava_down = pygame.sprite.GroupSingle()
		self.setup_level(level_data)
		self.world_shift_left = 0
		self.world_shift_right = 0
		self.current_x = 0
		self.player_on_ground = False


	def setup_level(self,layout): #layout: List[List[str]]
		# Init Player: (1152, 512)
		player_pos = (1152, 512)
		
		offset_x = (player_pos[0] + tile_size/2 - screen_width / 2)
		# offset_y = (player_pos[1] + tile_size/2  - screen_height / 2)
		offset_y = 0

		player_sprite = Player((screen_width/2 - tile_size/2, screen_height/2 - tile_size/2))
		self.player.add(player_sprite)
		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size - offset_x
				y = row_index * tile_size - offset_y
				
				if cell == 'X':
					lava = Lava((x,y),tile_size)
					self.tiles.add(lava)
					self.lava_down.add(lava)
				# if cell == 'P':
				# 	print((x,y))
				# 	player_sprite = Player((x,y))
				# 	self.player.add(player_sprite)

				if cell == 'U':
					thorn = Thorn((x,y),tile_size,cell)
					self.tiles.add(thorn)
					self.thorn_up.add(thorn)
				if cell == 'R':
					thorn = Thorn((x,y),tile_size,cell)
					self.tiles.add(thorn)
					self.thorn_right.add(thorn)
				if cell == 'L':
					thorn = Thorn((x,y),tile_size,cell)
					self.tiles.add(thorn)
					self.thorn_left.add(thorn)

				if cell == 'W':
					brick = Wall((x,y),tile_size)
					self.tiles.add(brick)
				if cell == 'S':
					star = Star((x,y),item_size)
					self.tiles.add(star)
				if cell == 'B':
					box = Box((x,y),item_size)
					self.tiles.add(box)


	def scroll_x(self):
		player = self.player.sprite
		player_x = player.rect.centerx
		direction_x = player.direction.x
		thorn_left = self.thorn_left.sprite.rect.topleft[0]
		thorn_right = self.thorn_right.sprite.rect.topright[0]
		# print(thorn_right)
		if player_x < screen_width / 3 and direction_x < 0 and thorn_left < 0:
			self.world_shift_left = screen_width / 3 - player_x
			player.speed = 0
		elif player_x > screen_width - (screen_width / 3) and direction_x > 0 and thorn_right > screen_width:
			self.world_shift_left = screen_width - (screen_width / 3) - player_x
			player.speed = 0
		else:
			self.world_shift_left = 0
			player.speed = 8

	def collide(self):
		player = self.player.sprite
		for sprite in self.tiles.sprites():
			if sprite.rect.colliderect(player.rect):
				if isinstance(sprite,Star):
					print("Hello WOrld")
					sprite.kill()
				if isinstance(sprite,Lava) or isinstance(sprite,Thorn):
					return -1
				if isinstance(sprite,Box):
					print("Box")
					# player.collide_box(sprite)
					# sprite.kill()


	def run(self):
		# level tiles
		self.scroll_x()
		if self.collide() == -1:
			self.__init__(self.level_data,self.display_surface)
			return -1
		
		# player
		self.player.update()
		self.player.draw(self.display_surface)
		self.tiles.update(self.world_shift_left, self.world_shift_right)
		self.tiles.draw(self.display_surface)

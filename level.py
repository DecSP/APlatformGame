import sys
import pygame 
from tiles.Box import Box
from tiles.Wall import Wall
from tiles.Star import Star
from tiles.Lava import Lava
from setting import *
from player import PMoves, Player

class Level:
	def __init__(self,level_data,surface):
		
		# level setup
		self.level_data = level_data
		self.display_surface = surface 
		self.player = pygame.sprite.GroupSingle()
		self.tiles = pygame.sprite.Group()
		self.bullets = []

		self.playermoves = PMoves()
		self.setup_level(level_data)
		self.health_bar = HealthBar([14, 5], 300, 20, [0, 200, 0])
		self.game_over=False
		
		self.aim_fly = False

	def setup_level(self,layout):
		player_pos = (1152, 512)
		offset_x = (player_pos[0] + tile_size/2 - screen_width / 2)
		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size - offset_x
				y = row_index * tile_size
				
				if cell == 'P':
					player_sprite = Player((x,y),self)
					self.player.add(player_sprite)
				if cell == 'X':
					lava = Lava((x,y),tile_size,self)
					self.tiles.add(lava)
				if cell == 'W':
					brick = Wall((x,y),tile_size,self)
					self.tiles.add(brick)
				if cell == 'S':
					star = Star((x,y),item_size,self)
					self.tiles.add(star)
				if cell == 'B':
					box = Box((x,y),item_size,self)
					self.tiles.add(box)


	def scroll_world(self):
		player = self.player.sprite
		px,py = player.rect.centerx, player.rect.centery
		scroll = [0, 0]
		scroll[0] += (
			px - self.display_surface.get_width() / 2
		) / 20
		scroll[1] += (
			py - self.display_surface.get_height() / 2
		) / 20
		scroll[0] = int(scroll[0])
		scroll[1] = int(scroll[1])

		player.scroll(scroll)
		for sprites in self.tiles:
			sprites.rect.center -= vec(scroll)
		for sprites in self.bullets:
			sprites.pos -= vec(scroll)

	def process(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				self.playermoves.flyToMouse = True
		if self.game_over:
			return
		# slomo and fly 
		if pygame.mouse.get_pressed()[0]:
			self.aim_fly=True
		else:
			self.aim_fly=False

		self.scroll_world()

	def update(self,delta):
		if self.aim_fly:
			delta = delta * SLOMO_SPEED

		# player
		if not self.game_over:
			self.player.update(delta,self.playermoves)
			self.player.draw(self.display_surface)

		# world object
		self.tiles.update(delta)
		self.tiles.draw(self.display_surface)
		for bullet in self.bullets:
			bullet.update(delta)
			bullet.draw(self.display_surface)

		if self.game_over:
			return

		# aim
		if self.aim_fly:
			player = self.player.sprite
			px,py = player.rect.centerx, player.rect.centery
			pygame.draw.line(self.display_surface,(255,255,255),(px,py),pygame.mouse.get_pos())
			self.player.sprite.reduceLife(100*delta)
		self.health_bar.update(self.display_surface,self.player.sprite.life)

class HealthBar:
    def __init__(
        self, pos, width, height, h_color=(205, 22, 22), o_color=(0, 0, 0), o_width=1
    ):
        self.pos = vec(pos)
        self.width = width
        self.init_width = width
        self.height = height
        self.h_color = h_color
        self.o_color = o_color
        self.o_width = o_width

    def update(self, surface, percent):
        pygame.draw.rect(
            surface, (0, 0, 0), pygame.Rect(self.pos, (self.init_width, self.height))
        )
        pygame.draw.rect(
            surface, self.h_color, pygame.Rect(self.pos, (self.init_width*percent/100, self.height))
        )
        pygame.draw.rect(
            surface,
            self.o_color,
            pygame.Rect(self.pos, (self.init_width, self.height)),
            self.o_width,
        )


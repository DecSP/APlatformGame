from random import randint
import sys
import pygame 
from tiles.Box import Box
from tiles.Wall import Wall
from tiles.Star import Star
from tiles.Lava import Lava
from setting import *
from player import PMoves, Player
from sprites import HealthBar

class Level:
	def __init__(self,level_data,surface):
		
		# level setup
		self.level_data = level_data
		self.display_surface = surface 
		self.player = pygame.sprite.GroupSingle()
		self.tiles = pygame.sprite.Group()
		self.bullets = []
		self.particles = []

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
		
		self.bg_rects=[]
		factor = 0.25
		for i in range(3):
			for _ in range(int(tile_size*len(layout[0]) / 80)):
				self.bg_rects.append(
					[
						factor,
						[
							vec(randint(0, tile_size*len(layout[0])), randint(50, 150)),
							vec(randint(20, 50), 300),
						],
					]
				)
			factor += 0.25


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
		for sprites in self.particles:
			sprites.pos -= vec(scroll)
		for rect in self.bg_rects:
			rect[1][0] -= vec(scroll) * rect[0]

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
		for particle in self.particles:
			particle.update(delta, self.display_surface)
			if particle.killed:
				self.particles.remove(particle)
		if self.game_over:
			return

		# aim
		if self.aim_fly:
			player = self.player.sprite
			px,py = player.rect.centerx, player.rect.centery
			pygame.draw.line(self.display_surface,(255,255,255),(px,py),pygame.mouse.get_pos())
			self.player.sprite.reduceLife(40*delta)
		self.health_bar.update(self.display_surface,self.player.sprite.life)
	
	def draw_bg(self):
		self.display_surface.fill((125, 18, 67))
		for rect in self.bg_rects:
			color = (85, 0, 35) if rect[0] == 0.75 else (99, 5, 47)
			if rect[0] == 0.25:
				color = (110, 16, 54)
			pygame.draw.rect(self.display_surface, color, pygame.Rect(rect[1][0], rect[1][1]))



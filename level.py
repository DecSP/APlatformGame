from random import randint
import sys
import pygame
from load_file import load_image 
from tiles.Item import Box,Star
from tiles.Wall import Wall
from tiles.Enemy import Bird
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
		self.playerColliders = pygame.sprite.Group()
		self.playerGathers = pygame.sprite.Group()
		self.bullets = []
		self.particles = []

		self.world_shift = [0,0]
		self.setup_level(level_data)

		self.playermoves = PMoves()
		self.health_bar = HealthBar(self.player.sprite,[14, 5], 300, 20, [0, 200, 0])
		self.game_over=False
		
		self.aim_fly = False

	def setup_level(self,layout):
		player_pos = (1152, 512)
		offset_x = (player_pos[0] + tile_size/2 - screen_width / 2)
		self.world_shift[0]=offset_x
		self.world_size = [len(layout[0])*tile_size,len(layout)*tile_size]
		for row_index,row in enumerate(layout):
			for col_index,cell in enumerate(row):
				x = col_index * tile_size - offset_x
				y = row_index * tile_size
				
				if cell == 'P':
					player_sprite = Player((x,y),self)
					self.player.add(player_sprite)
				elif cell == 'X':
					lava = Lava((x,y),tile_size,self)
					self.tiles.add(lava)
					self.playerColliders.add(lava)
				elif cell == 'W':
					brick = Wall((x,y),tile_size,self)
					self.tiles.add(brick)
					self.playerColliders.add(brick)
				elif cell == 'E':
					bird = Bird((x,y),self)
					self.tiles.add(bird)
					self.playerColliders.add(bird)
				elif cell == 'S':
					star = Star((x,y),item_size,self)
					self.tiles.add(star)
					self.playerGathers.add(star)
				elif cell == 'B':
					box = Box((x,y),item_size,self)
					self.tiles.add(box)
					self.playerGathers.add(box)
		
		self.bg_rects=[]
		factor = 1/4
		for i in range(4,0,-1):
			bgimg = load_image("bg/%s.png"%(str(i).zfill(2)))
			scale = self.world_size[1]/ bgimg.get_height()
			bgimg = pygame.transform.scale(bgimg,(scale*bgimg.get_width(),scale*bgimg.get_height()))

			for j in range((self.world_size[0]+bgimg.get_width()-1)//(bgimg.get_width())):
				self.bg_rects.append(
					[
						factor,
						[
							bgimg,
							vec([j*bgimg.get_width()-offset_x,0]),
						],
					]
				)
				
			factor += 1/4


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
		if self.world_shift[0]+scroll[0]<0 or self.world_shift[0]+scroll[0]+self.display_surface.get_width()>self.world_size[0] :
			scroll[0]=0
		if self.world_shift[1]+scroll[1]<0 or self.world_shift[1]+scroll[1]+self.display_surface.get_height()>self.world_size[1] :
			scroll[1]=0
		
		self.world_shift[0]+=scroll[0]
		self.world_shift[1]+=scroll[1]

		player.scroll(scroll)
		for sprites in self.tiles:
			sprites.rect.center -= vec(scroll)
		for sprites in self.bullets:
			sprites.pos -= vec(scroll)
		for sprites in self.particles:
			sprites.pos -= vec(scroll)
		for rect in self.bg_rects:
			rect[1][1] -= vec(scroll) * rect[0]
		

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
			bgimg = load_image("game_over.png")
			bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height))
			self.display_surface.blit(bgimg,(0,0))
			return

		# aim
		if self.aim_fly:
			player = self.player.sprite
			px,py = player.rect.centerx, player.rect.centery
			pygame.draw.line(self.display_surface,(255,255,255),(px,py),pygame.mouse.get_pos())
			self.player.sprite.reduceLife(40*delta)
		self.health_bar.update(self.display_surface)
	
	def draw_bg(self):
		for rect in self.bg_rects:
			self.display_surface.blit(rect[1][0],rect[1][1])



from random import randint
import sys
import pygame
from load_file import load_image 
from tiles.Item import Box, MedKit,Star
from tiles.Wall import Wall
from tiles.Enemy import Bird,Enemy,Boss
from tiles.Lava import Lava
from tiles.Thorn import Thorn
from setting import *
from player import PMoves, Player
from sprites import HealthBar, Score, Timer
from config import conf
from sound import sound

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
		self.timer = Timer([14, 30], self)
		self.score = Score([14, 70], self)
		self.target_img = load_image("target.png")
		self.game_over=False
		
		self.aim_fly = False
		self.cooldown_medkit = max_cooldown_medkit
		self.cooldown_bird = max_cooldown_bird
		self.cooldown_box = max_cooldown_box

		self.clock = pygame.time.Clock()
		self.is_exit = False

	def play(self):
		# Display the menu
		
		while True:
			self.draw_bg()
		
			# print("Start a game")
			self.process()
			deltaTime=self.clock.tick(120)/1000.0
			if not self.game_over:
				self.update(deltaTime)
				
			else:
				bgimg = load_image("game_over.png")
				sound.stop('music')
				bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height))
				self.display_surface.blit(bgimg,(0,0))

			pygame.display.update()
			# print("End a game")
			if self.is_exit:
				return

	# def pause(self):
	# 	pass

	# def reset(self):
	# 	pass

	def generate_medkit(self):
		obj = MedKit((randint(tile_size*2,self.world_size[0]-tile_size*2)-self.world_shift[0],
					randint(tile_size*2,self.world_size[1]-tile_size*2)-self.world_shift[1]),
					self)
		identical = pygame.sprite.spritecollide(obj, self.tiles, False)
		for tile in identical:
			if not isinstance(tile,Enemy): return
		self.tiles.add(obj)
		self.playerGathers.add(obj)
	
	def generate_box(self):
		obj = Box((randint(tile_size*2,self.world_size[0]-tile_size*2)-self.world_shift[0],
					randint(tile_size*2,self.world_size[1]-tile_size*2)-self.world_shift[1]),
					self)
		identical = pygame.sprite.spritecollide(obj, self.tiles, False)
		for tile in identical:
			if not isinstance(tile,Enemy): return
		self.tiles.add(obj)
		self.playerColliders.add(obj)

	def generate_bird(self,boss=0):
		if not boss:
			bird = Bird((randint(tile_size*1.5,self.world_size[0]-tile_size*1.5)-self.world_shift[0],
					randint(tile_size*1.5,self.world_size[1]-tile_size*1.5)-self.world_shift[1]),
					self)
		else:
			bird = Boss((randint(tile_size*2,self.world_size[0]-tile_size*2)-self.world_shift[0],
				randint(tile_size*2,self.world_size[1]-tile_size*2)-self.world_shift[1]),
				self,boss)
		identical = pygame.sprite.spritecollide(bird, self.player, False)
		if len(identical) == 0:
			# print("New bird is created at ({},{})".format(bird.rect.left,bird.rect.top))
			self.tiles.add(bird)
			self.playerColliders.add(bird)

	def set_screen(self):
		"""Sets (resets) the self.screen variable with the proper fullscreen"""
		if conf.fullscreen:
			fullscreen = pygame.FULLSCREEN | pygame.SCALED
		else:
			fullscreen = 0
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT), fullscreen)

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
				elif cell in ['U','L','R']:
					thorn = Thorn((x,y),tile_size,self,cell)
					self.tiles.add(thorn)
					self.playerColliders.add(thorn)
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
					box = Box((x,y),self)
					self.tiles.add(box)
					self.playerColliders.add(box)
		
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
			if isinstance(sprites,Enemy):
				sprites.pos -= vec(scroll)
			else:
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
			elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and self.game_over:
				self.is_exit = True

		if self.game_over:
			return
		# slomo and fly 
		if pygame.mouse.get_pressed()[0]:
			self.aim_fly=True
		else:
			self.aim_fly=False

		self.scroll_world()

	def update(self,delta):
		# print(self.world_shift)
		self.delta = delta
		if self.aim_fly:
			delta = delta * SLOMO_SPEED

		# Cooldown + Generate star
		self.cooldown_medkit -= delta
		if self.cooldown_medkit <= 0:
			self.cooldown_medkit = max_cooldown_medkit
			for i in range(number_medkit_generated):
				self.generate_medkit()
		
		# Cooldown + Generate bird
		self.cooldown_bird -= delta
		if self.cooldown_bird <= 0:
			self.cooldown_bird = max_cooldown_bird
			cnt = 0
			lbird =[]
			for x in self.playerColliders:
				if isinstance(x,Bird):
					cnt+=1
					lbird.append(x)
			if cnt<10:
				for i in range(number_bird_generated):
					self.generate_bird()
			else:
				for x in lbird:
					x.die()
				self.generate_bird(cnt*2)
		
		# Cooldown + Generate box
		self.cooldown_box -= delta
		if self.cooldown_box <= 0:
			self.cooldown_box = max_cooldown_box
			for i in range(number_box_generated):
				self.generate_box()

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
		# if self.game_over:
		# 	bgimg = load_image("game_over.png")
		# 	bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height))
		# 	self.display_surface.blit(bgimg,(0,0))
		# 	return

		# aim
		if self.aim_fly:
			player = self.player.sprite
			px,py = player.rect.centerx, player.rect.centery
			pygame.draw.line(self.display_surface,(255,255,255),(px,py),pygame.mouse.get_pos())
			self.player.sprite.reduceLife(40*delta)
		self.health_bar.update(self.display_surface)

		self.timer.update()
		self.score.update()
		statisticSurf= pygame.Surface((max(self.timer.text.get_width(),self.score.text.get_width())+50,80))
		statisticSurf.fill((0,0,0))
		statisticSurf.set_alpha(150)
		self.display_surface.blit(statisticSurf,(0,30))
		self.timer.draw(self.display_surface)
		self.score.draw(self.display_surface)
		self.display_surface.blit(
		self.target_img, vec(pygame.mouse.get_pos()) - vec(self.target_img.get_size()) / 2)
	
	def draw_bg(self):
		for rect in self.bg_rects:
			self.display_surface.blit(rect[1][0],rect[1][1])



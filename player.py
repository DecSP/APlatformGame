import pygame 
from load_file import * 
from setting import *
from tiles.Star import Star
from tiles.Lava import Lava
from tiles.Wall import Wall
class PMoves:
	def __init__(self):
		self.flyToMouse = False

class Player(pygame.sprite.Sprite):
	def __init__(self,pos,game):
		super().__init__()
		self.game=game
		self.image = pygame.transform.scale(load_image('ball.png'), (24,24))
		self.rect = self.image.get_rect(topleft = pos)
		self.life = 100

		# player movement
		self.v = pygame.math.Vector2(0,0)
		self.pos=pygame.math.Vector2(pos)
		self.speed = 700
		self.gravity = 600

	def normalize_to_speed(self):
		if self.v.xy!=[0,0]:
			self.v.scale_to_length(self.speed)
		
	def addLife(self,x):
		self.life+=x
		self.life=min(100,self.life)
	def reduceLife(self,x):
		self.life-=x
		self.life=max(0,self.life)

	def collideOthers(self,allHits,delta):
		for hit in allHits:
			if isinstance(hit,Star):
				self.addLife(20)
				hit.kill()
			elif isinstance(hit,Lava):
				self.reduceLife(10)
				self.v*=0.3
			elif isinstance(hit,Wall):
				self.v*=0.7
	def scroll(self, scroll):
		self.pos.x -= scroll[0]
		self.pos.y -= scroll[1]
		self.rect.x = int(self.pos.x)
		self.rect.y = int(self.pos.y)

	def move(self,delta):
		dx = self.v.x  * delta
		dy = self.v.y  * delta

		self.pos.x+=dx
		self.rect.x=int(self.pos.x)
		hits = pygame.sprite.spritecollide(self, self.game.tiles, False)
		for hit in hits:
			if self.v.x > 0:
				self.rect.right = hit.rect.left
			if self.v.x < 0:
				self.rect.left = hit.rect.right
			self.pos.x = self.rect.x
		if len(hits):
			self.v.x*=-0.4
		
		self.pos.y+=dy
		self.rect.y=int(self.pos.y)
		hits2 = pygame.sprite.spritecollide(self, self.game.tiles, False)
		for hit in hits2:
			if self.v.y > 0:
				self.rect.bottom = hit.rect.top
			if self.v.y < 0:
				self.rect.top = hit.rect.bottom
			self.pos.y = self.rect.y
		if len(hits2):
			self.v.y*=-0.4
		
		
		allHits=hits+hits2
		self.collideOthers(allHits,delta)
			


	def flyToMouse(self):
		mouse_pos = pygame.mouse.get_pos()
		cenx = self.rect.centerx
		ceny = self.rect.centery

		self.v.x = mouse_pos[0] - cenx
		self.v.y = mouse_pos[1] - ceny
		self.normalize_to_speed()


	def apply_gravity(self,delta):
		self.v.y += self.gravity*delta

	def update(self,delta,playermoves:PMoves):
		if self.life == 0:
			print("GAME OVER")
			self.game.game_over=True
			return
		if playermoves.flyToMouse:
			self.flyToMouse()
			playermoves.flyToMouse=False
		self.apply_gravity(delta)
		self.move(delta)
	
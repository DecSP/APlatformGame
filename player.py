import pygame 
from load_file import * 
from setting import *
from tiles.Enemy import Bird
from tiles.Item import Box, Star
from tiles.Lava import Lava
from tiles.Wall import Wall
from tiles.Thorn import Thorn
from sprites import CircleExplosion
from util import import_folder
class PMoves:
	def __init__(self):
		self.flyToMouse = False


class Player(pygame.sprite.Sprite):
	def __init__(self,pos,game):
		super().__init__()
		self.game=game
		self.initImg()
		self.rect = self.image.get_rect(topleft = pos)
		self.life = self.max_life = 100

		# player movement
		self.v = pygame.math.Vector2(0,0)
		self.pos=pygame.math.Vector2(pos)
		self.speed = 700
		self.gravity = 600

		self.animation_speed = 6
		self.frameIdx = 0

	def initImg(self):
		images=import_folder("data/player")
		flipImgs = [pygame.transform.flip(x,True,False) for x in images]
		self.images=[images,flipImgs]
		self.image = images[0]
		
	def normalize_to_speed(self):
		if self.v.xy!=[0,0]:
			self.v.scale_to_length(self.speed)
		
	def addLife(self,x):
		self.life+=x
		self.life=min(self.max_life,self.life)
	def reduceLife(self,x):
		self.life-=x
		self.life=max(0,self.life)
	def extendLife(self,x):
		self.max_life+=x

	def collideOthers(self,allHits,delta):
		for hit in allHits:
			if isinstance(hit,Bird):
				self.game.particles.append(
                    CircleExplosion(hit.rect.center, (50, 50, 255), 7, 100)
                )
				hit.kill()
				self.addLife(20)
			elif isinstance(hit,Star):
				self.game.particles.append(
                    CircleExplosion(hit.rect.center, (255, 255, 50), 7, 100)
                )
				self.addLife(30)
				hit.kill()
			elif isinstance(hit,Box):
				self.game.particles.append(
                    CircleExplosion(hit.rect.center, (50, 255, 50), 7, 100)
                )
				self.extendLife(30)
				self.addLife(30)
				hit.kill()
			elif isinstance(hit,Lava):
				self.reduceLife(20)
				self.v*=0.3
			elif isinstance(hit,Thorn):
				self.reduceLife(15)
				self.v*=0.8
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
		hits = pygame.sprite.spritecollide(self, self.game.playerColliders, False)
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
		hits2 = pygame.sprite.spritecollide(self, self.game.playerColliders, False)
		for hit in hits2:
			if self.v.y > 0:
				self.rect.bottom = hit.rect.top
			if self.v.y < 0:
				self.rect.top = hit.rect.bottom
			self.pos.y = self.rect.y
		if len(hits2):
			self.v.y*=-0.4
		
		
		allHits=hits+hits2+pygame.sprite.spritecollide(self,self.game.playerGathers,False)
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

	def animate(self,delta):
		mouse_pos = pygame.mouse.get_pos()
		self.frameIdx += delta*self.animation_speed
		while self.frameIdx >= len(self.images[0]):
			self.frameIdx-=len(self.images[0])
		if self.v.y > 100:
			self.frameIdx = 3
		elif self.v.y < -100:
			self.frameIdx = 2
		self.image=self.images[mouse_pos[0]<self.pos[0]][int(self.frameIdx)]

	def update(self,delta,playermoves:PMoves):
		if self.life == 0:
			print("GAME OVER")
			self.game.particles.append(
                    CircleExplosion(self.rect.center, (255, 50, 50), 7, 100)
                )
			self.game.game_over=True
			return
		if playermoves.flyToMouse:
			self.flyToMouse()
			playermoves.flyToMouse=False
		self.apply_gravity(delta)
		self.move(delta)
		self.animate(delta)
	
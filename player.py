from random import randint
import pygame 
from load_file import * 
from setting import *
from tiles.Enemy import Bird, Boss, Enemy
from tiles.Item import Box, MedKit, Potion, Star
from tiles.Lava import Lava
from tiles.Thorn import Thorn
from tiles.Wall import Wall
from tiles.Thorn import Thorn
from sprites import CircleExplosion
from util import import_folder
from sound import sound
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
		self.starModeTime = 0
		self.starShootDur = 0.4
		self.nextShoot = 0

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
		
	def normalize_to_speed(self,speed):
		if self.v.xy!=[0,0]:
			self.v.scale_to_length(speed)
		
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
				sound.play('explode')
				hit.die()
				self.game.score.score+=1
				self.addLife(20)
			elif isinstance(hit,Boss):
				hit.reduceLife(1)
				sound.play('explode')
				if hit.life == 0: 
					self.game.score.score+=hit.max_life
					hit.die()
			elif isinstance(hit,MedKit):
				self.game.particles.append(
                    CircleExplosion(hit.rect.center, (255, 50, 50), 7, 100)
                )
				self.addLife(30)
				sound.play('item')
				hit.kill()
			elif isinstance(hit,Star):
				self.game.particles.append(
                    CircleExplosion(hit.rect.center, (255, 255, 50), 7, 100)
                )
				self.starModeTime = 3
				sound.stop('music')
				sound.play('star_power',-1)
				hit.kill()
			elif isinstance(hit,Potion):
				self.game.particles.append(
                    CircleExplosion(hit.rect.center, (50, 255, 50), 7, 100)
                )
				self.extendLife(30)
				self.addLife(30)
				sound.play('upgrade')
				hit.kill()
			elif isinstance(hit,Box):
				self.game.particles.append(
                    CircleExplosion(hit.rect.center, (255, 255, 255), 7, 100)
                )
				sound.play('box')
				dif=(tile_size-item_size)/2
				v = hit.rect.topleft
				v = [v[0]+dif,v[1]+dif]
				if randint(1,3)==1:
					obj=Potion(v,item_size,self.game)
				else:
					obj=Star(v,item_size,self.game)
				self.game.tiles.add(obj)
				self.game.playerGathers.add(obj)
				hit.kill()
			elif isinstance(hit,Lava):
				self.reduceLife(20)
				sound.play('hurt')
				self.v*=0.3
			elif isinstance(hit,Thorn):
				self.reduceLife(15)
				sound.play('hurt')
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
			if abs(self.pos.x-self.rect.x)>50:
				self.rect.x=self.pos.x
			else: self.pos.x = self.rect.x
		if len(hits):
			self.v.x*=-0.6
		
		self.pos.y+=dy
		self.rect.y=int(self.pos.y)
		hits2 = pygame.sprite.spritecollide(self, self.game.playerColliders, False)
		for hit in hits2:
			if self.v.y > 0:
				self.rect.bottom = hit.rect.top
			if self.v.y < 0:
				self.rect.top = hit.rect.bottom
			if abs(self.pos.y-self.rect.y)>50:
				self.rect.y=self.pos.y
			else:self.pos.y = self.rect.y
		if len(hits2):
			self.v.y*=-0.6
		
		
		allHits=hits+hits2+pygame.sprite.spritecollide(self,self.game.playerGathers,False)
		self.collideOthers(allHits,delta)
			


	def flyToMouse(self):
		mouse_pos = pygame.mouse.get_pos()
		cenx = self.rect.centerx
		ceny = self.rect.centery

		self.v.x = mouse_pos[0] - cenx
		self.v.y = mouse_pos[1] - ceny
		speed = self.speed*min(1,self.v.length()/150)
		self.normalize_to_speed(speed)

	def starMode(self,delta):
		if self.starModeTime>0:
			self.starModeTime -=delta
			if self.starModeTime<=0:
				sound.stop('star_power')
				if not self.game.game_over:
					sound.play('music',-1)
		if self.starModeTime<=0:
			return
		self.nextShoot -=delta
		if self.nextShoot <= 0:
			self.nextShoot = self.starShootDur
			v=vec([1,0])
			n=randint(10,30)
			for j in range(n):
				self.game.bullets.append(
					Bullet(
						self.game,
						v.rotate(360/n*j),
						vec(self.rect.center)
					)

				)


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
			sound.play('die')
			sound.play('gameover')
			self.game.particles.append(
                    CircleExplosion(self.rect.center, (255, 50, 50), 7, 100)
                )
			self.game.game_over=True
			return
		if playermoves.flyToMouse:
			self.flyToMouse()
			sound.play('swoosh')
			playermoves.flyToMouse=False
		
		self.starMode(delta)
		self.apply_gravity(delta)
		self.move(delta)
		self.animate(delta)
	


class Bullet:
	def __init__(self, game, vector, pos,color = (100,255,100)):
		self.game = game
		self.color = color
		try:
			self.vector = vector.normalize()
		except:
			self.vector = vec(0, 0)
		self.pos = vec(pos)

	def update(self, dt):
		for tile in self.game.tiles:
			if isinstance(tile,Wall):
				if tile.rect.collidepoint(self.pos):
					try:
						self.game.bullets.remove(self)
					except:
						pass
			elif isinstance(tile,Enemy):
				if tile.rect.collidepoint(self.pos):
					try:
						if isinstance(tile,Bird):
							tile.die()
						else:
							tile.reduceLife(1)
							if tile.life==0:
								tile.die()
						self.game.bullets.remove(self)
					except:
						pass

		self.pos += self.vector * 500 * dt
		if not (-50 <= self.pos.x <= self.game.display_surface.get_width() + 50):
			try:
				self.game.bullets.remove(self)
			except:
				pass
		if not (-50 <= self.pos.y <= self.game.display_surface.get_height() + 50):
			try:
				self.game.bullets.remove(self)
			except:
				pass

	def draw(self, surface):
		pygame.draw.line(
			surface, self.color, self.pos, self.pos + self.vector * 30, 4
		)

from random import randint
import pygame 
from Tile import *
from setting import *
from tiles.Wall import Wall

class Enemy(pygame.sprite.Sprite):
    pass

class EnemyBullet:
	def __init__(self, game, vector, pos):
		self.game = game
		try:
			self.vector = vector.normalize()
		except:
			self.vector = vec(0, 0)
		self.pos = vec(pos)

	def update(self, dt):
		for tile in self.game.tiles:
			if not isinstance(tile,Wall): continue
			if tile.rect.collidepoint(self.pos):
				try:
					self.game.bullets.remove(self)
				except:
					pass
		if not self.game.game_over and self.game.player.sprite.rect.collidepoint(self.pos):
			self.game.player.sprite.reduceLife(50)
			try:
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
			surface, (255, 255, 50), self.pos, self.pos + self.vector * 20, 3
		)

def initImage():
	img=pygame.transform.scale2x(load_image("bird.png"))
	swidth = 64
	images=[]
	for i in range(img.get_width()//swidth):
		surf=pygame.Surface((swidth,swidth))
		surf.set_colorkey((0,0,0))
		surf.blit(img,(-i*swidth,0))
		images.append(surf)
	
	flipImgs = [pygame.transform.flip(x,True,False) for x in images]
	return [images,flipImgs]

birdImgs = initImage()
class Bird(Enemy):
	def __init__(self,pos,game):
		pygame.sprite.Sprite.__init__(self)
		self.pos=pos
		self.game=game
		self.image=birdImgs[0][0]
		self.rect = self.image.get_rect(topleft = pos)
		self.last_shot=0
		self.range=[1000,2000]
		self.shot_dur = randint(self.range[0], self.range[1])

		self.animation_speed = 10
		self.frameIdx = 0



	def animate(self,delta):
		ppos = self.game.player.sprite.pos
		self.frameIdx += delta*self.animation_speed
		while self.frameIdx >= len(birdImgs[0]):
			self.frameIdx-=len(birdImgs[0])
		self.image=birdImgs[ppos[0]>self.rect.centerx][int(self.frameIdx)]

	def update(self,delta):
		self.last_shot+=delta*1000
		if self.last_shot > self.shot_dur:
			self.last_shot = 0
			self.shot_dur = randint(self.range[0], self.range[1])
			self.game.bullets.append(
				EnemyBullet(
					self.game,
					(
						vec(self.game.player.sprite.rect.center)
						- vec(self.rect.center)
					).rotate(randint(-10, 10)),
					vec(self.rect.center),
				)
			)
		self.animate(delta)

from random import randint
import pygame 
from Tile import *
from setting import *
from sprites import CircleExplosion
from tiles.Wall import Wall
from sound import sound

class Enemy(pygame.sprite.Sprite):
    pass

class EnemyBullet:
	def __init__(self, game, vector, pos,color = (100,100,255)):
		self.game = game
		self.color = color
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
			surface, self.color, self.pos, self.pos + self.vector * 30, 4
		)

def changeColor(image, color):
	colouredImage = pygame.Surface(image.get_size())
	colouredImage.fill(color)

	finalImage = image.copy()
	finalImage.blit(colouredImage, (0, 0), special_flags = pygame.BLEND_MULT)
	return finalImage

def initImage(boss=False):
	img=pygame.transform.scale2x(load_image("bird.png"))
	swidth = 64
	if boss:
		img=pygame.transform.scale2x(img)
		swidth = 128
	images=[]
	for i in range(img.get_width()//swidth):
		surf=pygame.Surface((swidth,swidth))
		surf.fill((0,0,0))
		surf.set_colorkey((0,0,0))
		surf.blit(img,(-i*swidth,0))
		images.append(surf)
	
	flipImgs = [pygame.transform.flip(x,True,False) for x in images]
	return [images,flipImgs]

birdImgs = initImage()
class Bird(Enemy):
	def __init__(self,pos,game):
		pygame.sprite.Sprite.__init__(self)
		self.pos=vec(pos)
		self.game=game
		self.image=birdImgs[0][0]
		self.rect = self.image.get_rect(topleft = pos)
		self.last_shot=0
		self.range=[2000,5000]
		self.shot_dur = randint(self.range[0], self.range[1])

		self.animation_speed = 10
		self.frameIdx = 0

	def die(self):
		self.game.particles.append(
			CircleExplosion(self.rect.center, (50, 50, 255), 7, 100)
		)
		self.kill()

	def animate(self,delta):
		ppos = self.game.player.sprite.pos
		self.frameIdx += delta*self.animation_speed
		while self.frameIdx >= len(birdImgs[0]):
			self.frameIdx-=len(birdImgs[0])
		X=255*self.last_shot/self.shot_dur
		self.image=changeColor(birdImgs[ppos[0]>self.rect.centerx][int(self.frameIdx)],(255,255-X,255-X,100))

	def update(self,delta):
		self.last_shot+=delta*1000
		self.rect.center = self.pos
		if (self.game.player.sprite.pos - self.pos).length() < 1500:
			self.pos.x += (-self.pos.x + self.game.player.sprite.rect.centerx) / 80
			self.rect.center = self.pos
		if self.last_shot > self.shot_dur:
			self.last_shot = 0
			self.shot_dur = randint(self.range[0], self.range[1])
			v=vec(self.game.player.sprite.rect.center)- vec(self.rect.center)
			if v.length()<2000:
				sound.play('fireball')
				self.game.bullets.append(
					EnemyBullet(
						self.game,
						v.rotate(randint(-10, 10)),
						vec(self.rect.center),
					)
				)
		self.animate(delta)

bossImgs = initImage(True)
class Boss(Enemy):
	def __init__(self,pos,game,life):
		pygame.sprite.Sprite.__init__(self)
		self.pos=vec(pos)
		self.game=game
		self.image=bossImgs[0][0]
		self.life = self.max_life = life
		self.rect = self.image.get_rect(topleft = pos)
		self.last_shot=0
		self.range=[2000,5000]
		self.shot_dur = randint(self.range[0], self.range[1])

		self.animation_speed = 10
		self.frameIdx = 0

	def reduceLife(self,x):
		self.life -= x
		self.life = max(0,self.life)

	def die(self):
		sound.play('boss_die')
		self.game.particles.append(
			CircleExplosion(self.rect.center, (50, 50, 255), 7, 100)
		)
		self.kill()

	def animate(self,delta):
		ppos = self.game.player.sprite.pos
		self.frameIdx += delta*self.animation_speed
		while self.frameIdx >= len(bossImgs[0]):
			self.frameIdx-=len(bossImgs[0])
		X= max(1-self.life/self.max_life,0.1)
		Y =255*self.last_shot/self.shot_dur
		color =(255*X,(255-Y)*X,(255-Y)*X,100)
		self.image=changeColor(bossImgs[ppos[0]>self.rect.centerx][int(self.frameIdx)],color)

	def update(self,delta):
		self.last_shot+=delta*1000
		self.rect.center = self.pos
		if 300<(self.game.player.sprite.pos - self.pos).length() < 1500:
			self.pos.x += (-self.pos.x + self.game.player.sprite.rect.centerx) / 80
			self.pos.y += (-self.pos.y + self.game.player.sprite.rect.centery) / 80
			self.rect.center = self.pos
		if self.last_shot > self.shot_dur:
			self.last_shot = 0
			self.shot_dur = randint(1100, 4000)
			v=vec(self.game.player.sprite.rect.center)- vec(self.rect.center)
			n=randint(10,30)
			for j in range(n):
				self.game.bullets.append(
					EnemyBullet(
						self.game,
						v.rotate(360/n*j),
						vec(self.rect.center),
						(255,0,0)
					)
				)
		self.animate(delta)

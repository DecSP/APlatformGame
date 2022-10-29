from random import randint
import pygame 
from Tile import *
from setting import *

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
            if isinstance(tile,Star): continue
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



class Star(Tile):
	def __init__(self,pos,size,game):
		super().__init__(pos,size,'star.png',game)
		self.last_shot=0
		self.range=[1000,2000]
		self.shot_dur = randint(self.range[0], self.range[1])

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

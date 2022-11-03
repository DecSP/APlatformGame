import pygame
from setting import *
class HealthBar:
    def __init__(
        self, obj, pos, width, height, h_color=(205, 22, 22), o_color=(0, 0, 0), o_width=1
    ):
        self.pos = vec(pos)
        self.width = width
        self.init_width = width
        self.obj = obj
        self.height = height
        self.h_color = h_color
        self.o_color = o_color
        self.o_width = o_width

    def update(self, surface):
        pygame.draw.rect(
            surface, (0, 0, 0), pygame.Rect(self.pos, (self.init_width*self.obj.max_life/100, self.height))
        )
        pygame.draw.rect(
            surface, self.h_color, pygame.Rect(self.pos, (self.init_width*self.obj.life/100, self.height))
        )
        pygame.draw.rect(
            surface,
            self.o_color,
            pygame.Rect(self.pos, (self.init_width*self.obj.max_life/100, self.height)),
            self.o_width,
        )

class Timer: 
    def __init__(self, pos, game):
        self.pos = pos
        self.game = game
        self.time = 0

    def update(self):
        self.time += self.game.delta
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.text = self.font.render("Time: {}s".format(int(self.time)), True, "turquoise1")

    def draw(self,surface):
        surface.blit(self.text, self.pos)

class Score: 
    def __init__(self, pos, game):
        self.pos = pos
        self.game = game
        self.score = 0

    def update(self):
        self.font = pygame.font.SysFont("Arial", 30, bold=True)
        self.text = self.font.render("Score: {}".format(self.score), True, "turquoise1")

    def draw(self,surface):
        surface.blit(self.text, self.pos)

class CircleExplosion:
    def __init__(
        self, pos, color, initial_width, radius_increment=3, lighting_color=None
    ):
        (
            self.radius,
            self.width,
            self.pos,
            self.killed,
            self.color,
            self.radius_increment,
        ) = (10, initial_width, pos, False, color, radius_increment)
        self.lighting_color = lighting_color

    def update(self, dt, surface):
        self.radius += self.radius_increment * dt
        self.width -= 7 * dt
        if self.width > 1:
            pygame.draw.circle(
                surface, self.color, self.pos, self.radius, int(self.width)
            )
        else:
            self.killed = True

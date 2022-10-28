import pygame
from setting import *
class HealthBar:
    def __init__(
        self, pos, width, height, h_color=(205, 22, 22), o_color=(0, 0, 0), o_width=1
    ):
        self.pos = vec(pos)
        self.width = width
        self.init_width = width
        self.height = height
        self.h_color = h_color
        self.o_color = o_color
        self.o_width = o_width

    def update(self, surface, percent):
        pygame.draw.rect(
            surface, (0, 0, 0), pygame.Rect(self.pos, (self.init_width, self.height))
        )
        pygame.draw.rect(
            surface, self.h_color, pygame.Rect(self.pos, (self.init_width*percent/100, self.height))
        )
        pygame.draw.rect(
            surface,
            self.o_color,
            pygame.Rect(self.pos, (self.init_width, self.height)),
            self.o_width,
        )

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

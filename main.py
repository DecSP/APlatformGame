import pygame
from setting import * 

# Pygame setup
pygame.init()
# print((screen_width,screen_height))
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

from level import Level
level = Level(level_map,screen)
while True:
	level.draw_bg()
	
	# print("Start a game")
	level.process()
	deltaTime=clock.tick(120)/1000.0
	level.update(deltaTime)

	# print("End a game")
	pygame.display.update()
		
		
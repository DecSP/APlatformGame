import pygame
from setting import * 
from level import Level

# Pygame setup
pygame.init()
# print((screen_width,screen_height))
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

level = Level(level_map,screen)
while True:
	screen.fill('black')
	
	# print("Start a game")
	level.process()
	deltaTime=clock.tick(120)/1000.0
	level.update(deltaTime)

	# print("End a game")
	pygame.display.update()
		
		
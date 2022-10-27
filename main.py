import pygame, sys
from setting import * 
from level import Level

# Pygame setup
pygame.init()
# print((screen_width,screen_height))
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()

level = Level(level_map,screen)
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	
	screen.fill('black')
	
	# print("Start a game")
	level.run()
	# print("End a game")
	pygame.display.update()
	clock.tick(60)
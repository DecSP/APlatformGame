import pygame
from setting import * 

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))

from sound import sound
from level import Level


while True:
	sound.play("music", -1)
	
	level = Level(level_map,screen)
	level.play()
	del level

	sound.stop("music")





		
		
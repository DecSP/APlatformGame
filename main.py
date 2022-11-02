import pygame
from setting import * 

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))

from sound import sound
from level import Level
from menu import Menu


while True:
	
	level = Level(level_map,screen)
	menu = Menu(level)
	menu.show()
	sound.play("music",-1)
	level.play()
	del level

	sound.stop_all()






		
		
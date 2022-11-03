from os import walk
from load_file import filename
import pygame

def import_folder(path):
	surface_list = []
	path = filename(path)
	for _,__,img_files in walk(path):
		for image in img_files:
			full_path = path + '/' + image
			image_surf =pygame.transform.scale2x(pygame.image.load(full_path).convert_alpha())
			surface_list.append(image_surf)

	return surface_list

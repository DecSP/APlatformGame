import os
import sys
import pygame
# from constants import LOAD_DIR, SOUND_DIR
SOUND_DIR = 'sounds'
LOAD_DIR = 'data'

pygame.init()

def filename(name):
    # Find out where we are, or in the case of an exe
    if hasattr(sys, "frozen"):
        basedir = sys.prefix
    else:
        return name
    filename = os.path.join(basedir, name)
    return filename

img_memo={}
def load_image(name, colorkey=None):
    if name in img_memo:
        return img_memo[name]
    fullname = os.path.join(filename(LOAD_DIR), name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    img_memo[name]=image
    return image

def load_sound(name):
    fullname = os.path.join(filename(SOUND_DIR), name)
    sound = pygame.mixer.Sound(fullname[:-3]+'ogg')
    return sound

import os
import pygame
import sys

from setting import *


def detect_collision(sprite1, sprite2):
    """Detect a collision between two sprites"""

    sp1_mask = pygame.mask.from_surface(sprite1.image, 0)
    sp2_mask = pygame.mask.from_surface(sprite2.image, 0)

    offset = sprite2.rect.x - sprite1.rect.x, sprite2.rect.y - sprite1.rect.y

    return bool(sp1_mask.overlap(sp2_mask, offset))


__font_objs = {}


def __get_font(size):

    if size not in __font_objs:
        __font_objs[size] = pygame.font.Font(filename(FONT_FILENAME), size)

    return __font_objs[size]


def render_text(text, size, colour=WHITE):
    """Render some text"""

    return __get_font(size).render(text, True, colour)


def get_text_height(size):
    """Check the height of a certain size of text"""

    return __get_font(size).get_height()


def get_text_width(text, size):
    """Check the width of a certain size of text"""
    return __get_font(size).size(text)[0]


def draw_background_main():
    """Render the background for main screen."""
    background = pygame.image.load(filename("bg_main.png"))
    return background


def draw_background_menu():
    """Render the background for menu screen."""
    background = pygame.image.load(filename("bg_menu.png"))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    return background


def filename(name):
    """Get the path of a data file"""

    # Is this The Right Way(tm)?

    # Find out where we are, or in the case of an exe
    if hasattr(sys, "frozen"):
        basedir = sys.prefix
    else:
        basedir = sys.path[0]

    filename = os.path.join(basedir, DATA_DIRNAME, name)

    if not os.access(filename, os.F_OK | os.R_OK):
        print("Could not find file '%s'." % filename)
        raise SystemExit

    return filename


def none_func(*args, **kwargs):
    """Do nothing, gracefully."""
    pass

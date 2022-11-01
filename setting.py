# Lava: X
# Thorn-up: U
# Thorn-left: L
# Thorn-right: R
# Wall: W
### Init value
# Player: P
# S: Star
# E: Enemy
# B: Box
import pygame
level_map = [
'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU',
'L                                                                     R',
'L                                                      S              R',
'L                                                                     R',
'L                                   S                                 R',
'L        E     WWWW       S                  B   WWWW                 R',
'L   B                            B                          S         R',
'L                                                                     R',
'L           E          E                                   E          R',
'L                 P                       E                           R',
'L  WWWWW       WWWWWW       WWWWWW       WWWWWW    WWWWW    WWWWWW    R',
'L                                                                     R',
'L                                                                     R',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
item_size = 48
player_size = [32,32]
tile_size = 64
screen_width = 1200
screen_height = 704

max_cooldown_star = 4
max_cooldown_bird = 4
max_cooldown_box = 10

number_star_generated = 8
number_bird_generated = 5
number_box_generated = 4

SLOMO_SPEED = 0.3

vec=pygame.math.Vector2


SOUND_FILES = (
    "explode.wav",
    "music.mp3",
    "title.mp3",
    "die.wav",
    "slash.wav",
    "dash.wav",
    "menu_choosing.wav",
    "menu_picked.wav",
    "menu_switch.wav",
    "bullet1.mp3",
    "bullet2.wav",
    "shield.wav",
)

BACKGROUND = (0x11, 0x11, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)

MENU_FRAME_RATE = 24
TRANSPARENT = BLACK

HIGHSCORES_AMOUNT = 10
GAME = "APlatform Game"
WIDTH, HEIGHT = (screen_width, screen_height)
# WIDTH, HEIGHT = (len(level_map[0])*tile_size,len(level_map)*tile_size)
DATA_DIRNAME = "data"

FONT_FILENAME = "font.ttf"
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
'L  B                                                                B R',
'L                                                                     R',
'L                                                                     R',
'L                                                                     R',
'L              WWWW                          B   WWWW                 R',
'L   B                                                                 R',
'L                                                                     R',
'L                                                                     R',
'L                 P                                                   R',
'L  WWWWW       WWWWWW       WWWWWW       WWWWWW    WWWWW    WWWWWW    R',
'L                                                                     R',
'L                                                                   B R',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
item_size = 32
player_size = [32,32]
tile_size = 64
screen_width = 1200
screen_height = 704

max_cooldown_medkit = 4
max_cooldown_bird = 6
max_cooldown_box = 10

number_medkit_generated = 2
number_bird_generated = 5
number_box_generated = 1

SLOMO_SPEED = 0.3

vec=pygame.math.Vector2


SOUND_FILES = (
    "explode.wav",
    "music.mp3",
    "title.mp3",
    "die.wav",
    "menu_choosing.wav",
    "menu_picked.wav",
    "menu_switch.wav",
    "fireball.wav",
    "gameover.mp3",
    "item.mp3",
    "upgrade.mp3",
    "swoosh.wav",
    "hurt.wav",
    "boss_die.mp3",
    "star_power.mp3",
    "box.wav",
)

BACKGROUND = (0x11, 0x11, 0x00)
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0x00, 0x00, 0x00)

MENU_FRAME_RATE = 24
TRANSPARENT = BLACK

HIGHSCORES_AMOUNT = 10
GAME = "Bird's Rage"
WIDTH, HEIGHT = (screen_width, screen_height)
# WIDTH, HEIGHT = (len(level_map[0])*tile_size,len(level_map)*tile_size)
DATA_DIRNAME = "data"

FONT_FILENAME = "font.ttf"
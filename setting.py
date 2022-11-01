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

number_star_generated = 9
number_bird_generated = 5

SLOMO_SPEED = 0.3

vec=pygame.math.Vector2
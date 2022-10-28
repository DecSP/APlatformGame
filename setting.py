# level_map = [
# '                            ',
# '                   X        ',
# '                            ',
# ' XX    XXX            XX    ',
# ' XX P                       ',
# ' XX X         XX         XX ',
# '                            ',
# '                  XX  XX    ',
# '                  XX  XXX   ',
# 'XXXXXXXX  XXXXXX  XX  XXXX  ',
# 'XXXXXXXX  XXXXXX  XX  XXXX  ']

# screen_height = 700
# print(screen_height, screen_width)
# How to scroll-y


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
'UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU',
# 'L                 E                 R',
'L                                   R',
'L                                   R',
'L        S                S         R',
'L   B                            B  R',
'L                 S                 R',
'L           S          S            R',
'L                 P                 R',
'L  WWWWW       WWWWWW      WWWW     R',
'L                                   R',
'L                                   R',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']
item_size = 24
tile_size = 64
screen_width = 1200
screen_height = len(level_map) * tile_size #704

SLOMO_SPEED = 0.3

vec=pygame.math.Vector2
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
'WUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUW',
'L                                                                     R',
'L                                                      S              R',
'L                                                                     R',
'L                                   S                                 R',
'L        S     WWWW       S                      WWWW                 R',
'L   B                            B                          S         R',
'L                                                                    R',
'L           S          S                                   S          R',
'L                 P                       S                           R',
'L  WWWWW       WWWWWW       WWWWWW       WWWWWW    WWWWW    WWWWWW    R',
'L                                                                     R',
'L                                                                     R',
'WXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXW']
item_size = 24
tile_size = 64
screen_width = 1200
screen_height = 704

SLOMO_SPEED = 0.3

vec=pygame.math.Vector2
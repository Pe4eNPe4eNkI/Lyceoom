from parameters import *
from numba.core import types
from numba.typed import Dict
from numba import int32
import pygame
from random import choice

# тут создается карта и всё связанное с ней
_ = False
map_x = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, 3, _, 4, _, _, _, _, _, 1],
    [1, 2, 2, 2, _, _, _, _, _, 2, 2, 2, _, _, _, 3, _, _, _, _, 4, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 2, _, 2, 2, _, _, 3, 3, _, _, _, _, _, _, 1],
    [1, _, 2, 2, 2, _, 4, _, _, _, _, _, 2, _, 4, _, _, 3, _, _, _, 4, _, 1],
    [1, _, 3, _, _, _, 4, _, _, 2, _, _, 2, _, _, _, _, _, _, 4, _, _, _, 1],
    [1, _, 3, _, _, _, 2, _, _, 2, 2, _, 2, _, _, _, 4, _, _, _, _, 4, _, _],
    [1, _, _, 3, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, 3, _, _, _, _, _, _, _, 3, _, _, 3, 3, _, _, _, _, 3, 3, _, _, 1],
    [1, _, 3, _, _, _, 3, 3, _, 3, _, _, _, 3, 3, _, _, _, _, 2, 3, _, _, 1],
    [1, _, _, 4, _, _, _, _, 4, _, _, _, _, 2, 2, 2, 2, 2, 2, 2, 2, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 4, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# map_x = [
#    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]

map_y = [
    [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1, 1],
        [1, 2, 2, 2, _, _, _, _, _, 2, 2, 2, _, _, _, _, _, _, _, 4, _, _, 1],
        [1, _, _, _, _, _, _, _, _, 2, _, 2, 2, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 2, 2, _, _, _, _, _, _, _, _, 2, _, _, _, _, 4, _, _, 4, _, 1],
        [_, _, 3, _, _, _, 4, _, _, 2, _, _, 2, 2, 2, 2, _, _, 4, _, _, _, _],
        [1, _, 3, _, _, _, 2, _, _, 2, 2, _, 2, _, _, _, _, _, _, _, 4, _, 2],
        [1, _, _, 3, _, _, 2, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 3, _, _, _, _, _, _, _, 3, _, _, _, _, _, _, 3, 3, 3, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 3, _, _, _, _, _, _, _, 3, _, _, _, _, _, _, 3, 3, 3, _, _, 1],
        [1, _, _, _, _, _, _, 1, _, _, 4, _, _, _, _, _, _, _, _, 2, _, _, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [
        [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, 1, _, _, _, _, _, _, _, 1],
        [1, 2, 2, 2, _, _, _, _, _, 2, 2, 2, _, _, _, _, _, _, _, 4, _, _, 1],
        [1, _, _, _, _, _, _, _, _, 2, _, 2, 2, _, _, _, _, _, _, _, _, _, 1],
        [1, 1, 2, 2, _, _, _, _, _, _, _, _, 2, _, _, _, _, 4, _, _, 4, _, 1],
        [_, _, 3, _, _, _, 2, _, _, 2, 2, _, 2, 2, 2, 2, 2, _, _, _, 4, _, _],
        [1, _, _, 3, _, _, 2, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 3, _, _, _, _, _, _, _, 3, _, _, _, _, _, _, 3, 3, 3, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, _, _, _, _, _, 1, _, _, 4, _, _, _, _, _, _, _, _, 2, _, _, 1],
        [1, _, 3, _, _, _, 4, _, _, 2, _, _, 2, _, _, _, _, _, 4, _, _, _, 1],
        [1, _, _, _, _, _, _, 1, _, _, 4, _, _, _, _, _, _, _, _, 2, _, _, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ],
    [
        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, 2, _, 2, _, _, _, _, _, 2, 2, 2, _, _, _, _, _, 3, _, 4, _, _, 1],
        [1, _, _, 1, _, _, _, _, _, 2, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 2, 2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 4, _, 1],
        [_, _, 3, _, _, _, 2, _, _, 2, 2, _, 2, 2, 2, 2, 2, _, _, _, 4, _, _],
        [1, _, _, 3, _, _, 2, _, _, _, 1, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, 3, _, _, _, _, _, _, _, 3, _, _, _, _, _, _, 3, 3, 3, _, _, 1],
        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
        [1, _, _, _, _, _, _, 1, _, _, 4, _, _, _, _, _, _, _, _, 2, _, _, 1],
        [1, _, 3, _, _, _, 4, _, _, 2, _, _, _, _, _, _, _, 1, 4, _, _, _, 1],
        [1, _, _, 1, 1, 2, 2, 1, _, _, 4, _, _, _, _, _, _, _, _, 2, _, _, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
]

# map_y = [
#    [
#        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#    ],
#    [
#        [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#    ],
#    [
#        [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [_, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
#        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
#    ]
# ]
#  координаты стен

x = len(map_y)

z_map = []

for i in range(x):
    while len(z_map) != x:
        world_map = choice(map_y)
        if world_map not in z_map:
            z_map.append(world_map)
a_map = z_map[0]

for i in range(1, x):
    for j in range(len(a_map)):
        a_map[j] += z_map[i][j]

W_WORLD = len(a_map[0]) * CELL
H_WORLD = len(a_map) * CELL

mini_map = set()
txt_map = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
collision_walls = []

for j, row in enumerate(a_map):
    for i, char in enumerate(row):
        if char:
            mini_map.add((i * MAP_CELL, j * MAP_CELL))
            collision_walls.append(pygame.Rect(i * CELL, j * CELL, CELL, CELL))
            if char == 1:
                txt_map[(i * CELL, j * CELL)] = 1
            elif char == 2:
                txt_map[(i * CELL, j * CELL)] = 2
            elif char == 3:
                txt_map[(i * CELL, j * CELL)] = 3
            elif char == 4:
                txt_map[(i * CELL, j * CELL)] = 4

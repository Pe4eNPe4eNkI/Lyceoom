import pygame
from parameters import *
from map import txt_map


def ray_casting(gamer_pos, gamer_angle, world_map):
    casted_walls = []
    ox, oy = gamer_pos
    xm, ym = mapping(ox, oy)
    cur_angle = gamer_angle - HALF_FOV
    texture_v, texture_h = 1, 1
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
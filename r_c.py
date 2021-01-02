import pygame
from parameters import *
from map import txt_map


def ray_casting(monitor, gamer_pos, gamer_angle):
    view_angle = gamer_angle - H_FOV
    ox, oy = gamer_pos
    for ray in range(N_RAYS):
        sin_a = math.sin(view_angle)
        cos_a = math.cos(view_angle)
        for i in range(MAX_DEPTH):
            x = ox + i * cos_a
            y = oy + i * sin_a
            pygame.draw.line(monitor, DARKGREY, gamer_pos, (x, y), 2)
            if (x // CELL * CELL, y // CELL * CELL) in txt_map:
                hight = PROJ_COEFF / depth
                pygame.draw.rect(monitor, WHITE, (ray * SCALE, H_HEIGHT - proj_height // 2, SCALE))
                break
        view_angle += DELTA_ANGLE
import pygame
from parameters import *
from map import txt_map


def mapping(a, b):
    return int((a // CELL) * CELL), int((b // CELL) * CELL)

def ray_casting(monitor, gamer_pos, gamer_angle):
    ox, oy = gamer_pos
    xm, ym = mapping(ox, oy)
    view_angle = gamer_angle - H_FOV
    for ray in range(N_RAYS):
        sin_a = math.sin(view_angle)
        cos_a = math.cos(view_angle)

        x, dx = (xm + CELL, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, CELL):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in txt_map:
                break
            x += dx * CELL

        y, dy = (ym + CELL, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, CELL):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy) in txt_map:
                break
            y += dy * CELL

        depth = depth_v if depth_v < depth_h else depth_h
        depth *= math.cos(gamer_angle - view_angle)
        depth = max(depth, 0.00001)
        hight = min((PROJ_C / depth), 2 * HEIGHT)
        a = 255 / (1 + depth * depth * 0.0001)
        color = (a, a, a)
        pygame.draw.rect(monitor, color, (ray * SCALE, H_HEIGHT - hight // 2, SCALE, hight))
        view_angle += DELTA_ANGLE
from parameters import *
from map import txt_map
from r_c import mapping
import math
import pygame
from numba import njit


@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_x, npc_y, txt_map, pos_gamer):
    ox, oy = pos_gamer
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    view_angle = math.atan2(delta_y, delta_x)
    view_angle += math.pi

    sin_a = math.sin(view_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(view_angle)
    cos_a = cos_a if cos_a else 0.000001

    x, dx = (xm + CELL, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // CELL):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in txt_map:
            return False
        x += dx * CELL

    y, dy = (ym + CELL, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // CELL):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in txt_map:
            return False
        y += dy * CELL
    return True


class Interaction:
    def __init__(self, gamer, sprites, malen):
        self.gamer = gamer
        self.sprites = sprites
        self.malen = malen

    def interaction_objects(self):
        if self.gamer.shot and self.malen.shotgun_shot_animation_trigger:
            for obj in sorted(self.sprites.list_of_sprites, key=lambda obj: obj.dist_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.dead != 'immortal' and not obj.dead:
                        if ray_casting_npc_player(obj.x, obj.y, txt_map, self.gamer.pos):
                            obj.dead = True
                            obj.blocked = None
                            self.malen.shotgun_shot_animation_trigger = False
                    break

    def npc_action(self):
        for obj in self.sprites.list_of_sprites:
            if obj.tp == 'enemy' and not obj.dead:
                if ray_casting_npc_player(obj.x, obj.y, txt_map, self.gamer.pos):
                    obj.is_trigger = True
                else:
                    obj.is_trigger = False


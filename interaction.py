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
        self.pain_sound = pygame.mixer.Sound('sound/pain.ogg')

    def interaction_objects(self):
        if self.gamer.shot and self.malen.shotgun_shot_animation_trigger:
            for obj in sorted(self.sprites.list_of_sprites, key=lambda obj: obj.dist_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.dead != 'immortal' and not obj.dead:
                        if ray_casting_npc_player(obj.x, obj.y, txt_map, self.gamer.pos):
                            if obj.tp == 'enemy':
                                self.pain_sound.play()
                            obj.dead = True
                            obj.blocked = None
                            self.malen.shotgun_shot_animation_trigger = False
                    break

    def npc_action(self):
        for obj in self.sprites.list_of_sprites:
            if obj.tp == 'enemy' and not obj.dead:
                if ray_casting_npc_player(obj.x, obj.y, txt_map, self.gamer.pos):
                    obj.is_trigger = True
                    self.npc_move(obj)
                else:
                    obj.is_trigger = False

    def npc_move(self, obj):
        if abs(obj.dist_to_sprite) > CELL:
            dx = obj.x - self.gamer.pos[0]
            dy = obj.y - self.gamer.pos[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('sound/theme.ogg')
        pygame.mixer.music.play(10)



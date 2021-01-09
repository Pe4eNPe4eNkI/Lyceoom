import random
import os
import math
import pygame
from parameters import *
from collections import deque
from r_c import mapping
from numba.core import types
from numba.typed import Dict
from numba import int32


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Sprites:
    def __init__(self):
        self.list_of_sprites = [AllSprites(Barrel(), (9.1, 4)),  # карта №1
                                AllSprites(DoorH(), (10.96, 2.55)),
                                AllSprites(NextDoorFirst(), (22.8, 7.55)),
                                AllSprites(NextDoorSecond(), (46.27, 7.55)),
                                AllSprites(DoorV(), (1.5, 8.55)),
                                AllSprites(Human1(), (7.1, 2.1)),
                                AllSprites(Pinky(), (7.31, 5.88)),
                                AllSprites(Fire(), (8.31, 7.88)),
                                AllSprites(MedKit(), (4.53, 9.1)),
                                AllSprites(Sosademon(), (8.54, 14.45))]
        self.list_of_sprites_2 = [AllSprites(Human1(), (36.61, 5.37)),
                                  AllSprites(Pinky(), (25.76, 4.74)),
                                  AllSprites(MedKit(), (32.02, 7.1)),
                                  AllSprites(Sosademon(), (25.74, 6.25))]
        self.list_of_sprites_3 = [AllSprites(Human2(), (47.41, 1.37)),
                                  AllSprites(Pinky(), (58.8, 2.45)),
                                  AllSprites(MedKit(), (56.8, 13.6)),
                                  AllSprites(Sosademon(), (49.24, 8.96))]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_sprites
                    + self.list_of_sprites_2
                    + self.list_of_sprites_3], default=(float('inf'), 0))

    @property
    def b_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in self.list_of_sprites:
            if obj.tp == 'h_door' or obj.tp == 'h_nextdoor_first' or \
                obj.tp == 'h_nextdoor_second' and obj.blocked:
                    i, j = mapping(obj.x, obj.y)
                    blocked_doors[(i, j)] = 0
        return blocked_doors

    def delete_dead_mobs(self):
        deleted_lst = self.list_of_sprites[:]
        for obj in deleted_lst: 
            if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter') and obj.dead:
                if pygame.time.get_ticks() - obj.time >= 3000:
                    self.list_of_sprites.remove(obj)
        deleted_lst = self.list_of_sprites_2[:]
        for obj in deleted_lst: 
            if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter') and obj.dead:
                if pygame.time.get_ticks() - obj.time >= 3000:
                    self.list_of_sprites_2.remove(obj)
        deleted_lst = self.list_of_sprites_3[:]
        for obj in deleted_lst:
            if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter') and obj.dead:
                if pygame.time.get_ticks() - obj.time >= 3000:
                    self.list_of_sprites_3.remove(obj)



class AllSprites:
    def __init__(self, kind, pos):
        self.obj = kind.way.copy()
        self.viewing_angles = kind.viewing_angles
        self.shift = kind.shift
        self.scale = kind.scale
        self.animation = kind.animation.copy()
        self.animation_dist = kind.animation_dist
        self.animation_speed = kind.animation_speed
        self.time = None
        self.dead_anim = kind.dead_anim.copy()
        self.dead = kind.dead
        self.dead_shift = kind.dead_shift
        self.dead_anim_count = 0

        self.x, self.y = pos[0] * CELL, pos[1] * CELL
        self.tp = kind.tp
        self.blocked = kind.blocked
        self.animation_count = 0
        self.side = kind.side
        self.is_trigger = False
        self.d_open_trigger = False
        self.d_last_pos = self.y if self.tp == 'h_door' \
                                    or self.tp == 'h_nextdoor_first' or \
                                        self.tp == 'h_nextdoor_second' else self.x
        self.cls = False
        self.obj_action = kind.obj_action.copy()

        if self.viewing_angles:
            if len(self.obj) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}

    @property
    def is_on_fire(self):
        if C_RAY - self.side // 2 < self.current_ray < C_RAY + self.side // 2 and self.blocked:
            return self.dist_to_sprite, self.p_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, gamer, walls):
        fake_walls0 = [walls[0] for i in range(100)]
        fake_walls1 = [walls[-1] for i in range(100)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - gamer.x, self.y - gamer.y
        self.dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        self.betta = math.atan2(dy, dx)
        gamma = self.betta - gamer.angle
        if dx > 0 and 180 <= math.degrees(gamer.angle) <= 360 or dx < 0 and dy < 0:
            gamma += ZWEI_PI
        self.betta -= 1.4 * gamma

        d_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = C_RAY + d_rays

        if self.tp not in {'h_door', 'v_door', 'h_nextdoor_first', 'h_nextdoor_second'}:
            if abs(math.cos(H_FOV - self.current_ray * DELTA_ANGLE)) >= 0.5:
                self.dist_to_sprite *= math.cos(H_FOV - self.current_ray * DELTA_ANGLE)
            
        fake_ray = self.current_ray + 100
        if 0 <= fake_ray <= N_RAYS - 1 + 2 * 100 and self.dist_to_sprite > 30:
            self.p_height = min(int(PROJ_C
                                    / self.dist_to_sprite),
                                D_HEIGHT if self.tp
                                            not in {'h_door', 'v_door', 'h_nextdoor_first',
                                                    'h_nextdoor_second'} else HEIGHT)

            sprite_width = int(self.p_height * self.scale[0])
            sprite_heigth = int(self.p_height * self.scale[1])
            h_s_width = sprite_width // 2
            h_s_height = sprite_heigth // 2
            shift = h_s_height * self.shift

            if self.tp in {'h_door', 'v_door', 'h_nextdoor_first', 'h_nextdoor_second'}:
                if self.d_open_trigger:
                    self.d_open()
                self.obj = self.show_sprite()
                sprite_object = self.s_animation()
            else:
                if self.dead and self.dead != 'never':
                    sprite_object = self.dead_animation()
                    shift = h_s_height * self.dead_shift
                    sprite_heigth = int(sprite_heigth / 1.3)
                elif self.is_trigger:
                    sprite_object = self.s_action()
                else:
                    self.obj = self.show_sprite()
                    sprite_object = self.s_animation()

            sprite_pos = (self.current_ray * SCALE - h_s_width, H_HEIGHT - h_s_height + shift)
            if type(sprite_object) == list:
                sprite = pygame.transform.scale(sprite_object[0], (self.p_height, self.p_height))
            else:
                sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_heigth))
            return (self.dist_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def s_animation(self):
        if self.animation and self.dist_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            if len(self.animation) == 1:
                return sprite_object
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.obj

    def show_sprite(self):
        if self.viewing_angles:
            if self.betta < 0:
                self.betta += ZWEI_PI
            self.betta = 360 - int(math.degrees(self.betta))

            for angles in self.sprite_angles:
                if self.betta in angles:
                    return self.sprite_positions[angles]
        return self.obj

    def dead_animation(self):
        if len(self.dead_anim):
            if self.dead_anim_count < self.animation_speed:
                self.d_sprite = self.dead_anim[0]
                self.dead_anim_count += 1
            else:
                self.d_sprite = self.dead_anim.popleft()
                self.dead_anim_count = 0
        return self.d_sprite

    def s_action(self):
        sprite_object = self.animation[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.animation.rotate()
            self.animation_count = 0
        return sprite_object

    def d_open(self):
        if self.tp == 'h_nextdoor_first':
            self.y -= 3
            if abs(self.y - self.d_last_pos) > CELL:
                self.cls = True
        if self.tp == 'h_nextdoor_second':
            self.y -= 3
            if abs(self.y - self.d_last_pos) > CELL:
                self.cls = True
        if self.tp == 'h_door':
            self.y -= 3
            if abs(self.y - self.d_last_pos) > CELL:
                self.cls = True
        elif self.tp == 'v_door':
            self.x -= 3
            if abs(self.x - self.d_last_pos) > CELL:
                self.cls = True


class Fire:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/fire/base/3.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = 0.7
        self.scale = (0.6, 0.6)
        self.side = 30
        self.animation = deque([pygame.image.load(f'data/sprites/fire/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(16)])
        self.animation_dist = 1800
        self.animation_speed = 10
        self.dead = 'never'
        self.dead_shift = 1.8
        self.dead_anim = []
        self.tp = 'fire'
        self.blocked = False
        self.obj_action = []


class Barrel:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/barrel/base/0.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = 1.8
        self.scale = (0.4, 0.4)
        self.side = 30
        self.animation = deque([pygame.image.load(f'data/sprites/'
                                                  f'barrel/anim/{i}.png').convert_alpha() 
                                for i in range(12)])
        self.animation_dist = 150
        self.animation_speed = 5
        self.animation_dist = 1800
        self.animation_speed = 10
        self.dead = None
        self.dead_shift = 2.6
        self.dead_anim = deque([pygame.image.load(f'data/sprites/barrel/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(4)])
        self.tp = 'barrel'
        self.blocked = True
        self.obj_action = []


class Sosademon:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/sosademon/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0
        self.scale = (1, 1)
        self.side = 70
        self.animation = deque([pygame.image.load(f'data/sprites/sosademon/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(6)])
        self.animation_dist = 800
        self.animation_speed = 18
        self.dead = None
        self.dead_shift = 0.5
        self.dead_anim = deque([pygame.image.load(f'data/sprites/sosademon/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(6)])
        self.tp = 'enemy'
        self.blocked = True
        self.obj_action = []

class Pinky:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/pinky/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.2
        self.scale = (0.8, 0.9)
        self.side = 90
        self.animation = deque([pygame.image.load(f'data/sprites/pinky/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 12
        self.dead = None
        self.dead_shift = 0.8
        self.dead_anim = deque([pygame.image.load(f'data/sprites/pinky/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(1, 6)])
        self.tp = 'enemy'
        self.blocked = True
        self.obj_action = []


class Obama:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/obama/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.2
        self.scale = (0.8, 0.9)
        self.side = 90
        self.animation = deque([pygame.image.load(f'data/sprites/obama/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 10
        self.dead = None
        self.dead_shift = 0.8
        self.dead_anim = deque([pygame.image.load(f'data/sprites/obama/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(6)])
        self.tp = 'enemy'
        self.blocked = True
        self.obj_action = []


class Human1:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/human1/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.5
        self.scale = (0.5, 0.8)
        self.side = 30
        self.animation = deque([pygame.image.load(f'data/sprites/human1/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 7
        self.dead = None
        self.dead_shift = 1
        self.dead_anim = deque([pygame.image.load(f'data/sprites/human1/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(5)])
        self.tp = 'enemy_shooter'
        self.blocked = True
        self.obj_action = []


class Human2:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/stas/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.5
        self.scale = (0.6, 0.8)
        self.side = 30
        self.animation = deque([pygame.image.load(f'data/sprites/stas/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 10
        self.dead = None
        self.dead_shift = 1
        self.dead_anim = deque([pygame.image.load(f'data/sprites/stas/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(5)])
        self.tp = 'enemy'
        self.blocked = True
        self.obj_action = []


class DoorH:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha() 
                    for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = CELL
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'h_door'
        self.blocked = True
        self.obj_action = []


class DoorV:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha()
                    for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = CELL
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'v_door'
        self.blocked = True
        self.obj_action = []


class NextDoorFirst:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha()
                    for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = CELL
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'h_nextdoor_first'
        self.blocked = True
        self.obj_action = []


class NextDoorSecond:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha()
                    for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = CELL
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'h_nextdoor_second'
        self.blocked = True
        self.obj_action = []


class MedKit:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/MedKit/base/0.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = -7
        self.scale = (0.1, 0.1)
        self.side = 30
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = None
        self.dead_shift = 0
        self.tp = 'medkit'
        self.dead_anim = []
        self.blocked = False
        self.obj_action = []

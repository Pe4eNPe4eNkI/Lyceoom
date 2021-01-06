from parameters import *
import pygame
import os
import math
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
                                AllSprites(Door(), (10.96, 2.55)),
                                AllSprites(Door(), (2.6, 3.55)),
                                AllSprites(Door(), (22.8, 7.55)),
                                AllSprites(Door(), (25.99, 1.55)),
                                AllSprites(Door(), (38.01, 10.55)),
                                AllSprites(Door(), (39.01, 1.55)),
                                AllSprites(Door(), (46.27, 7.55)),
                                AllSprites(Human1(), (7.1, 2.1)),
                                AllSprites(Human1(), (13.37, 3.31)),
                                AllSprites(Human1(), (8.51, 1.7)),
                                AllSprites(Human1(), (7.26, 1.3)),
                                AllSprites(Human1(), (20.36, 14.76)),
                                AllSprites(Human1(), (7.1, 4.1)),
                                AllSprites(Obama(), (5.1, 2.1)),
                                AllSprites(Obama(), (10.1, 2.1)),
                                AllSprites(Obama(), (1.67, 1.45)),
                                AllSprites(Obama(), (16.94, 1.9)),
                                AllSprites(Obama(), (8.1, 9.1)),
                                AllSprites(Obama(), (16.75, 14.51)),
                                AllSprites(Obama(), (21.5, 9.72)),
                                AllSprites(Pinky(), (7.31, 5.88)),
                                AllSprites(Pinky(), (7.51, 7.68)),
                                AllSprites(Pinky(), (18.68, 14.74)),
                                AllSprites(Pinky(), (8.1, 6.1)),
                                AllSprites(Pinky(), (13.82, 4.62)),
                                AllSprites(Pinky(), (19.72, 1.24)),
                                AllSprites(Sosademon(), (8.54, 14.45)),
                                AllSprites(Sosademon(), (13.44, 11.12)),
                                AllSprites(Sosademon(), (11.72, 14.69)),
                                AllSprites(Sosademon(), (11.74, 6.66)),
                                AllSprites(Sosademon(), (14.84, 6.9)),
                                AllSprites(Sosademon(), (21.71, 11.36)),
                                AllSprites(Human2(), (6.51, 13.43)),
                                AllSprites(Human2(), (18.7, 4.58)),
                                AllSprites(Human2(), (7.78, 11.76)),
                                AllSprites(Human2(), (9.54, 8.15)),
                                AllSprites(Human2(), (8.28, 13.26)),
                                AllSprites(Human1(), (25.74, 6.37)),  # карта №2
                                AllSprites(Human1(), (36.61, 5.37)),
                                AllSprites(Human1(), (41.64, 3.33)),
                                AllSprites(Human1(), (32.74, 14.55)),
                                AllSprites(Human1(), (31.76, 11.25)),
                                AllSprites(Human1(), (34.74, 4.37)),
                                AllSprites(Human1(), (34.74, 5.25)),
                                AllSprites(Sosademon(), (25.74, 6.25)),
                                AllSprites(Sosademon(), (42.58, 4.05)),
                                AllSprites(Sosademon(), (40.01, 5.72)),
                                AllSprites(Sosademon(), (33.24, 13.75)),
                                AllSprites(Sosademon(), (40.37, 7.35)),
                                AllSprites(Sosademon(), (33.26, 14.76)),
                                AllSprites(Sosademon(), (25.68, 1.24)),
                                AllSprites(Sosademon(), (36.44, 3.44)),
                                AllSprites(Pinky(), (25.76, 4.74)),
                                AllSprites(Pinky(), (44.76, 14.76)),
                                AllSprites(Pinky(), (40.38, 13.03)),
                                AllSprites(Pinky(), (30.24, 1.25)),
                                AllSprites(Pinky(), (44.25, 9.81)),
                                AllSprites(Pinky(), (24.5, 13.27)),
                                AllSprites(Pinky(), (30.29, 13.33)),
                                AllSprites(Pinky(), (24.24, 11.75)),
                                AllSprites(Pinky(), (33.47, 1.53)),
                                AllSprites(Obama(), (24.46, 1.5)),
                                AllSprites(Obama(), (35.28, 1.55)),
                                AllSprites(Obama(), (42.26, 13.24)),
                                AllSprites(Obama(), (42.24, 12.52)),
                                AllSprites(Obama(), (31.24, 14.76)),
                                AllSprites(Obama(), (27.48, 13.52)),
                                AllSprites(Obama(), (35.39, 2.33)),
                                AllSprites(Human2(), (34.58, 7.2)),
                                AllSprites(Human2(), (38.7, 1.87)),
                                AllSprites(Human2(), (33.25, 10.24)),
                                AllSprites(Human2(), (29.74, 12.75)),
                                AllSprites(Human2(), (29.23, 14.69)),
                                AllSprites(Human2(), (28.75, 12.4)),
                                AllSprites(Human2(), (47.41, 1.37)),  # карта №3
                                AllSprites(Human2(), (58.65, 2.56)),
                                AllSprites(Human2(), (57.56, 5.86)),
                                AllSprites(Human2(), (57.46, 7.19)),
                                AllSprites(Human2(), (59.45, 7.65)),
                                AllSprites(Human2(), (59.46, 6.31)),
                                AllSprites(Human2(), (49.5, 1.31)),
                                AllSprites(Obama(), (47.24, 3.47)),
                                AllSprites(Obama(), (54.57, 3.34)),
                                AllSprites(Obama(), (51.5, 6.35)),
                                AllSprites(Obama(), (53.83, 5.94)),
                                AllSprites(Obama(), (62.76, 9.74)),
                                AllSprites(Obama(), (58.58, 9.43)),
                                AllSprites(Obama(), (57.75, 9.46)),
                                AllSprites(Obama(), (59.91, 12.68)),
                                AllSprites(Obama(), (56.58, 3.27)),
                                AllSprites(Obama(), (50.46, 7.5)),
                                AllSprites(Pinky(), (58.8, 2.45)),
                                AllSprites(Pinky(), (50.73, 5.74)),
                                AllSprites(Pinky(), (56.74, 3.25)),
                                AllSprites(Pinky(), (48.77, 6.7)),
                                AllSprites(Pinky(), (63.4, 11.82)),
                                AllSprites(Pinky(), (64.76, 14.29)),
                                AllSprites(Pinky(), (57.6, 14.76)),
                                AllSprites(Pinky(), (56.35, 13.46)),
                                AllSprites(Human1(), (49.28, 7.61)),
                                AllSprites(Human1(), (53.35, 1.24)),
                                AllSprites(Sosademon(), (49.24, 8.96)),
                                AllSprites(Sosademon(), (61.69, 6.47)),
                                AllSprites(Sosademon(), (58.16, 14.29)),
                                AllSprites(Sosademon(), (57.35, 11.57)),
                                AllSprites(Sosademon(), (54.71, 12.76)),
                                AllSprites(Sosademon(), (53.26, 13.46)),
                                AllSprites(Sosademon(), (52.66, 14.46)),
                                AllSprites(Sosademon(), (51.76, 12.42)),
                                AllSprites(Sosademon(), (49.42, 12.24)),
                                AllSprites(Sosademon(), (48.76, 14.75)),
                                AllSprites(Sosademon(), (50.72, 13.1)),
                                AllSprites(Sosademon(), (55.04, 7.14)),
                                AllSprites(Sosademon(), (65.28, 5.34)),
                                AllSprites(Sosademon(), (66.72, 7.36)),
                                AllSprites(Sosademon(), (64.66, 9.36)),
                                AllSprites(Sosademon(), (56.24, 1.57)),
                                AllSprites(Sosademon(), (50.97, 1.28)),
                                ]

    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_sprites], default=(float('inf'), 0))

    @property
    def b_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in self.list_of_sprites:
            if obj.tp == 'h_door' or obj.tp == 'v_door' and obj.blocked:
                    i, j = mapping(obj.x, obj.y)
                    blocked_doors[(i, j)] = 0
        return blocked_doors


class AllSprites:
    def __init__(self, kind, pos):
        self.obj = kind.way.copy()
        self.viewing_angles = kind.viewing_angles
        self.shift = kind.shift
        self.scale = kind.scale
        self.animation = kind.animation.copy()
        self.animation_dist = kind.animation_dist
        self.animation_speed = kind.animation_speed

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
        self.d_last_pos = self.y if self.tp == 'h_door' else self.x
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
            #  print(self.sprite_angles)

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

        if self.tp not in {'h_door', 'v_door'}:
            self.dist_to_sprite *= math.cos(H_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + 100
        if 0 <= fake_ray <= N_RAYS - 1 + 2 * 100 and self.dist_to_sprite > 30:
            self.p_height = min(int(PROJ_C / self.dist_to_sprite), D_HEIGHT if self.tp not in {'h_door', 'v_door'} else HEIGHT)

            sprite_width = int(self.p_height * self.scale[0])
            sprite_heigth = int(self.p_height * self.scale[1])
            h_s_width = sprite_width // 2
            h_s_height = sprite_heigth // 2
            shift = h_s_height * self.shift

            if self.tp in {'h_door', 'v_door'}:
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
                                for i in range(1, 16)])
        self.animation_dist = 1800
        self.animation_speed = 10
        self.dead = 'never'
        self.dead_shift = 1.8
        self.dead_anim = deque([pygame.image.load(f'data/sprites/fire/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(6)])
        self.tp = 'object'
        self.blocked = True
        self.obj_action = []

class Barrel:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/barrel/base/0.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = 1.8
        self.scale = (0.4, 0.4)
        self.side = 30
        self.animation = deque([pygame.image.load(f'data/sprites/'
                                                  f'barrel/anim/{i}.png').convert_alpha() for i in range(12)])
        self.animation_dist = 150
        self.animation_speed = 5
        self.animation_dist = 1800
        self.animation_speed = 10
        self.dead = None
        self.dead_shift = 2.6
        self.dead_anim = deque([pygame.image.load(f'data/sprites/barrel/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(4)])
        self.tp = 'object'
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
        self.tp = 'enemy'
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

class Door:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha() for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = 100
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'h_door'
        self.blocked = True
        self.obj_action = []

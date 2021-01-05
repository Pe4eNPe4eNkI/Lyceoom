from parameters import *
import pygame
import os
import math
from collections import deque


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
        self.new_types = {
            'fire': {
                'way': pygame.image.load('data/sprites/fire/base/3.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque([pygame.image.load(f'data/sprites/fire/action/{i}.png').convert_alpha()
                                    for i in range(1, 16)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': False
            },
            'sosademon': {
                'way': [pygame.image.load(f'data/sprites/sosademon/base/{i}.png').convert_alpha() for i in range(8)],
                'viewing_angles': True,
                'shift': 0,
                'scale': (1.1, 1.1),
                'animation': deque([pygame.image.load(f'data/sprites/sosademon/action/{i}.png').convert_alpha()
                                    for i in range(6)]),
                'animation_dist': None,
                'animation_speed': 10,
                'blocked': True
            },
            'barrel': {
                'way': pygame.image.load('data/sprites/barrel/base/0.png').convert_alpha(),
                'viewing_angles': False,
                'shift': 1.8,
                'scale': 0.4,
                'animation': None,
                'animation_dist': 150,
                'animation_speed': 5,
                'blocked': True
            },
            'pinky': {
                'way': pygame.image.load('data/sprites/pinky/base/0.png').convert_alpha(),
                'viewing_angles': True,
                'shift': 0,
                'scale': (0.9, 1.0),
                'animation': deque([pygame.image.load(f'data/sprites/pinky/action/{i}.png').convert_alpha()
                                    for i in range(4)]),
                'animation_dist': 1,
                'animation_speed': 8,
                'blocked': True
                }
        }

        #self.list_of_sprites = [AllSprites(self.new_types['fire'], (7.1, 2.1)),
        #                        AllSprites(self.new_types['fire'], (7.1, 4.1)),
        #                        AllSprites(self.new_types['fire'], (5.1, 2.1)),
        #                        AllSprites(self.new_types['fire'], (10.1, 2.1)),
        #                        AllSprites(self.new_types['fire'], (7.1, 5.1)),
        #                        AllSprites(self.new_types['barrel'], (8.1, 9.1)),
        #                        AllSprites(self.new_types['sosademon'], (5.51, 12.43))]

        self.list_of_sprites = [AllSprites(Fire(), (7.1, 2.1)),
                                AllSprites(Fire(), (7.1, 4.1)),
                                AllSprites(Pinky(), (5.1, 2.1)),
                                AllSprites(Obama(), (10.1, 2.1)),
                                AllSprites(Pinky(), (8.1, 6.1)),
                                AllSprites(Obama(), (8.1, 9.1)),
                                AllSprites(Sosademon(), (5.51, 12.43))]
    @property
    def sprite_shot(self):
        return min([obj.is_on_fire for obj in self.list_of_sprites], default=(float('inf')))


class AllSprites:
    def __init__(self, kind, pos):
        self.obj = kind.way
        self.viewing_angles = kind.viewing_angles
        self.shift = kind.shift
        self.scale = kind.scale
        self.animation = kind.animation
        self.animation_dist = kind.animation_dist
        self.animation_speed = kind.animation_speed
        self.blocked = kind.blocked
        self.animation_count = 0
        self.side = 30
        self.x, self.y = pos[0] * CELL, pos[1] * CELL

        if self.viewing_angles:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}
            print(self.sprite_angles)

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
        d_rays = int(gamma / DELTA_ANGLE)
        self.current_ray = C_RAY + d_rays
        self.dist_to_sprite *= math.cos(H_FOV - self.current_ray * DELTA_ANGLE)

        fake_ray = self.current_ray + 100
        if 0 <= fake_ray <= N_RAYS - 1 + 2 * 100 and self.dist_to_sprite > 30:
            self.p_height = min(int(PROJ_C / self.dist_to_sprite * self.scale), D_HEIGHT)
            h_p_height = self.p_height // 2
            shift = h_p_height * self.shift

            if self.viewing_angles:
                if self.betta < 0:
                    self.betta += ZWEI_PI
                self.betta = 360 - int(math.degrees(self.betta))

                for angles in self.sprite_angles:
                    if self.betta in angles:
                        self.obj = self.sprite_positions[angles]
                        break

            sprite_object = self.obj
            if self.animation and self.dist_to_sprite < self.animation_dist:
                sprite_object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0
            sprite_pos = (self.current_ray * SCALE - h_p_height, H_HEIGHT - h_p_height + shift)
            if type(sprite_object) == list:
                sprite = pygame.transform.scale(sprite_object[0], (self.p_height, self.p_height))
            else:
                sprite = pygame.transform.scale(sprite_object, (self.p_height, self.p_height))
            return (self.dist_to_sprite, sprite, sprite_pos)
        else:
            return (False,)


class Fire:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/fire/base/3.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = 0.7
        self.scale = 0.6
        self.animation = deque([pygame.image.load(f'data/sprites/fire/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(1, 16)])
        self.animation_dist = 800
        self.animation_speed = 10
        self.blocked = False
                                

class Sosademon:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/sosademon/base/{i}.png').convert_alpha() 
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0
        self.scale = 1
        self.animation = deque([pygame.image.load(f'data/sprites/sosademon/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(6)])
        self.animation_dist = 800
        self.animation_speed = 18
        self.blocked = True


class Pinky:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/pinky/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.2
        self.scale = 0.9
        self.animation = deque([pygame.image.load(f'data/sprites/pinky/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 12
        self.blocked = True


class Obama:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/obama/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.2
        self.scale = 0.9
        self.animation = deque([pygame.image.load(f'data/sprites/obama/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 10
        self.blocked = True


class Barrel:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/barrel/base/0.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = 1.8
        self.scale = 0.4
        self.animation = None
        self.animation_dist = 150
        self.animation_speed = 5
        self.blocked = True
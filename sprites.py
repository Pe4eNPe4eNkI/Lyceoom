from parameters import *
import pygame
import os
import math


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
        self.types = {'barrel': pygame.image.load('data/sprites/0.png').convert_alpha(),
                      'fire': pygame.image.load('data/sprites/2.png').convert_alpha(),
                      'sosademon': [pygame.image.load(f'data/sprites/' + \
                                                      f'sosademon/base/{i}.png').convert_alpha() 
                                    for i in range(8)]}

        self.list_of_sprites = [AllSprites(self.types['barrel'], True, (7.1, 2.1), 1.8, 0.4),
                                AllSprites(self.types['barrel'], True, (14.62, 1.31), 1.8, 0.4),
                                AllSprites(self.types['barrel'], True, (21.38, 7.8), 1.8, 0.4),
                                AllSprites(self.types['barrel'], True, (21.37, 8.95), 1.8, 0.4),
                                AllSprites(self.types['fire'], True, (5.9, 2.1), 0.7, 0.6),
                                AllSprites(self.types['fire'], True, (16.47, 4.31), 0.7, 0.6),
                                AllSprites(self.types['fire'], True, (14.27, 3.5), 0.7, 0.6),
                                AllSprites(self.types['fire'], True, (9.41, 4.8), 0.7, 0.6),
                                AllSprites(self.types['sosademon'], False, (5.51, 12.43), 0, 1)]


class AllSprites:
    def __init__(self, obj, static,  pos, shift, scale):
        self.obj = obj
        self.static = static
        self.shift = shift
        self.scale = scale
        self.pos = self.x, self.y = pos[0] * CELL, pos[1] * CELL

        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}

    def object_locate(self, gamer, walls):
        fake_walls0 = [walls[0] for i in range(100)]
        fake_walls1 = [walls[-1] for i in range(100)]
        fake_walls = fake_walls0 + walls + fake_walls1

        dx, dy = self.x - gamer.x, self.y - gamer.y
        dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        betta = math.atan2(dy, dx)
        gamma = betta - gamer.angle
        if dx > 0 and 180 <= math.degrees(gamer.angle) <= 360 or dx < 0 and dy < 0:
            gamma += ZWEI_PI
        d_rays = int(gamma / DELTA_ANGLE)
        current_ray = C_RAY + d_rays
        dist_to_sprite *= math.cos(H_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + 100
        if 0 <= fake_ray <= N_RAYS - 1 + 2 * 100 and dist_to_sprite > 30:
            p_height = min(int(PROJ_C / dist_to_sprite * self.scale), D_HEIGHT)
            h_p_height = p_height // 2
            shift = h_p_height * self.shift

            if not self.static:
                if betta < 0:
                    betta += ZWEI_PI
                betta = 360 - int(math.degrees(betta))

                for angles in self.sprite_angles:
                    if betta in angles:
                        self.obj = self.sprite_positions[angles]
                        break

            sprite_pos = (current_ray * SCALE - h_p_height, H_HEIGHT - h_p_height + shift)
            sprite = pygame.transform.scale(self.obj, (p_height, p_height))
            return (dist_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

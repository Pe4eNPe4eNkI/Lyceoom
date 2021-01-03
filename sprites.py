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
        self.types =  {'barrel': pygame.image.load('data/sprites/0.png'),
                       'fire': pygame.image.load('data/sprites/2.png')}
        self.list_of_sprites = [AllSprites(self.types['barrel'], True,
                                1.8, (1214, 142), 0.8),
                                AllSprites(self.types['fire'], True, 1.8, (1200, 120), 0.8)]


class AllSprites:
    def __init__(self, obj, static, shift, pos, scale):
        self.obj = obj
        self.static = static
        self.shift = shift
        self.scale = scale
        self.pos = self.x, self.y = pos[0] * CELL, pos[1] * CELL

        if not static:
            self.sprite_angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}

    def object_locate(self, gamer, walls):
        fake_wall0 = [walls[0] for _ in range(100)]
        fake_wall1 = [walls[-1] for _ in range(100)]
        fake_walls = fake_wall0 + walls + fake_wall1

        dx, dy = self.x - gamer.x, self.y - gamer.y
        dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        betta = math.atan2(dx, dy)
        gamma = betta - gamer.angle
        if dx > 0 and 180 <= math.degrees(gamer.angle) <= 360 or dx < 0 and dy < 0:
            gamma += ZWEI_PI
        d_rays = int(gamma / DELTA_ANGLE)
        current_ray = C_RAY + d_rays
        dist_to_sprite *= math.cos(H_FOV - current_ray * DELTA_ANGLE)

        fake_ray = current_ray + 100
        if 0 <= fake_ray <= N_RAYS - 1 + 2 * 100 and dist_to_sprite < fake_walls[fake_ray][0]:
            p_height = int(PROJ_C / dist_to_sprite * self.scale)
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
            print('ass')
            return (False,)
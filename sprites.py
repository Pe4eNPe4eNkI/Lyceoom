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


class AllSprites:
    def __init__(self, obj, static, pos, shift, scale):
        self.obj = obj
        self.static = static
        self.pos = self.x, self.y = pos[0] * CELL, pos[1] * CELL
        self.shift = shift
        self.scale = scale

    def object_locate(self, gamer, walls):
        dx, dy = self.x - gamer.x, self.y - gamer.y
        dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        betta = math.atan2(dx, dy)
        gamma = betta - gamer.angle
        if dx > 0 and 180 <= math.degrees(gamer.angle) <= 360 or dx < 0 and dy < 0:
            gamma += ZWEI_PI
        d_rays = int(gamma / DELTA_ANGLE)
        current_ray = C_RAY + d_rays
        dist_to_sprite *= math.cos(H_FOV - current_ray * DELTA_ANGLE)

        if 0 <= current_ray <= N_RAYS - 1 and dist_to_sprite < walls[current_ray][0]:
            p_height = int(PROJ_C / dist_to_sprite * self.scale)
            h_p_height = p_height // 2
            shift = h_p_height * self.shift
            sprite_pos = (current_ray * SCALE - h_p_height, H_HEIGHT - h_p_height + shift)
            sprite = pygame.transform.scale(self.obj, (p_height, p_height))
            return (dist_to_sprite, sprite, sprite_pos)
        return (False,)


class Fire:
    def __init__(self):
        # super().__init__(all_sprites)
        self.image = pygame.image.load('data/sprites/0.png')
        self.look_angle = None
        self.shift = 0.7
        self.scale = (0.6, 0.6)
        self.side = 30
        self.is_dead = None
        self.mission = 'decor'



all_sprites = pygame.sprite.Group()
fire_sprite = Fire()
list_of_sprites = [AllSprites(fire_sprite, True, (602, 397), 0.7, 0.8), 
                   AllSprites(fire_sprite, True, (598, 400), 1.8, 0.4),
                   AllSprites(fire_sprite, True, (9.47, 2.1), 1.8, 0.4),
                   AllSprites(fire_sprite, True, (10.21, 2.1), 1.8, 0.4),
                   AllSprites(fire_sprite, True, (142.1, 2.1), 1.8, 0.4),
                   AllSprites(fire_sprite, True, (14.1, 2.1), 1.8, 0.4),
                   AllSprites(fire_sprite, True, (36.1, 2.1), 1.8, 0.4)]

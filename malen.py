import pygame
from parameters import *
from r_c import ray_casting
from map import mini_map
from collections import deque


class Malen:
    def __init__(self, monitor, monitor_map, gamer):
        self.monitor = monitor
        self.monitor_map = monitor_map
        self.gamer = gamer
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.texture = {1: pygame.image.load('data/text/wall/wall3.png').convert(),
                        2: pygame.image.load('data/text/wall/wall7.png').convert(),
                        3: pygame.image.load('data/text/wall/wall1.png').convert(),
                        4: pygame.image.load('data/text/wall/wall2.png').convert(),
                        'S': pygame.image.load('data/text/sky/sky1.png').convert(),
                        'F': pygame.image.load('data/text/down/down.png').convert()
                        }
        #Пушки
        self.shotgun_base_sprite = pygame.image.load('data/sprites/weapons/shot-gun/base/1.png').convert_alpha()
        self.shotgun_shot_animation = deque([pygame.image.load(f'data/sprites/weapons/shot-gun/'
                                                            f'shot1/{i}.png').convert_alpha() for i in range(14)])
        self.shotgun_rect = self.shotgun_base_sprite.get_rect()
        self.shotgun_pos = (H_WIDTH - self.shotgun_rect.width // 2, HEIGHT - self.shotgun_rect.height)
        self.shotgun_shot_length = len(self.shotgun_shot_animation)
        self.shotgun_shot_length_count = 0
        self.shotgun_shot_animation_speed = 3
        self.shotgun_shot_animation_count = 0
        self.shotgun_shot_animation_trigger = True

    def bg(self, angle):
        sky_offset = -5 * math.degrees(angle) % WIDTH
        self.monitor.blit(self.texture['S'], (sky_offset, 0))
        self.monitor.blit(self.texture['S'], (sky_offset - WIDTH, 0))
        self.monitor.blit(self.texture['S'], (sky_offset + WIDTH, 0))

        pygame.draw.rect(self.monitor, DARKGREY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, ob, ob_pos = obj
                self.monitor.blit(ob, ob_pos)

    def fps(self, clock):
        fps_clock = str(int(clock.get_fps()))
        render = self.font.render(fps_clock, 0, RED)
        self.monitor.blit(render, FPS_POS)

    def mini_map(self, gamer):
        self.monitor_map.fill(BLACK)
        map_x, map_y = self.gamer.x // MAP_SCALE, self.gamer.y // MAP_SCALE
        pygame.draw.line(self.monitor_map, YELLOW, (map_x, map_y), (map_x + 4 * math.cos(self.gamer.angle),
                                                                    map_y + 4 * math.sin(self.gamer.angle)), 2)
        pygame.draw.circle(self.monitor_map, RED, (int(map_x), int(map_y)), 4)

        for x, y in mini_map:
            pygame.draw.rect(self.monitor_map, DARKORANGE, (x, y, MAP_CELL, MAP_CELL), 2)
        self.monitor.blit(self.monitor_map, MAP_POS)

    def player_weapon_shotgun(self):
        if self.gamer.shot:
            shotgun_shot_sprite = self.shotgun_shot_animation[0]
            self.monitor.blit(shotgun_shot_sprite, self.shotgun_pos)
            self.shotgun_shot_animation_count += 1
            if self.shotgun_shot_animation_count == self.shotgun_shot_animation_speed:
                self.shotgun_shot_animation.rotate(-1)
                self.shotgun_shot_animation_count = 0
                self.shotgun_shot_length_count += 1
                self.shotgun_shot_animation_trigger = False
            if self.shotgun_shot_length_count == self.shotgun_shot_length:
                self.gamer.shot = False
                self.shotgun_shot_length_count = 0
                self.shotgun_shot_animation_trigger = True
        else:
            self.monitor.blit(self.shotgun_base_sprite, self.shotgun_pos)
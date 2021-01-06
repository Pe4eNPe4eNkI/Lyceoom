import pygame
from parameters import *
from r_c import ray_casting
#from new_map import mini_map
from map import mini_map
from collections import deque


class Malen:
    def __init__(self, monitor, monitor_map, gamer):
        self.monitor = monitor
        self.monitor_map = monitor_map
        self.gamer = gamer
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.texture = {1: pygame.image.load('data/img/lvl1/wall11.png').convert(),
                        2: pygame.image.load('data/img/lvl1/wall8.png').convert(),
                        3: pygame.image.load('data/img/lvl1/wall9.png').convert(),
                        4: pygame.image.load('data/img/lvl1/wall10.png').convert(),
                        'S': pygame.image.load('data/img/lvl1/sk1.jpeg').convert(),
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
        self.shotgun_shot_animation_speed = 5
        self.shotgun_shot_animation_count = 0
        self.shotgun_shot_animation_trigger = True
        self.shotgun_shot_sound = pygame.mixer.Sound('sound/shotgun.ogg')
        #sfx
        self.sfx = deque([pygame.image.load(f'data/sprites/'
                                            f'shoot_sfx/action/{i}.png').convert_alpha() for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

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

    def mini_map(self):
        self.monitor_map.fill(BLACK)
        xmap, ymap = self.gamer.x // MAP_SCALE, self.gamer.y // MAP_SCALE
        pygame.draw.line(self.monitor_map, YELLOW, (xmap, ymap), (xmap + 4 * math.cos(self.gamer.angle),
                                                                    ymap + 4 * math.sin(self.gamer.angle)), 2)
        pygame.draw.circle(self.monitor_map, RED, (int(xmap), int(ymap)), 4)

        for x, y in mini_map:
            pygame.draw.rect(self.monitor_map, DARKORANGE, (x, y, MAP_CELL, MAP_CELL), 2)
        self.monitor.blit(self.monitor_map, MAP_POS)

    def player_weapon_shotgun(self, shots):
        if self.gamer.shot:
            if not self.shotgun_shot_length_count:
                self.shotgun_shot_sound.play()
            self.shot_projection = int(min(shots)[1] // 2)
            self.bullet_sfx()
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
                self.sfx_length_count = 0
                self.shotgun_shot_animation_trigger = True
        else:
            self.monitor.blit(self.shotgun_base_sprite, self.shotgun_pos)

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.monitor.blit(sfx, (H_WIDTH - sfx_rect.w // 2, H_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)
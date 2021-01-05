import pygame
import sys
import math
from parameters import *
from map import collision_walls


def terminate():
    pygame.quit()
    sys.exit()


class Gamer:
    def __init__(self, sprites):
        self.x, self.y = 908, 142
        self.angle = gamer_angle
        self.sensitivity = 0.002
        # Параметры игрока для того, чтобы не ходить сквозь объекты
        self.sprites = sprites
        self.collision_sprites = [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in
                                  self.sprites.list_of_sprites if obj.blocked]
        self.collision_list = collision_walls + self.collision_sprites
        # Параметры игрока для того, чтобы не ходить сквозь стены
        self.side = 50
        self.rect = pygame.Rect(*gamer_pos, self.side, self.side)

    @property
    def pos(self):
        print(self.x, self.y)
        return (self.x, self.y)

    def detect_collision(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(self.collision_list)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = self.collision_list[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_x < delta_y:
                dx = 0
        self.x += dx
        self.y += dy

    def keys_check(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            terminate()
        if keys[pygame.K_w]:
            dx = gamer_speed * cos_a
            dy = gamer_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = -gamer_speed * cos_a
            dy = -gamer_speed * sin_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = gamer_speed * sin_a
            dy = -gamer_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = -gamer_speed * sin_a
            dy = gamer_speed * cos_a
            self.detect_collision(dx, dy)
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

    def movement(self):
        self.keys_check()
        self.mouse_verific()
        self.rect.center = self.x, self.y
        self.angle %= ZWEI_PI

    def mouse_verific(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - H_WIDTH
            pygame.mouse.set_pos((H_WIDTH, H_HEIGHT))
            self.angle += diff * self.sensitivity

# tests
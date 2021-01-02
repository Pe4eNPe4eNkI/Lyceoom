import pygame
import sys
import math
from parameters import *


def terminate():
    pygame.quit()
    sys.exit()


class Gamer:
    def __init__(self):
        self.x, self.y = gamer_pos
        self.angle = gamer_angle
        self.sensitivity = 0.004

    @property
    def pos(self):
        return (self.x, self.y)

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            terminate()
        if keys[pygame.K_w]:
            self.x += gamer_speed * cos_a
            self.y += gamer_speed * sin_a
        if keys[pygame.K_s]:
            self.x += -gamer_speed * cos_a
            self.y += -gamer_speed * sin_a
        if keys[pygame.K_a]:
            self.x += gamer_speed * sin_a
            self.y += -gamer_speed * cos_a
        if keys[pygame.K_d]:
            self.x += -gamer_speed * sin_a
            self.y += gamer_speed * cos_a
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
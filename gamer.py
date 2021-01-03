import pygame
import sys
import math
from parameters import *


def terminate():
    pygame.quit()
    sys.exit()


class Gamer:
    def __init__(self):
        self.x, self.y = 908, 142
        self.angle = gamer_angle
        self.sensitivity = 0.0008

    @property
    def pos(self):
        #  print(self.x, self.y)
        return (self.x, self.y)

    def keys_check(self):
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
        
    def movement(self):
        self.keys_check()
        self.mouse_verific()
        self.angle %= ZWEI_PI

    def mouse_verific(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - H_WIDTH
            pygame.mouse.set_pos((H_WIDTH, H_HEIGHT))
            self.angle += diff * self.sensitivity
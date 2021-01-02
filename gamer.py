import pygame
from parameters import *
from main import terminate


class Gamer:
    def __init__(self):
        self.x, self.y = gamer_pos
        self.angle = gamer_angle
        self.sensitivity = 0.004

    def pos(self):
        return (self.x, self.y)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            terminate()
        if keys[pygame.K_w]:
            self.y -= gamer_speed
        if keys[pygame.K_s]:
            self.y += gamer_speed
        if keys[pygame.K_a]:
            self.x -= gamer_speed
        if keys[pygame.K_d]:
            self.x += gamer_speed
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02
        
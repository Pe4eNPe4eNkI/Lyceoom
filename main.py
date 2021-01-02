import pygame
import sys
import math
from parameters import *
from gamer import Gamer
from map import txt_map
from r_c import ray_casting
from malen import Malen


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
monitor = pygame.display.set_mode((WIDTH, HEIGHT))
mon_map = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
timer = pygame.time.Clock()
gamer = Gamer()
malen = Malen(monitor, mon_map)

while True:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            terminate()
    gamer.movement()
    monitor.fill(BLACK)
    malen.bg()
    malen.world(gamer.pos, gamer.angle)
    malen.fps(timer)
    malen.mini_map(gamer)

    pygame.display.flip()
    timer.tick(FPS)

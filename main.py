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
timer = pygame.time.Clock()
gamer = Gamer()
malen = Malen(monitor)

while True:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            terminate()
    gamer.movement()
    monitor.fill(BLACK)
    malen.bg()
    malen.world(player.pos, player.angle)
    malen.fps(clock)
    '''pygame.draw.rect(monitor, BLUE, (0, 0, WIDTH, H_HEIGHT))
    pygame.draw.rect(monitor, DARKGREY, (0, H_HEIGHT, WIDTH, H_HEIGHT))'''


    ray_casting(monitor, gamer.pos, gamer.angle)

    '''pygame.draw.circle(monitor, RED, (int(gamer.x), int(gamer.y)), 12)
    pygame.draw.line(monitor, RED, gamer.pos,
                     (gamer.x + WIDTH * math.cos(gamer.angle), gamer.y + WIDTH * math.sin(gamer.angle)))

    # отрисовка карты

    for x, y in txt_map:
        pygame.draw.rect(monitor, DARKGREY, (x, y, CELL, CELL), 2)'''



    pygame.display.flip()
    timer.tick(FPS)

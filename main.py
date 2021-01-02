import pygame
import sys
import math
from parameters import *
from gamer import Gamer
from map import txt_map


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
monitor = pygame.display.set_mode((WIDTH, HEIGHT))
timer = pygame.time.Clock()
gamer = Gamer()

while True:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            terminate()
    gamer.movement()
    monitor.fill(BLACK)

    pygame.draw.circle(monitor, RED, gamer.pos, 12)
    pygame.draw.line(monitor, RED, gamer.pos,
                     (gamer.x + WIDTH * math.cos(gamer.angle), gamer.y + WIDTH * math.sin(gamer.angle)))


#отрисовка карты

    for x, y in txt_map:
        pygame.draw.rect(monitor, DARKGREY, (x, y, CELL, CELL), 2)

    pygame.display.flip()
    timer.tick(FPS)

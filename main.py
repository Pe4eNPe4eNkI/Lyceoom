import pygame
import sys
from parameters import *
from gamer import Gamer


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

    pygame.display.flip()
    timer.tick(FPS)
import pygame
from parameters import *
from gamer import Gamer


pygame.init()
monitor = pygame.display.set_mode((WIDHT, HIGHT))
timer = pygame.time.Clock()
gamer = Gamer()

while True:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            exit()
    gamer.movement()
    monitor.fill(BLACK)

    pygame.draw.rect(monitor, RED, (gamer.pos[0], gamer.pos[1], 6, 6))

    pygame.display.flip()
    timer.tick(FPS)

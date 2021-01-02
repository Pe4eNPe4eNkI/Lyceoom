import pygame
from parameters import *


pygame.init()
monitor = pygame.display.set_mode((WIDHT, HIGHT))
timer = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            exit()
    monitor.fill(BLACK)

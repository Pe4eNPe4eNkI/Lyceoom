import pygame
import sys
from parameters import *
from gamer import Gamer
from sprites import *
from r_c import walls_with_ray_cast
from malen import Malen


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()
monitor = pygame.display.set_mode((WIDTH, HEIGHT))
mon_map = pygame.Surface(MAP_RES)
pygame.mouse.set_visible(False)
timer = pygame.time.Clock()
sprites = Sprites()
gamer = Gamer(sprites)
malen = Malen(monitor, mon_map, gamer)

while True:
    '''for event in pygame.event.get():
        if pygame.event == pygame.QUIT:
            terminate()'''
    gamer.movement()
    '''monitor.fill(BLACK)'''
    malen.bg(gamer.angle)
    walls = walls_with_ray_cast(gamer, malen.texture)
    malen.world(walls + [obj.object_locate(gamer, walls) for obj in sprites.list_of_sprites])
    malen.fps(timer)
    malen.mini_map(gamer)
    malen.player_weapon_shotgun()

    pygame.display.flip()
    timer.tick(FPS)

# test
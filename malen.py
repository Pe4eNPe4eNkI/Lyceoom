import pygame
from parameters import *
from r_c import ray_casting
from map import mini_map

# для коммита
# еще каммит

class Malen:
    def __init__(self, monitor, monitor_map):
        self.monitor = monitor
        self.monitor_map = monitor_map
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def bg(self):
        pygame.draw.rect(self.monitor, SKY_BLUE, (0, 0, WIDTH, H_HEIGHT))
        pygame.draw.rect(self.monitor, DARKGREY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, gamer_pos, gamer_angle):
        ray_casting(self.monitor, gamer_pos, gamer_angle)

    def fps(self, clock):
        fps_clock = str(int(clock.get_fps()))
        render = self.font.render(fps_clock, 0, RED)
        self.monitor.blit(render, FPS_POS)

    def mini_map(self, gamer):
        self.monitor_map.fill(BLACK)
        map_x, map_y = gamer.x // MAP_SCALE, gamer.y // MAP_SCALE
        pygame.draw.circle(self.monitor_map, RED, (int(map_x), int(map_y)), 4)
        pygame.draw.line(self.monitor_map, YELLOW, (map_x, map_y), (map_x + WIDTH * math.cos(gamer.angle),
                                                                    map_y + WIDTH * math.sin(gamer.angle)), 2)

        for x, y in mini_map:
            pygame.draw.rect(self.monitor_map, DARKBROWN, (x, y, MAP_CELL, MAP_CELL), 2)
        self.monitor.blit(self.monitor_map, MAP_POS)

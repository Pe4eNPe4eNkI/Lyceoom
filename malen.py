import pygame
from parameters import *
from r_c import ray_casting

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
        map_x, map_y = self.gamer.x // MAP_SCALE, self.gamer.y // MAP_SCALE
        pygame.draw.line(self.monitor_map, YELLOW, (map_x, map_y), (map_x + 8 * math.cos(self.gamer.angle),
                                                               map_y + 8 * math.sin(self.gamer.angle)), 2)
        pygame.draw.circle(self.monitor_map, RED, (int(map_x), int(map_y)), 4)
        for x, y in mini_map:
            pygame.draw.rect(self.monitor_map, DARKBROWN, (x, y, MAP_CELL, MAP_CELL))
        self.monitor.blit(self.monitor_map, MAP_POS)
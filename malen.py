import pygame
from parameters import *
from r_c import ray_casting
from map import mini_map


# для коммита
# еще каммит

class Malen:
    def __init__(self, monitor, monitor_map, gamer):
        self.monitor = monitor
        self.monitor_map = monitor_map
        self.gamer = gamer
        self.font = pygame.font.SysFont('Arial', 36, bold=True)
        self.texture = {'1': pygame.image.load('data/text/3.png').convert(),
                        '2': pygame.image.load('data/text/wall7.png').convert(),
                        '3': pygame.image.load('data/text/12.png').convert()
                        }

    def bg(self):
        pygame.draw.rect(self.monitor, SKY_BLUE, (0, 0, WIDTH, H_HEIGHT))
        pygame.draw.rect(self.monitor, DARKGREY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, gamer_pos, gamer_angle):
        ray_casting(self.monitor, gamer_pos, gamer_angle, self.texture)

    def fps(self, clock):
        fps_clock = str(int(clock.get_fps()))
        render = self.font.render(fps_clock, 0, RED)
        self.monitor.blit(render, FPS_POS)

    def mini_map(self, gamer):
        self.monitor_map.fill(BLACK)
        map_x, map_y = self.gamer.x // MAP_SCALE, self.gamer.y // MAP_SCALE
        pygame.draw.line(self.monitor_map, YELLOW, (map_x, map_y), (map_x + 4 * math.cos(self.gamer.angle),
                                                                    map_y + 4 * math.sin(self.gamer.angle)), 2)
        pygame.draw.circle(self.monitor_map, RED, (int(map_x), int(map_y)), 4)

        for x, y in mini_map:
            pygame.draw.rect(self.monitor_map, DARKBROWN, (x, y, MAP_CELL, MAP_CELL), 2)
        self.monitor.blit(self.monitor_map, MAP_POS)

# я спать, всем спокойной ночи (1:39)
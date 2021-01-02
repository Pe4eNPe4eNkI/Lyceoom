import pygame
from parameters import *
from r_c import ray_casting

# для коммита
# еще каммит

class Malen:
    def init(self, monitor):
        self.monitor = monitor
        self.font = pygame.font.SysFont('Arial', 36, bold=True)

    def bg(self):
        pygame.draw.rect(self.monitor, SKY_BLUE, (0, 0, WIDTH, H_HEIGHT))
        pygame.draw.rect(self.monitor, DARKGREY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, gamer_pos, gamer_angle):
        ray_casting(self.monitor, gamer_pos, gamer_angle)

    # update, people, update

    def fps(self, clock):
        fps_clock = str(int(clock.get_fps()))
        render = self.font.render(fps_clock, 0, RED)
        self.monitor.blit(render, FPS_POS)
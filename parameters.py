# здесь хранятся всякие разные константы для остальных файлов проекта
import math

# общие настройки
WIDTH = 1200
HEIGHT = 800
H_HEIGHT = HEIGHT / 2
H_WIDTH = WIDTH / 2
D_HEIGHT = HEIGHT * 2
D_WIDTH = WIDTH * 2
P_HEIGHT = 5 * HEIGHT
CELL = 100
FPS = 90
FPS_POS = (WIDTH - 65, 5)

# настройки игрока
gamer_pos = (H_WIDTH, H_HEIGHT)
gamer_angle = 0
gamer_speed = 2.5

# настройки лучей
FOV = math.pi / 3
H_FOV = FOV / 2
N_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / N_RAYS
DISTANCE = N_RAYS / (2 * math.tan(H_FOV))
PROJ_C = 3 * DISTANCE * CELL
SCALE = WIDTH // N_RAYS

# настройки для миникарты

MINIMAP_SCALE = 5
MAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_SCALE = 2 * MINIMAP_SCALE
MAP_CELL = CELL // MAP_SCALE
MAP_POS = (0, 0)

# текстуры
T_W = 1200
T_H = 1200
T_SCALE = T_W // CELL

# спрайты
ZWEI_PI = math.pi * 2
C_RAY = N_RAYS // 2 - 1  # аоаоаоаоа

# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 80, 0)
BLUE = (0, 0, 220)
DARKGREY = (61, 61, 61)
DARKBROWN = (63, 42, 20)
DARKORANGE = (255, 98, 0)
PURPLE = (120, 0, 120)
SKY_BLUE = (0, 180, 255)
YELLOW = (220, 220, 0)
SANDY = (244, 164, 96)

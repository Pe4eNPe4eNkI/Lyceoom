# здесь хранятся всякие разные константы для остальных файлов проекта
import math

# общие настройки
WIDTH = 1200  # ширина 
HEIGHT = 800  # высота 
H_HEIGHT = HEIGHT / 2
H_WIDTH = WIDTH / 2
D_HEIGHT = HEIGHT * 2
D_WIDTH = WIDTH * 2
P_HEIGHT = 5 * HEIGHT
CELL = 100   # длина квадартной клетки поля 
FPS = 90
# ниже позиции счетчиков фпс и хп 
FPS_POS = (WIDTH - 65, 25)
HP_POS = (WIDTH - 100, 650)  
STATUSBAR_POS = (WIDTH - 225, 655)

# настройки игрока
gamer_pos = (124, 753)  # начальные координаты
gamer_angle = 0  # начальный угол поворота
gamer_speed = 4.5  # скорость игрока на протяжении всей игры

# настройки лучей
FOV = math.pi / 3  # угол обзора
H_FOV = FOV / 2  
N_RAYS = 300  # количество лучей для детализации проекций
MAX_DEPTH = 800  # максимальная глубина прорисовки
DELTA_ANGLE = FOV / N_RAYS  # угол между двумя лучами
DISTANCE = N_RAYS / (2 * math.tan(H_FOV))  # прорисовка
PROJ_C = 3 * DISTANCE * CELL  # коэффициент для реалистичности
SCALE = WIDTH // N_RAYS

# настройки для миникарты

MINIMAP_SCALE = 5  # разница миникарты и карты
MAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)  # разрешение миникарты
MAP_SCALE = 2 * MINIMAP_SCALE
MAP_CELL = CELL // MAP_SCALE  # длина клетки на миникарте
MAP_POS = (15, 50)  # позиция миникарты на мониторе

# текстуры
T_W = 1200  # ширина
T_H = 1200  # высота
H_T_H = T_H // 2
T_SCALE = T_W // CELL

# спрайты
ZWEI_PI = math.pi * 2  # удвоенный пи для корректировки углов
C_RAY = N_RAYS // 2 - 1  

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
SPRINGGREEN = (0, 250, 154)
GRAY = (26, 26, 26)

# Импорт необходимых элементов
import pygame
from parameters import *
from numba import njit
from map import txt_map, H_WORLD, W_WORLD


@njit(fastmath=True)
def mapping(a, b):  # Проверка на попадание луча в стену
    return int((a // CELL) * CELL), int((b // CELL) * CELL)


@njit(fastmath=True)
# Алгоритм Брезенхэма
def ray_casting(pos_gamer, angle_gamer, txt_map):  # Функция выдает картинку с помощью рей кастинга
    walls = []
    ox, oy = pos_gamer  # Координаты начала лучей
    texture_v, texture_h = 1, 1
    xm, ym = mapping(ox, oy)
    view_angle = angle_gamer - H_FOV  # Первый угол
    for ray in range(N_RAYS):  # Пробегаемся по всем лучам
        sin_a = math.sin(view_angle)  # Функции направления луча
        sin_a = sin_a if sin_a else 0.000001
        cos_a = math.cos(view_angle)
        cos_a = cos_a if cos_a else 0.000001

        # Проверка на пересечение луча с прямыми (вертикальные)
        x, dx = (xm + CELL, 1) if cos_a >= 0 else (xm, -1)  
        for i in range(0, W_WORLD, CELL):  # Пробегаемся по всем прямым
            depth_v = (x - ox) / cos_a  # Исправление эффекта рыбьего глаза
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in txt_map:
                texture_v = txt_map[tile_v]
                break
            x += dx * CELL

        # Проверка на пересечение луча с прямыми (горизонтальные)
        y, dy = (ym + CELL, 1) if sin_a >= 0 else (ym, -1)  
        for i in range(0, H_WORLD, CELL):  # Пробегаемся по всем прямым
            depth_h = (y - oy) / sin_a  # Исправление эффекта рыбьего глаза
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in txt_map:
                texture_h = txt_map[tile_h]
                break
            y += dy * CELL

        # Выбираем, какая из точе пересечения препятствием ближе и отрисовываем его
        if depth_v < depth_h:  
            depth, offset, texture = (depth_v, yv, texture_v)
        else:
            depth, offset, texture = (depth_h, xh, texture_h)
        offset = int(offset) % CELL
        depth *= math.cos(angle_gamer - view_angle)
        depth = max(depth, 0.00001)
        hight = int(PROJ_C / depth)  # Проекционная высота стены

        walls.append((depth, offset, hight, texture))
        view_angle += DELTA_ANGLE
    return walls


def walls_with_ray_cast(gamer, textures):  # Формирование текстур
    verific_walls = ray_casting(gamer.pos, gamer.angle, txt_map)
    wall_shot = verific_walls[C_RAY][0], verific_walls[C_RAY][2]
    walls = []
    for ray, casted_values in enumerate(verific_walls):  # Прогрузка стен
        depth, offset, hight, texture = casted_values
        if hight > HEIGHT:  # Условие на отображение части стены
            coeff = hight / HEIGHT
            texture_height = T_H / coeff
            wall_c = textures[texture].subsurface(offset * T_SCALE, H_T_H - texture_height // 2,
                                                  T_SCALE, texture_height)
            wall_c = pygame.transform.scale(wall_c, (SCALE, HEIGHT))
            walls_pos = (ray * SCALE, 0)
        else:
            wall_c = textures[texture].subsurface(offset * T_SCALE, 0, T_SCALE, T_H)
            wall_c = pygame.transform.scale(wall_c, (SCALE, hight))
            walls_pos = (ray * SCALE, H_HEIGHT - hight // 2)
        walls.append((depth, wall_c, walls_pos))
    return walls, wall_shot  # Возврат данных
# в этом файле хранится все, что имеет отношение к нашим спрайтам


import os
import pygame
from parameters import *
from collections import deque  # итератор очереди для обработки анимаций
from r_c import mapping
from numba.core import types  # берем типы данных из намбы
from numba.typed import Dict  # берем намбовские словари для хранения карты
from numba import int32  


# функция подгрузки фото из учебника
def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


# класс, в котором хранится список со всеми спрайтами и вспомогательные штуки
class Sprites:
    def __init__(self):
        # список с дверями
        self.list_of_sprites_doors = [AllSprites(DoorH(), (10.96, 2.55)),  # Двери
                                      AllSprites(NextDoorFirst(), (22.8, 7.55)),
                                      AllSprites(NextDoorSecond(), (46.27, 7.55)),
                                      AllSprites(DoorV(), (1.5, 8.55)),
                                      AllSprites(DoorH(), (2.6, 3.55)),
                                      AllSprites(DoorH(), (22.8, 7.55)),
                                      AllSprites(DoorH(), (25.99, 1.55)),
                                      AllSprites(DoorH(), (38.01, 10.55)),
                                      AllSprites(DoorH(), (39.01, 1.55)),
                                      AllSprites(DoorV(), (11.5, 6.55)),
                                      AllSprites(DoorH(), (7.25, 13.5)),
                                      AllSprites(DoorV(), (24.5, 5.43)),
                                      AllSprites(DoorH(), (30.85, 11.5)),
                                      AllSprites(DoorH(), (37.5, 14.5)),
                                      AllSprites(DoorV(), (44.5, 5.55)),
                                      AllSprites(DoorH(), (14.5, 9.5)),
                                      AllSprites(DoorV(), (34.5, 5.5))]
        self.list_of_sprites = [AllSprites(Barrel(), (9.1, 4)),  # карта №1
                                AllSprites(Human1(), (7.1, 2.1)),
                                AllSprites(MedKit(), (21.63, 11.69)),
                                AllSprites(MedKit(), (2.21, 14.58)),
                                AllSprites(Fire(), (8.31, 7.88)),
                                AllSprites(Obama(), (2.27, 1.39)),
                                AllSprites(Pinky(), (8.54, 14.45)),
                                AllSprites(Pinky(), (2.9, 14.66)),
                                AllSprites(Pinky(), (11.95, 8.6)),
                                AllSprites(Obama(), (11.87, 14.05)),
                                AllSprites(Human2(), (16.19, 12.57)),
                                AllSprites(Pinky(), (21.22, 14.21)),
                                AllSprites(Obama(), (15.55, 10.48)),
                                AllSprites(Human1(), (12.03, 1.54)),
                                AllSprites(Obama(), (13.8, 4.62)),
                                AllSprites(Pinky(), (18.93, 4.56)),
                                AllSprites(Human1(), (16.76, 2.02))]
        self.list_of_sprites_2 = [AllSprites(Obama(), (35.39, 2.33)), # карта №2
                                  AllSprites(Pinky(), (27.27, 5.5)),
                                  AllSprites(Obama(), (25.41, 4.31)),
                                  AllSprites(Human2(), (25.43, 1.45)),
                                  AllSprites(Pinky(), (25.59, 14.65)),
                                  AllSprites(MedKit(), (24.54, 13.7)),
                                  AllSprites(Human1(), (31.43, 6.18)),
                                  AllSprites(Pinky(), (30.48, 6.49)),
                                  AllSprites(MedKit(), (24.62, 14.21)),
                                  AllSprites(Obama(), (32.98, 3.72)),
                                  AllSprites(Human2(), (30.63, 13.51)),
                                  AllSprites(Pinky(), (32.56, 14.59)),
                                  AllSprites(Human1(), (37.35, 12.08)),
                                  AllSprites(Human2(), (42.71, 13.74)),
                                  AllSprites(Pinky(), (42.56, 10.91)),
                                  AllSprites(Obama(), (37.37, 6.75)),
                                  AllSprites(Fire(), (32.52, 12.57)),
                                  AllSprites(Fire(), (41.55, 5.59)),
                                  AllSprites(Fire(), (29.82, 4.49)),
                                  AllSprites(Fire(), (24.74, 11.3)),
                                  AllSprites(Barrel(), (28.44, 6.51)),
                                  AllSprites(Barrel(), (27.55, 14.43)),
                                  AllSprites(Barrel(), (38.21, 6.76)),
                                  AllSprites(Barrel(), (41.47, 12.56)),
                                  AllSprites(MedKit(), (41.87, 1.55)),
                                  AllSprites(MedKit(), (39.98, 13.51))]
        # пустая комната с боссом
        self.list_of_sprites_3 = [AllSprites(Sosademon(), (65.21, 15.5))]

    @property
    def sprite_shot(self):  # По кому идет стрельба
        return min([obj.is_on_fire for obj in self.list_of_sprites
                    + self.list_of_sprites_2
                    + self.list_of_sprites_3
                    + self.list_of_sprites_doors], default=(float('inf'), 0))

    @property
    def b_doors(self):  # Функция запрещает видеть через закрытые двери
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in self.list_of_sprites_doors:
            if obj.tp == 'h_door' or obj.tp == 'h_nextdoor_first' or obj.tp == 'h_nextdoor_second' \
                    and obj.blocked:
                i, j = mapping(obj.x, obj.y)
                blocked_doors[(i, j)] = 0
        return blocked_doors

    # в этой функции удаляются спрайты после кулдауна
    def delete_objects(self):
        # список-копия со всеми элементами
        deleted_lst = self.list_of_sprites[:] + self.list_of_sprites_doors[:]
        # удаление открытых дверей
        for obj in deleted_lst:
            if obj.tp in {'h_door', 'v_door', 'h_nextdoor_first', 'h_nextdoor_second'} and obj.cls:
                if pygame.time.get_ticks() - obj.time >= 1000:
                    self.list_of_sprites_doors.remove(obj)
        # удаление трупов мобови на каждой карте через 4 секунды
        for obj in deleted_lst:
            if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss') and obj.dead:
                if pygame.time.get_ticks() - obj.time >= 4000:
                    self.list_of_sprites.remove(obj)
        deleted_lst = self.list_of_sprites_2[:]
        for obj in deleted_lst:
            if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss') and obj.dead:
                if pygame.time.get_ticks() - obj.time >= 4000:
                    self.list_of_sprites_2.remove(obj)
        deleted_lst = self.list_of_sprites_3[:]
        for obj in deleted_lst:
            if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss') and obj.dead:
                if pygame.time.get_ticks() - obj.time >= 4000:
                    self.list_of_sprites_3.remove(obj)


#  определяющий класс для всех спрайтов
#  на самом деле можно было спроектировать все проще через наследование
#  но мы затупили и cразу не подумали, поэтому хотя бы так
class AllSprites:
    def __init__(self, kind, pos):
        self.obj = kind.way.copy()  # путь к картинкам
        self.viewing_angles = kind.viewing_angles
        self.shift = kind.shift  # сдвиг
        self.scale = kind.scale  # масштаб
        self.animation = kind.animation.copy()  # анимация
        self.animation_dist = kind.animation_dist  # дистанция ее прогрузки
        self.animation_speed = kind.animation_speed  # скорость анимации
        self.time = None  # время, в которое спрайт был убит (заполняется позже)
        self.dead_anim = kind.dead_anim.copy()  # анимация смерти
        self.dead = kind.dead  # проверка на жизнь
        self.dead_shift = kind.dead_shift  # сдвиг мертвой анимации
        self.dead_anim_count = 0
        self.npc_hp = kind.npc_hp  # здоровье каждого моба
        self.d_sprite = []

        self.x, self.y = pos[0] * CELL, pos[1] * CELL  # позиция в координатах
        self.tp = kind.tp  # маркер
        self.blocked = kind.blocked  # маркер проходимости (прозрачности) для игрока
        self.animation_count = 0
        self.side = kind.side  # сторона прямоугольника для коллизии
        self.is_trigger = False  # видит ли нас моб
        self.d_open_trigger = False  # проверка двери на открытость
        # последняя позиция двери в зависимости от ее класса
        self.d_last_pos = self.y if self.tp == 'h_door' \
                                    or self.tp == 'h_nextdoor_first' \
                                    or self.tp == 'h_nextdoor_second' else self.x
        self.cls = False  # несуществование (нужно ли удалять)
        self.obj_action = kind.obj_action.copy()  # движение
        # если спрайт не статичный (со всех сторон одинаковый)
        if self.viewing_angles:
            # делаем списки с замороженными множествами углов (нужны будут для ключей)
            if len(self.obj) == 8:
                self.sprite_angles = [frozenset(range(338, 361)) | frozenset(range(0, 23))] + \
                                     [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
            else:
                self.sprite_angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                                     [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            # создаем словарь для соотношения картинки и угла 
            # поэтому нам и нужны замороженные множества, так они неизменямые и могут быть ключами
            self.sprite_positions = {angle: pos for angle, pos in zip(self.sprite_angles, self.obj)}

    # функция через декоратор (теперь атрибут класса), проверяющая, видят ли мобы игрока
    @property
    def is_on_fire(self):
        if C_RAY - self.side // 2 < self.current_ray < C_RAY + self.side // 2 and self.blocked:
            return self.dist_to_sprite, self.p_height
        return float('inf'), None

    # тоже атрибут для определения текущей позиции
    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    # функция для определения расстояния до спрайта 
    def object_locate(self, gamer, walls):
        fake_walls0 = [walls[0] for i in range(100)]
        fake_walls1 = [walls[-1] for i in range(100)]
        fake_walls = fake_walls0 + walls + fake_walls1
        dx, dy = self.x - gamer.x, self.y - gamer.y
        # формула расстояния между точками на плоскости
        self.dist_to_sprite = math.sqrt(dx ** 2 + dy ** 2)
        # угол между горизонтальными и вертикальными составляющими
        self.betta = math.atan2(dy, dx)
        gamma = self.betta - gamer.angle
        # соседний угол
        # условия для корректировки угла
        if dx > 0 and 180 <= math.degrees(gamer.angle) <= 360 or dx < 0 and dy < 0:
            gamma += ZWEI_PI
        # корректируем угол для реалистичности
        self.betta -= 1.4 * gamma
        
        d_rays = int(gamma / DELTA_ANGLE) # количество углов между лучами в гамме
        self.current_ray = C_RAY + d_rays  # находим луч со спрайтом
        # для того, чтобы не было рыбьего глаза и спрайты двигались нормально корректируем дистанцию
        if self.tp not in {'h_door', 'v_door', 'h_nextdoor_first', 'h_nextdoor_second'}:
            if abs(math.cos(H_FOV - self.current_ray * DELTA_ANGLE)) >= 0.5:
                self.dist_to_sprite *= math.cos(H_FOV - self.current_ray * DELTA_ANGLE)
        # фейковый луч для того, чтобы спрайты резко не исчезали
        fake_ray = self.current_ray + 100
        if 0 <= fake_ray <= N_RAYS - 1 + 2 * 100 and self.dist_to_sprite > 30:
            if self.tp not in {'h_door', 'v_door', 'h_nextdoor_first', 'h_nextdoor_second'}:
                self.p_height = min(int(PROJ_C / self.dist_to_sprite), D_HEIGHT)
            else:
                self.p_height = min(int(PROJ_C / self.dist_to_sprite), HEIGHT)
            # размеры спрайта
            sprite_width = int(self.p_height * self.scale[0])
            sprite_heigth = int(self.p_height * self.scale[1])
            h_s_width = sprite_width // 2
            h_s_height = sprite_heigth // 2
            shift = h_s_height * self.shift
            #  определяем, когда нужно показывать спрайт
            if self.tp in {'h_door', 'v_door', 'h_nextdoor_first', 'h_nextdoor_second'}:
                if self.d_open_trigger:
                    self.d_open()
                self.obj = self.show_sprite()
                sprite_object = self.s_animation()
            else:
                if self.dead and self.dead != 'never':
                    sprite_object = self.dead_animation()
                    shift = h_s_height * self.dead_shift
                    sprite_heigth = int(sprite_heigth / 1.3)
                elif self.is_trigger:
                    sprite_object = self.s_action()
                else:
                    self.obj = self.show_sprite()
                    sprite_object = self.s_animation()
            # позиция спрайта на мониторе
            sprite_pos = (self.current_ray * SCALE - h_s_width, H_HEIGHT - h_s_height + shift)
            # подготавливаем сам спрайт (картинку)
            if type(sprite_object) == list:
                sprite = pygame.transform.scale(sprite_object[0], (self.p_height, self.p_height))
            else:
                sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_heigth))
            # возвращаем все нужные атрибуты
            return (self.dist_to_sprite, sprite, sprite_pos)
        else:
            return (False,)

    def s_animation(self):  # Отображение анимация мира для игрока
        if self.animation and self.dist_to_sprite < self.animation_dist:
            sprite_object = self.animation[0]
            if self.animation_count < self.animation_speed:
                self.animation_count += 1
            if len(self.animation) == 1:
                return sprite_object
            else:
                self.animation.rotate()
                self.animation_count = 0
            return sprite_object
        return self.obj

    def show_sprite(self):  # Отображение спрайтов для игрока
        if self.viewing_angles:
            if self.betta < 0:
                self.betta += ZWEI_PI
            self.betta = 360 - int(math.degrees(self.betta))

            for angles in self.sprite_angles:
                if self.betta in angles:
                    return self.sprite_positions[angles]
        return self.obj

    def dead_animation(self):  # Анимация смерти мобов и объектов
        if len(self.dead_anim):
            if self.dead_anim_count < self.animation_speed:
                self.d_sprite = self.dead_anim[0]
                self.dead_anim_count += 1
            else:
                self.d_sprite = self.dead_anim.popleft()
                self.dead_anim_count = 0
        return self.d_sprite

    def s_action(self):  # Анимация мобов при действиях
        sprite_object = self.animation[0]
        if self.animation_count < self.animation_speed:
            self.animation_count += 1
        else:
            self.animation.rotate()
            self.animation_count = 0
        return sprite_object

    def d_open(self):  # Открытие дверей
        if self.tp == 'h_nextdoor_first':
            self.y -= 3
            if abs(self.y - self.d_last_pos) > CELL:
                self.cls = True
        if self.tp == 'h_nextdoor_second':
            self.y -= 3
            if abs(self.y - self.d_last_pos) > CELL:
                self.cls = True
        if self.tp == 'h_door':
            self.y -= 3
            if abs(self.y - self.d_last_pos) > CELL:
                self.cls = True
        elif self.tp == 'v_door':
            self.x -= 3
            if abs(self.x - self.d_last_pos) > CELL:
                self.cls = True


# далее идут классы для всех спрайтов, что значит каждый элемент, я пояснил в AllSprites

class Fire:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/fire/base/3.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = 0.7
        self.scale = (0.6, 0.6)
        self.side = 30
        self.animation = deque([pygame.image.load(f'data/sprites/fire/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(16)])
        self.animation_dist = 1800
        self.animation_speed = 10
        self.dead = 'never'
        self.dead_shift = 1.8
        self.dead_anim = []
        self.tp = 'fire'
        self.blocked = False
        self.npc_hp = None
        self.obj_action = []


class Barrel:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/barrel/base/0.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = 1.8
        self.scale = (0.4, 0.4)
        self.side = 30
        self.animation = deque([pygame.image.load(f'data/sprites/barrel/' + \
                                                  f'anim/{i}.png').convert_alpha()
                                for i in range(12)])
        self.animation_dist = 150
        self.animation_speed = 5
        self.animation_dist = 1800
        self.animation_speed = 10
        self.dead = None
        self.dead_shift = 2.6
        self.dead_anim = deque([pygame.image.load(f'data/sprites/barrel/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(4)])
        self.tp = 'barrel'
        self.blocked = True
        self.npc_hp = None
        self.obj_action = []


class Sosademon:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/sosademon/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0
        self.scale = (1, 1)
        self.side = 100
        self.animation = deque([pygame.image.load(f'data/sprites/sosademon/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(6)])
        self.animation_dist = 800
        self.animation_speed = 18
        self.dead = None
        self.dead_shift = 0.5
        self.dead_anim = deque([pygame.image.load(f'data/sprites/sosademon/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(6)])
        self.tp = 'boss'
        self.blocked = True
        self.npc_hp = 45
        self.obj_action = []


class Pinky:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/pinky/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.2
        self.scale = (0.8, 0.9)
        self.side = 120
        self.animation = deque([pygame.image.load(f'data/sprites/pinky/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 12
        self.dead = None
        self.dead_shift = 0.8
        self.dead_anim = deque([pygame.image.load(f'data/sprites/pinky/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(1, 6)])
        self.tp = 'enemy'
        self.blocked = True
        self.npc_hp = 5
        self.obj_action = []


class Obama:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/obama/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.2
        self.scale = (0.8, 0.9)
        self.side = 90
        self.animation = deque([pygame.image.load(f'data/sprites/obama/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 10
        self.dead = None
        self.dead_shift = 0.8
        self.dead_anim = deque([pygame.image.load(f'data/sprites/obama/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(6)])
        self.tp = 'enemy'
        self.blocked = True
        self.npc_hp = 3
        self.obj_action = []


class Human1:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/human1/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.5
        self.scale = (0.5, 0.8)
        self.side = 50
        self.animation = deque([pygame.image.load(f'data/sprites/human1/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 7
        self.dead = None
        self.dead_shift = 1
        self.dead_anim = deque([pygame.image.load(f'data/sprites/' + \
                                                  f'human1/death/{i}.png').convert_alpha()
                                for i in range(5)])
        self.tp = 'enemy_shooter'
        self.blocked = True
        self.npc_hp = 1
        self.obj_action = []


class Human2:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/stas/base/{i}.png').convert_alpha()
                    for i in range(8)]
        self.viewing_angles = True
        self.shift = 0.5
        self.scale = (0.6, 0.8)
        self.side = 50
        self.animation = deque([pygame.image.load(f'data/sprites/stas/' + \
                                                  f'action/{i}.png').convert_alpha()
                                for i in range(4)])
        self.animation_dist = 800
        self.animation_speed = 10
        self.dead = None
        self.dead_shift = 1
        self.dead_anim = deque([pygame.image.load(f'data/sprites/stas/' + \
                                                  f'death/{i}.png').convert_alpha()
                                for i in range(5)])
        self.tp = 'enemy'
        self.blocked = True
        self.npc_hp = 10
        self.obj_action = []


class DoorH:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha()
                    for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = CELL
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'h_door'
        self.blocked = True
        self.npc_hp = None
        self.obj_action = []


class DoorV:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha()
                    for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = CELL
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'v_door'
        self.blocked = True
        self.npc_hp = None
        self.obj_action = []


class NextDoorFirst:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha()
                    for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = CELL
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'h_nextdoor_first'
        self.blocked = True
        self.npc_hp = None
        self.obj_action = []


class NextDoorSecond:
    def __init__(self):
        self.way = [pygame.image.load(f'data/sprites/doors/h_door/{i}.png').convert_alpha()
                    for i in range(16)]
        self.viewing_angles = True
        self.shift = -0.005
        self.scale = (1.74, 1.5)
        self.side = CELL
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = 'never'
        self.dead_shift = 0
        self.dead_anim = []
        self.tp = 'h_nextdoor_second'
        self.blocked = True
        self.npc_hp = None
        self.obj_action = []


class MedKit:
    def __init__(self):
        self.way = [pygame.image.load('data/sprites/MedKit/base/0.png').convert_alpha()]
        self.viewing_angles = False
        self.shift = -7
        self.scale = (0.1, 0.1)
        self.side = 30
        self.animation = []
        self.animation_dist = 0
        self.animation_speed = 0
        self.dead = None
        self.dead_shift = 0
        self.tp = 'medkit'
        self.dead_anim = []
        self.blocked = False
        self.obj_action = []
        self.npc_hp = None

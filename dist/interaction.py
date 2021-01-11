# Импорт необходимых элементов
import random
import pygame
import sys
from map import txt_map
from r_c import mapping
from numba import njit
from parameters import *


# Функция, проверяющая могут ли мобы видеть игрока
@njit(fastmath=True, cache=True)
def ray_casting_npc_player(npc_x, npc_y, blocked_doors, txt_map, pos_gamer):
    ox, oy = pos_gamer
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    view_angle = math.atan2(delta_y, delta_x)
    view_angle += math.pi

    sin_a = math.sin(view_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = math.cos(view_angle)
    cos_a = cos_a if cos_a else 0.000001

    x, dx = (xm + CELL, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // CELL):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in txt_map or tile_v in blocked_doors:
            return False
        x += dx * CELL

    y, dy = (ym + CELL, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // CELL):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in txt_map or tile_h in blocked_doors:
            return False
        y += dy * CELL
    return True


class Interaction:
    def __init__(self, gamer, sprites, malen, diff_level):
        self.gamer = gamer
        self.sprites = sprites
        self.malen = malen
        self.diff_level = diff_level
        self.mob_speed = 0
        self.pain_sound = pygame.mixer.Sound('data/sound/deadmon.wav')
        self.pain_sound.set_volume(0.5)
        self.heal_sound = pygame.mixer.Sound('data/sound/heal.wav')
        self.set_difficulty()

    def terminate(self):  # Выход из игры
        pygame.quit()
        sys.exit()

    # Функция определяет реакцию объектов на стрельбу игрока, в зависимости от их типа
    def interaction_objects(self):
        if self.gamer.shot and self.malen.shotgun_animation_trigger:
            for obj in sorted(self.sprites.list_of_sprites
                              + self.sprites.list_of_sprites_2
                              + self.sprites.list_of_sprites_3
                              + self.sprites.list_of_sprites_doors,
                              key=lambda obj: obj.dist_to_sprite):
                if obj.is_on_fire[1]:
                    if obj.dead != 'never' and not obj.dead:
                        if ray_casting_npc_player(obj.x, obj.y, self.sprites.b_doors,
                                                  txt_map, self.gamer.pos):
                            # Стрельба по мобам
                            if obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss':
                                if self.gamer.weapon_now == 'shotgun':
                                    damage = 3
                                elif self.gamer.weapon_now == 'autorifle':
                                    damage = 0.35
                                if obj.npc_hp is None or obj.npc_hp - damage <= 0:
                                    self.pain_sound.play()
                                    obj.dead = True
                                    obj.blocked = None
                                    obj.status = False
                                    obj.time = pygame.time.get_ticks()  # Исчезновение трупов
                                else:
                                    obj.npc_hp -= damage
                            # Уничтожение бочки вместе с нанесением урона мобам неподалеку
                            elif obj.tp == 'barrel':
                                if obj.dist_to_sprite <= CELL * 3:
                                    hit = random.randrange(0, 2)
                                    if hit != 0:
                                        self.gamer.hp -= 50
                                all_1 = self.sprites.list_of_sprites \
                                        + self.sprites.list_of_sprites_2 \
                                        + self.sprites.list_of_sprites_3
                                for obj_2 in all_1:
                                    if obj_2.tp != 'fire':
                                        difference_x = obj.x - obj_2.x
                                        difference_y = obj.y - obj_2.y
                                        if math.fabs(difference_x) <= CELL // 2 \
                                                or math.fabs(difference_y) <= CELL // 2:
                                            obj_2.dead = True
                                            obj_2.blocked = None
                                            obj_2.status = False
                                            # Исчезновение трупов
                                            obj_2.time = pygame.time.get_ticks()

                            self.malen.shotgun_animation_trigger = False
                            self.malen.autorifle_animation_trigger = False
                    # Открытие доступа ко второй комнате
                    if obj.tp == 'h_nextdoor_first' and obj.dist_to_sprite < CELL:
                        key = 0
                        obj.time = pygame.time.get_ticks()
                        for elem in self.sprites.list_of_sprites:
                            if elem.tp in ('barrel', 'fire', 'medkit'):
                                pass
                            elif elem.dead == 'never':
                                pass
                            elif elem.dead != True:
                                key += 1
                        if key == 0:
                            obj.d_open_trigger = True
                            obj.blocked = None
                    if obj.tp == 'h_nextdoor_second' and obj.dist_to_sprite < CELL:
                        key = 0
                        obj.time = pygame.time.get_ticks()
                        for elem in self.sprites.list_of_sprites_2:
                            if elem.tp in ('barrel', 'fire', 'medkit'):
                                pass
                            elif elem.dead == 'never':
                                pass
                            elif elem.dead != True:
                                key += 1
                        if key == 0:
                            obj.d_open_trigger = True
                            obj.blocked = None
                            self.mob_speed = 3  # Изменение скорости мобов при попадании к боссу
                    # Открытие дверей
                    if obj.tp in {'h_door', 'v_door'} and obj.dist_to_sprite < CELL:
                        obj.d_open_trigger = True
                        obj.blocked = None
                        obj.time = pygame.time.get_ticks()
                    break
        for obj in sorted(self.sprites.list_of_sprites
                          + self.sprites.list_of_sprites_2
                          + self.sprites.list_of_sprites_3, key=lambda obj: obj.dist_to_sprite):
            if obj.tp == 'medkit':  # Поглощение аптечки
                if abs(obj.dist_to_sprite) <= 50:
                    if self.gamer.hp + 30 <= 100:
                        self.gamer.hp += 30
                    else:
                        self.gamer.hp = 100
                    self.heal_sound.play()
                    if obj in self.sprites.list_of_sprites:
                        self.sprites.list_of_sprites.remove(obj)
                    elif obj in self.sprites.list_of_sprites_2:
                        self.sprites.list_of_sprites_2.remove(obj)
                    elif obj in self.sprites.list_of_sprites_3:
                        self.sprites.list_of_sprites_3.remove(obj)

    def npc_action(self):
        for obj in (self.sprites.list_of_sprites +
                    self.sprites.list_of_sprites_2 +
                    self.sprites.list_of_sprites_3):
            if obj.tp == 'fire':
                # Проверка на то, видят ли нпс игрока
                if ray_casting_npc_player(obj.x, obj.y, self.sprites.b_doors,
                                          txt_map, self.gamer.pos):
                    obj.is_trigger = True
                    if obj.tp == 'fire':
                        if abs(obj.dist_to_sprite) <= CELL:
                            hit = random.randrange(0, 2)
                            if hit != 0:
                                self.gamer.hp -= 0.05
            if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss') \
                    and not obj.dead:
                if ray_casting_npc_player(obj.x, obj.y, self.sprites.b_doors,
                                          txt_map, self.gamer.pos):
                    obj.is_trigger = True
                    self.npc_move(obj)
                    # Атака мобов и их урон
                    if obj.tp == 'enemy_shooter':
                        hit = random.randrange(0, 2)
                        if hit != 0:
                            self.gamer.hp -= 0.15
                    if obj.tp == 'enemy':
                        if abs(obj.dist_to_sprite) <= CELL:
                            hit = random.randrange(0, 2)
                            if hit != 0:
                                self.gamer.hp -= 0.3
                    if obj.tp == 'boss':
                        if abs(obj.dist_to_sprite) <= CELL:
                            hit = random.randrange(0, 2)
                            if hit != 0:
                                self.gamer.hp -= 50
                else:
                    obj.is_trigger = False

    def set_difficulty(self):
        if self.diff_level == 'hard':
            self.mob_speed = 2
        elif self.diff_level == 'normal':
            self.mob_speed = 1.5
        elif self.diff_level == 'easy':
            self.mob_speed = 1

    def npc_move(self, obj):  # Движение нпс к игроку
        if abs(obj.dist_to_sprite) > CELL:
            dx = obj.x - self.gamer.pos[0]
            dy = obj.y - self.gamer.pos[1]
            obj.x = obj.x + self.mob_speed if dx < 0 else obj.x - self.mob_speed
            obj.y = obj.y + self.mob_speed if dy < 0 else obj.y - self.mob_speed

    def play_music(self):  # загружаем музыку, которая играет во время игры
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('data/sound/doom.wav')  # загрузка музыкальной темы игры
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    #  если мы выиграли (убили всех мобов), то вызывается эта функция, которая сообщает о победе
    def wins(self):
        if self.gamer.alive:  # если персонаж жив
            if not len([obj for obj in self.sprites.list_of_sprites_3
                        if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss')
                           and not obj.dead]):
                # если все
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/sound/ledohod.wav')
                pygame.mixer.music.play(-1)
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.terminate()
                    self.malen.win()  # отрисовка менюшки победы

    # если нас убили, то вызывается эта функция, которая сообщает о смерти персонажа
    def deads(self):
        if not self.gamer.alive:
            pygame.mixer.Sound('data/sound/pain2.wav').play()
            pygame.mixer.music.stop()
            pygame.mixer.music.load('data/sound/dead_mus.wav')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                self.malen.dead_menu()  # отрисовка менюшки смерти
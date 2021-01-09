import random
import pygame
import sys
from map import txt_map
from r_c import mapping
from numba import njit
from parameters import *


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
    def __init__(self, gamer, sprites, malen):
        self.gamer = gamer
        self.sprites = sprites
        self.malen = malen
        self.speed = 0
        self.pain_sound = pygame.mixer.Sound('data/sound/pain2.wav')
        self.heal_sound = pygame.mixer.Sound('data/sound/heal.wav')

    def terminate(self):
        pygame.quit()
        sys.exit()

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
                            if obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss':
                                if self.gamer.weapon_now == 'shotgun':
                                    damage = 3
                                elif self.gamer.weapon_now == 'autorifle':
                                    damage = 0.25
                                if obj.npc_hp is None or obj.npc_hp - damage <= 0:
                                    self.pain_sound.play()
                                    obj.dead = True
                                    obj.blocked = None
                                    obj.status = False
                                    obj.time = pygame.time.get_ticks()
                                else:
                                    obj.npc_hp -= damage
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
                                            obj_2.time = pygame.time.get_ticks()

                            self.malen.shotgun_animation_trigger = False
                            self.malen.autorifle_animation_trigger = False
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
                            self.speed = 3
                    if obj.tp in {'h_door', 'v_door'} and obj.dist_to_sprite < CELL:
                        obj.d_open_trigger = True
                        obj.blocked = None
                        obj.time = pygame.time.get_ticks()
                    break
        for obj in sorted(self.sprites.list_of_sprites
                          + self.sprites.list_of_sprites_2
                          + self.sprites.list_of_sprites_3, key=lambda obj: obj.dist_to_sprite):
            if obj.tp == 'medkit':
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
                if ray_casting_npc_player(obj.x, obj.y, self.sprites.b_doors,
                                          txt_map, self.gamer.pos):
                    obj.is_trigger = True
                    if obj.tp == 'fire':
                        if abs(obj.dist_to_sprite) <= CELL:
                            hit = random.randrange(0, 2)
                            if hit != 0:
                                self.gamer.hp -= 0.05
            if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss') and not obj.dead:
                if ray_casting_npc_player(obj.x, obj.y, self.sprites.b_doors,
                                          txt_map, self.gamer.pos):
                    obj.is_trigger = True
                    self.npc_move(obj)
                    # Атака мобов
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
                                self.gamer.hp -= 1000
                else:
                    obj.is_trigger = False

    def npc_move(self, obj):
        if abs(obj.dist_to_sprite) > CELL:
            dx = obj.x - self.gamer.pos[0]
            dy = obj.y - self.gamer.pos[1]
            obj.x = obj.x + 2 + self.speed if dx < 0 else obj.x - 2 - self.speed
            obj.y = obj.y + 2 + self.speed if dy < 0 else obj.y - 2 - self.speed

    def play_music(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.load('data/sound/thema1.wav')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(10)

    def wins(self):
        if self.gamer.alive:
            if not len([obj for obj in self.sprites.list_of_sprites_3
                        if (obj.tp == 'enemy' or obj.tp == 'enemy_shooter' or obj.tp == 'boss') and not obj.dead]):
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/sound/win.wav')
                pygame.mixer.music.play()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.terminate()
                    self.malen.win()

    def deads(self):
        if not self.gamer.alive:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.terminate()
                self.malen.dead_menu()

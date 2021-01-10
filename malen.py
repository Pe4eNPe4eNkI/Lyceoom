# Это файл с классом, в котором происходит отрисовка всех штук
# "malen" (нем.) = "рисовать" (рус.)

import pygame
import sys
from collections import deque
from random import randrange
from parameters import *
from map import mini_map, Camera


class Malen:
    def __init__(self, monitor, monitor_map, gamer, timer):
        self.monitor = monitor
        self.monitor_map = monitor_map
        self.gamer = gamer
        self.timer = timer
        self.camera = Camera(self.monitor_map, self.gamer)
        self.corps_on = False  # остаются ли трупы после смерти
        self.diff_level = 'hard'

        # шрифты
        self.font_win = pygame.font.Font('data/font/font1.ttf', 65)
        self.font = pygame.font.Font('data/font/font1.ttf', 55, bold=True)

        # текстуры стен и неба
        self.texture = {1: pygame.image.load('data/text/wall/wall11.png').convert(),
                        2: pygame.image.load('data/text/wall/wall8.png').convert(),
                        3: pygame.image.load('data/text/wall/wall9.png').convert(),
                        4: pygame.image.load('data/text/wall/wall10.png').convert(),
                        'S1': pygame.image.load('data/text/sky/sk1.jpeg').convert(),
                        'S2': pygame.image.load('data/text/sky/sky5.png').convert(),
                        'S3': pygame.image.load('data/text/sky/sky8.png').convert(),
                        5: pygame.image.load('data/text/wall/wall13.png').convert(),
                        6: pygame.image.load('data/text/wall/wall17.png').convert(),
                        7: pygame.image.load('data/text/wall/wall15.png').convert(),
                        8: pygame.image.load('data/text/wall/wall16.png').convert(),
                        9: pygame.image.load('data/text/wall/wall3.png').convert(),
                        10: pygame.image.load('data/text/wall/wall12.png').convert(),
                        11: pygame.image.load('data/text/wall/wall18.png').convert(),
                        12: pygame.image.load('data/text/wall/wall19.png').convert(),
                        13: pygame.image.load('data/text/wall/wall5.png').convert(),
                        14: pygame.image.load('data/text/wall/wall6.png').convert(),
                        }

        # открыта ли меню
        self.menu_tr = True

        # фоновые картинки
        self.menu_picture = pygame.image.load('data/text/bg/bg2.jpg').convert()
        self.dead_picture = pygame.image.load('data/text/bg/bg_dead.jpg').convert()

        # дробовик
        self.shotgun_base_sprite = pygame.image.load('data/sprites/weapons/shot-gun/' + \
                                                     'base/1.png').convert_alpha()
        self.shotgun_animation = deque([pygame.image.load(f'data/sprites/weapons/shot-gun/' + \
                                                          f'shot1/{i}.png').convert_alpha()
                                        for i in range(14)])
        self.shotgun_rect = self.shotgun_base_sprite.get_rect()
        self.shotgun_pos = (H_WIDTH - self.shotgun_rect.width // 2,
                            HEIGHT - self.shotgun_rect.height)
        self.shotgun_length = len(self.shotgun_animation)
        self.shotgun_length_count = 0
        self.shotgun_animation_speed = 5
        self.shotgun_animation_count = 0
        self.shotgun_animation_trigger = True
        self.shotgun_sound = pygame.mixer.Sound('data/sound/boom3.wav')  # звук выстрела
        self.shotgun_sound.set_volume(0.4)
        self.shotgun_damage = 3  # дамаг от дробовика

        # автомат
        self.autorifle_base_sprite = pygame.image.load(
            'data/sprites/weapons/autorifle/0.png').convert_alpha()
        self.autorifle_animation = deque([pygame.image.load(f'data/sprites/weapons/autorifle/' + \
                                                            f'{i}.png').convert_alpha()
                                          for i in range(4)])
        self.autorifle_rect = self.autorifle_base_sprite.get_rect()
        self.autorifle_pos = (H_WIDTH - self.autorifle_rect.width // 2,
                              HEIGHT - self.autorifle_rect.height)
        self.autorifle_length = len(self.autorifle_animation)
        self.autorifle_length_count = 0
        self.autorifle_animation_speed = 1
        self.autorifle_animation_count = 0
        self.autorifle_animation_trigger = True
        self.autorifle_sound = pygame.mixer.Sound('data/sound/shotrifle.wav')  # звук выстрела
        self.autorifle_sound.set_volume(0.7)
        self.autorifle_damage = 1  # дамаг от автомата

        # эффекты выстрела
        self.sfx = deque([pygame.image.load(f'data/sprites/'
                                            f'shoot_sfx/action/{i}.png').convert_alpha()
                          for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def bg(self, angle):  # отрисовка неба
        sky_offset = -5 * math.degrees(angle) % WIDTH
        if self.gamer.x < 2306:  # проверка на номер комнаты ( на координаты игрока )
            self.monitor.blit(self.texture['S1'], (sky_offset, 0))
            self.monitor.blit(self.texture['S1'], (sky_offset - WIDTH, 0))
            self.monitor.blit(self.texture['S1'], (sky_offset + WIDTH, 0))
        elif self.gamer.x < 4556 and self.gamer.x > 2306:
            self.monitor.blit(self.texture['S2'], (sky_offset, 0))
            self.monitor.blit(self.texture['S2'], (sky_offset - WIDTH, 0))
            self.monitor.blit(self.texture['S2'], (sky_offset + WIDTH, 0))
        elif self.gamer.x > 4556:
            self.monitor.blit(self.texture['S3'], (sky_offset, 0))
            self.monitor.blit(self.texture['S3'], (sky_offset - WIDTH, 0))
            self.monitor.blit(self.texture['S3'], (sky_offset + WIDTH, 0))

        # отрисовка текстуры неба
        pygame.draw.rect(self.monitor, DARKGREY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, world_objects):  # расстановка спрайтов по карте
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, ob, ob_pos = obj
                self.monitor.blit(ob, ob_pos)

    def fps(self, clock):  # счетчик фпс в углу экрана
        fps_clock = str(int(clock.get_fps()))
        render = self.font.render(fps_clock, 0, RED)
        self.monitor.blit(render, FPS_POS)

    def hp(self, hp):  # кол-во хп персонажа
        hp = str(int(hp))
        pygame.draw.rect(self.monitor, BLACK, (*STATUSBAR_POS, 100, 30), 2)

        # отрисовка полоски хп разными цветами
        if 0 <= self.gamer.hp <= 33.3:
            render = self.font.render(hp, 0, RED)
            pygame.draw.rect(self.monitor, RED, (*[i + 1 for i in STATUSBAR_POS],
                                                 self.gamer.hp * 0.99, 28), 0)
            self.monitor.blit(render, HP_POS)
        if 33.3 < self.gamer.hp <= 66.6:
            render = self.font.render(hp, 0, YELLOW)
            pygame.draw.rect(self.monitor, YELLOW, (*[i + 1 for i in STATUSBAR_POS],
                                                    self.gamer.hp * 0.99, 28), 0)
            self.monitor.blit(render, HP_POS)
        if 66.6 < self.gamer.hp <= 100:
            render = self.font.render(hp, 0, SPRINGGREEN)
            pygame.draw.rect(self.monitor, GREEN, (*[i + 1 for i in STATUSBAR_POS],
                                                   self.gamer.hp * 0.99, 28), 0)
            self.monitor.blit(render, HP_POS)  # отрисовка статус бара и хп

    def terminate(self):  # выход из игры
        pygame.quit()
        sys.exit()

    def mini_map(self):  # отрисовка мини-карты
        self.monitor_map.fill(GRAY)  # фоновый цвет
        # позиции персонажа на миникарте
        xmap, ymap = self.gamer.x // MAP_SCALE, self.gamer.y // MAP_SCALE
        # короткий луч для определения направления
        pygame.draw.line(self.monitor_map, YELLOW, (xmap + self.camera.dx, ymap),
                         (xmap + self.camera.dx + 4 * math.cos(self.gamer.angle),
                          ymap + 4 * math.sin(self.gamer.angle)), 2)

        # отрисовка персонажа ( шарик )
        pygame.draw.circle(self.monitor_map, RED, (int(xmap) + self.camera.dx, int(ymap)), 4)
        # отрисовка самого персонажа
        for x, y in mini_map:
            self.camera.apply(x, y)
        self.monitor.blit(self.monitor_map, MAP_POS)
        self.camera.update()

    def choice_weapon(self, shots, flag):  # Функция позволяет выбрать оружие из инвентаря
        if flag == 'shotgun' or flag == '':
            if self.gamer.shot:
                if not self.shotgun_length_count:
                    self.shotgun_sound.play()
                self.shot_projection = int(min(shots)[1] // 2)
                self.bullet_sfx()
                shotgun_sprite = self.shotgun_animation[0]
                self.monitor.blit(shotgun_sprite, self.shotgun_pos)
                self.shotgun_animation_count += 1
                if self.shotgun_animation_count == self.shotgun_animation_speed:
                    self.shotgun_animation.rotate(-1)
                    self.shotgun_animation_count = 0
                    self.shotgun_length_count += 1
                    self.shotgun_animation_trigger = False
                if self.shotgun_length_count == self.shotgun_length:
                    self.gamer.shot = False
                    self.shotgun_length_count = 0
                    self.sfx_length_count = 0
                    self.shotgun_animation_trigger = True
            else:
                self.monitor.blit(self.shotgun_base_sprite, self.shotgun_pos)
                self.gamer.weapon_now = 'shotgun'
        elif flag == 'autorifle':
            if self.gamer.shot:
                if not self.autorifle_length_count:
                    self.autorifle_sound.play()
                self.shot_projection = int(min(shots)[1] // 2)
                self.bullet_sfx()
                autorifle_sprite = self.autorifle_animation[0]
                self.monitor.blit(autorifle_sprite, self.autorifle_pos)
                self.autorifle_animation_count += 1
                if self.autorifle_animation_count == self.autorifle_animation_speed:
                    self.autorifle_animation.rotate(-1)
                    self.autorifle_animation_count = 0
                    self.autorifle_length_count += 1
                    self.autorifle_animation_trigger = False
                if self.autorifle_length_count == self.autorifle_length:
                    self.gamer.shot = False
                    self.autorifle_length_count = 0
                    self.sfx_length_count = 0
                    self.shotgun_animation_trigger = True
            else:
                self.monitor.blit(self.autorifle_base_sprite, self.autorifle_pos)
                self.gamer.weapon_now = 'autorifle'

    def bullet_sfx(self):  # Отрисовывает взрывы на стенах при стрельбе
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.monitor.blit(sfx, (H_WIDTH - sfx_rect.w // 2, H_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def win(self):  # окошко победы
        x = 0
        keys = pygame.key.get_pressed()  # при нажатии esc выход
        if keys[pygame.K_ESCAPE]:
            self.terminate()

        # поздравительная надпись
        rend = self.font_win.render("You're not dead, congratulations!", 1,
                                    (randrange(100, 255), 100, 220))
        rect = pygame.Rect(0, 0, 630, 250)
        rect.center = H_WIDTH, H_HEIGHT

        pygame.draw.rect(self.monitor, BLACK, rect, border_radius=50)
        self.monitor.blit(rend, (rect.centerx - 290, rect.centery - 80))
        button_font = pygame.font.Font('data/font/font2.ttf', 35)

        '''
        кнопка рестарт ( на будущее)
        restart = button_font.render('RESTART', 0, pygame.Color('gray'))
        button_restart = pygame.Rect(0, 0, 400, 100)
        button_restart.center = H_WIDTH, H_HEIGHT + 5
        '''

        # кнопка выхода
        reexit = button_font.render('EXIT', 1, pygame.Color('gray'))
        button_reexit = pygame.Rect(0, 0, 300, 100)
        button_reexit.center = H_WIDTH, H_HEIGHT + 55
        '''
        тож для рестарта
        pygame.draw.rect(self.monitor, BLUE, button_restart, border_radius=25, width=10)
        self.monitor.blit(restart, (button_restart.centerx - 155, button_restart.centery - 25))
        '''
        pygame.draw.rect(self.monitor, BLUE, button_reexit, border_radius=25, width=10)
        self.monitor.blit(reexit, (button_reexit.centerx - 75, button_reexit.centery - 15))

        mouse_pos = pygame.mouse.get_pos()  # для мышки
        mouse_click = pygame.mouse.get_pressed()

        '''
        if button_restart.collidepoint(mouse_pos):
           pygame.draw.rect(self.monitor, BLUE, button_restart, border_radius=25)
           self.monitor.blit(restart, (button_restart.centerx - 155, button_restart.centery - 25))
           if mouse_click[0]:
               self.menu_tr = False
        '''

        if button_reexit.collidepoint(mouse_pos):  # при нажатии кнопки "выход" игра завершается
            pygame.mouse.set_visible(True)
            pygame.draw.rect(self.monitor, BLUE, button_reexit, border_radius=25)
            self.monitor.blit(reexit, (button_reexit.centerx - 75, button_reexit.centery - 15))
            if mouse_click[0]:
                self.terminate()

        pygame.display.flip()
        self.timer.tick(15)

    '''
        def dead_music(self):
        pygame.mixer.init()
        pygame.mixer.music.load('data/sound/dead_mus.wav')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play()
    '''

    # смысл примерно такой же, как и в меню победы, но ток тут аниме девка на заставке
    def menu(self):
        x = 0
        pygame.mixer.music.load('data/sound/ledohod.wav')
        pygame.mixer.music.play()

        button_font = pygame.font.Font('data/font/font2.ttf', 40)
        button_font_corps = pygame.font.Font('data/font/font2.ttf', 26)
        label_font = pygame.font.Font('data/font/font1.ttf', 280)

        start = button_font.render('START', 0, pygame.Color(50, 50, 50))
        button_start = pygame.Rect(0, 0, 300, 100)
        button_start.center = 170, H_HEIGHT - 50

        exit = button_font.render('EXIT', 1, pygame.Color(50, 50, 50))
        button_exit = pygame.Rect(0, 0, 300, 100)
        button_exit.center = 170, H_HEIGHT + 100

        optimize_off = button_font_corps.render('CORPSE', 1, pygame.Color(52, 50, 50))
        optimize_on = button_font_corps.render('CORPSE', 1, pygame.Color(205, 184, 145))
        button_optimize = pygame.Rect(0, 0, 200, 66.7)
        button_optimize.center = 1080, 54

        dif_lvl_easy = button_font_corps.render('EASY', 1, pygame.Color(52, 80, 80))
        dif_lvl_normal = button_font_corps.render('NORMAL', 1, pygame.Color(52, 50, 50))
        dif_lvl_hard = button_font_corps.render('HARD', 1, pygame.Color(205, 184, 145))
        button_dif_lvl = pygame.Rect(0, 0, 200, 66.7)
        button_dif_lvl.center = 1080, 134



        while self.menu_tr:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
            pygame.mouse.set_visible(True)
            self.monitor.blit(self.menu_picture, (0, 0))
            x += 1

            pygame.draw.rect(self.monitor, BLACK, button_start, border_radius=25, width=10)
            self.monitor.blit(start, (button_start.centerx - 110, button_start.centery - 25))

            pygame.draw.rect(self.monitor, BLACK, button_exit, border_radius=25, width=10)
            self.monitor.blit(exit, (button_exit.centerx - 85, button_exit.centery - 20))

            pygame.draw.rect(self.monitor, BLACK, button_optimize, border_radius=25, width=10)
            self.monitor.blit(optimize_on if self.corps_on else optimize_off,
                              (button_optimize.centerx - 87, button_optimize.centery - 12))

            if self.diff_level == 'hard':
                self.difficulty = [dif_lvl_hard, button_dif_lvl.centerx - 58,
                                   button_dif_lvl.centery - 12]
            elif self.diff_level == 'normal':
                self.difficulty = [dif_lvl_normal, button_dif_lvl.centerx - 87,
                                   button_dif_lvl.centery - 12]
            else:
                self.difficulty = [dif_lvl_easy, button_dif_lvl.centerx - 58,
                                   button_dif_lvl.centery - 12]
            pygame.draw.rect(self.monitor, BLACK, button_dif_lvl, border_radius=25, width=10)
            self.monitor.blit(self.difficulty[0],
                              (self.difficulty[1], self.difficulty[2]))

            color = randrange(40)
            label = label_font.render('Lyceoom', 1, (color, color, color))
            self.monitor.blit(label, (30, 45))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                '''
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/sound/hit_menu1.mp3')
                pygame.mixer.music.play()
                '''
                pygame.draw.rect(self.monitor, BLACK, button_start, border_radius=25)
                self.monitor.blit(start, (button_start.centerx - 110, button_start.centery - 25))
                if mouse_click[0]:
                    self.menu_tr = False
            elif button_exit.collidepoint(mouse_pos):
                '''
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/sound/hit_menu1.mp3')
                pygame.mixer.music.play()
                '''
                pygame.draw.rect(self.monitor, BLACK, button_exit, border_radius=25)
                self.monitor.blit(exit, (button_exit.centerx - 85, button_exit.centery - 20))
                if mouse_click[0]:
                    self.terminate()
            elif button_optimize.collidepoint(mouse_pos):
                '''
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/sound/hit_menu1.mp3')
                pygame.mixer.music.play()
                '''
                if mouse_click[0]:
                    if self.corps_on:
                        self.corps_on = False
                        print(self.corps_on)

                    else:
                        self.corps_on = True
                        print(self.corps_on)

            elif button_dif_lvl.collidepoint(mouse_pos):
                '''
                pygame.mixer.music.stop()
                pygame.mixer.music.load('data/sound/hit_menu1.mp3')
                pygame.mixer.music.play()
                '''
                if mouse_click[0]:
                    if self.diff_level == 'hard':
                        self.diff_level = 'normal'
                        print(self.diff_level)
                    elif self.diff_level == 'normal':
                        self.diff_level = 'easy'
                        print(self.diff_level)
                    elif self.diff_level == 'easy':
                        self.diff_level = 'hard'
                        print(self.diff_level)

            pygame.display.flip()
            self.timer.tick(20)

    def dead_menu(self):  # тут тоже менюшка, ток уже смерти и тут не аниме девка, а череп
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.terminate()
        button_font = pygame.font.Font('data/font/font2.ttf', 35)

        rend_dead = self.font_win.render("Antonio was killed, try again", 1,
                                         (randrange(20, 180), 100, 220))

        self.monitor.blit(self.dead_picture, (H_WIDTH - 400, H_HEIGHT - 300))
        self.monitor.blit(rend_dead, (H_WIDTH - 240, 130))
        reexit = button_font.render('EXIT', 1, pygame.Color('gray'))
        button_reexit = pygame.Rect(0, 0, 300, 70)
        button_reexit.center = H_WIDTH, H_HEIGHT + 185
        pygame.draw.rect(self.monitor, RED, button_reexit, border_radius=25, width=10)
        self.monitor.blit(reexit, (button_reexit.centerx - 75, button_reexit.centery - 15))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_reexit.collidepoint(mouse_pos):
            pygame.mouse.set_visible(True)
            pygame.draw.rect(self.monitor, RED, button_reexit, border_radius=25)
            self.monitor.blit(reexit, (button_reexit.centerx - 75, button_reexit.centery - 15))
            if mouse_click[0]:
                self.terminate()
        pygame.display.flip()
        self.timer.tick(20)
import pygame
import sys
from collections import deque
from random import randrange
from parameters import *
from r_c import ray_casting
from map import mini_map, Camera


class Malen:
    def __init__(self, monitor, monitor_map, gamer, timer):
        self.monitor = monitor
        self.monitor_map = monitor_map
        self.gamer = gamer
        self.timer = timer
        self.camera = Camera(self.monitor_map, self.gamer)
        self.font_win = pygame.font.Font('data/font/font1.ttf', 65)
        self.font = pygame.font.Font('data/font/font1.ttf', 55, bold=True)
        self.texture = {1: pygame.image.load('data/img/lvl1/wall11.png').convert(),
                        2: pygame.image.load('data/img/lvl1/wall8.png').convert(),
                        3: pygame.image.load('data/img/lvl1/wall9.png').convert(),
                        4: pygame.image.load('data/img/lvl1/wall10.png').convert(),
                        'S': pygame.image.load('data/img/lvl1/sk1.jpeg').convert(),
                        'F': pygame.image.load('data/text/down/down.png').convert(),
                        5: pygame.image.load('data/img/lvl2/wall8.png').convert(),
                        6: pygame.image.load('data/img/lvl2/wall13.png').convert(),
                        7: pygame.image.load('data/img/lvl2/wall9.png').convert(),
                        8: pygame.image.load('data/img/lvl2/wall11.png').convert()
                        }
        self.menu_tr = True
        self.menu_picture = pygame.image.load('data/text/bg/bg2.jpg').convert()
        self.dead_picture = pygame.image.load('data/text/bg/bg_dead.jpg').convert()
        # shot_gun
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
        self.shotgun_sound = pygame.mixer.Sound('sound/boom3.wav')

        # autorifle
        self.autorifle_base_sprite = pygame.image.load('data/sprites/weapons/autorifle/0.png').convert_alpha()
        self.autorifle_animation = deque([pygame.image.load(f'data/sprites/weapons/autorifle/' + \
                                                          f'{i}.png').convert_alpha()
                                        for i in range(4)])
        self.autorifle_rect = self.autorifle_base_sprite.get_rect()
        self.autorifle_pos = (H_WIDTH - self.autorifle_rect.width // 2,
                            HEIGHT - self.autorifle_rect.height)
        self.autorifle_length = len(self.autorifle_animation)
        self.autorifle_length_count = 0
        self.autorifle_animation_speed = 2
        self.autorifle_animation_count = 0
        self.autorifle_animation_trigger = True
        self.autorifle_sound = pygame.mixer.Sound('sound/shotrifle.wav')

        # sfx
        self.sfx = deque([pygame.image.load(f'data/sprites/'
                                            f'shoot_sfx/action/{i}.png').convert_alpha()
                          for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def bg(self, angle):
        sky_offset = -5 * math.degrees(angle) % WIDTH
        self.monitor.blit(self.texture['S'], (sky_offset, 0))
        self.monitor.blit(self.texture['S'], (sky_offset - WIDTH, 0))
        self.monitor.blit(self.texture['S'], (sky_offset + WIDTH, 0))

        pygame.draw.rect(self.monitor, DARKGREY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, ob, ob_pos = obj
                self.monitor.blit(ob, ob_pos)

    def fps(self, clock):
        fps_clock = str(int(clock.get_fps()))
        render = self.font.render(fps_clock, 0, RED)
        self.monitor.blit(render, FPS_POS)

    def hp(self, hp):
        hp = str(int(hp))
        pygame.draw.rect(self.monitor, BLACK, (*STATUSBAR_POS, 100, 30), 2)
        if 0 <= self.gamer.hp <= 33.3:
            render = self.font.render(hp, 0, RED)
            pygame.draw.rect(self.monitor, RED, (*[i + 1 for i in STATUSBAR_POS], 
                                                 self.gamer.hp * 0.99, 28), 0)
        if 33.3 < self.gamer.hp <= 66.6:
            render = self.font.render(hp, 0, YELLOW)
            pygame.draw.rect(self.monitor, YELLOW, (*[i + 1 for i in STATUSBAR_POS], 
                                                    self.gamer.hp * 0.99, 28), 0)
        if 66.6 < self.gamer.hp <= 100:
            render = self.font.render(hp, 0, SPRINGGREEN)
            pygame.draw.rect(self.monitor, GREEN, (*[i + 1 for i in STATUSBAR_POS], 
                                                    self.gamer.hp * 0.99, 28), 0)
        self.monitor.blit(render, HP_POS)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def mini_map(self):
        self.monitor_map.fill(BLACK)
        # позиции персонажа на миникарте
        xmap, ymap = self.gamer.x // MAP_SCALE, self.gamer.y // MAP_SCALE
        # короткий луч для определения направления
        pygame.draw.line(self.monitor_map, YELLOW, (xmap + self.camera.dx, ymap),
                         (xmap + self.camera.dx + 4 * math.cos(self.gamer.angle),
                          ymap + 4 * math.sin(self.gamer.angle)), 2)
        pygame.draw.circle(self.monitor_map, RED, (int(xmap) + self.camera.dx, int(ymap)), 4)
        # отрисовка самого персонажа
        for x, y in mini_map:
            self.camera.apply(x, y)
        self.monitor.blit(self.monitor_map, MAP_POS)
        self.camera.update()

    def player_weapon_shotgun(self, shots):
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

    def player_weapon_autorifle(self, shots):
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

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_projection, self.shot_projection))
            sfx_rect = sfx.get_rect()
            self.monitor.blit(sfx, (H_WIDTH - sfx_rect.w // 2, H_HEIGHT - sfx_rect.h // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)

    def win(self):
        x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.terminate()

        rend = self.font_win.render("You're not dead, congratulations!", 1,
                                    (randrange(100, 255), 100, 220))
        rect = pygame.Rect(0, 0, 630, 250)
        rect.center = H_WIDTH, H_HEIGHT

        pygame.draw.rect(self.monitor, BLACK, rect, border_radius=50)
        self.monitor.blit(rend, (rect.centerx - 290, rect.centery - 80))
        button_font = pygame.font.Font('data/font/font2.ttf', 35)

        # restart = button_font.render('RESTART', 0, pygame.Color('gray'))
        # button_restart = pygame.Rect(0, 0, 400, 100)
        # button_restart.center = H_WIDTH, H_HEIGHT + 5
        reexit = button_font.render('EXIT', 1, pygame.Color('gray'))
        button_reexit = pygame.Rect(0, 0, 300, 100)
        button_reexit.center = H_WIDTH, H_HEIGHT + 55
        # pygame.draw.rect(self.monitor, BLUE, button_restart, border_radius=25, width=10)
        # self.monitor.blit(restart, (button_restart.centerx - 155, button_restart.centery - 25))
        pygame.draw.rect(self.monitor, BLUE, button_reexit, border_radius=25, width=10)
        self.monitor.blit(reexit, (button_reexit.centerx - 75, button_reexit.centery - 15))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        # if button_restart.collidepoint(mouse_pos):
        #    pygame.draw.rect(self.monitor, BLUE, button_restart, border_radius=25)
        #    self.monitor.blit(restart, (button_restart.centerx - 155, button_restart.centery - 25))
        #    if mouse_click[0]:
        #        self.menu_tr = False
        if button_reexit.collidepoint(mouse_pos):
            pygame.draw.rect(self.monitor, BLUE, button_reexit, border_radius=25)
            self.monitor.blit(reexit, (button_reexit.centerx - 75, button_reexit.centery - 15))
            if mouse_click[0]:
                self.terminate()

        pygame.display.flip()
        self.timer.tick(15)

    def menu(self):
        x = 0
        #pygame.mixer.music.load('sound/win.mp3')
        #pygame.mixer.music.play()

        button_font = pygame.font.Font('data/font/font2.ttf', 40)
        label_font = pygame.font.Font('data/font/font1.ttf', 280)

        start = button_font.render('START', 0, pygame.Color(50, 50, 50))
        button_start = pygame.Rect(0, 0, 300, 100)
        button_start.center = 170, H_HEIGHT - 50
        exit = button_font.render('EXIT', 1, pygame.Color(50, 50, 50))
        button_exit = pygame.Rect(0, 0, 300, 100)
        button_exit.center = 170, H_HEIGHT + 100

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
            self.monitor.blit(exit, (button_exit.centerx - 90, button_exit.centery - 25))

            color = randrange(40)
            label = label_font.render('Lyceoom', 1, (color, color, color))
            self.monitor.blit(label, (30, 45))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                pygame.draw.rect(self.monitor, BLACK, button_start, border_radius=25)
                self.monitor.blit(start, (button_start.centerx - 110, button_start.centery - 25))
                if mouse_click[0]:
                    self.menu_tr = False
            elif button_exit.collidepoint(mouse_pos):
                pygame.draw.rect(self.monitor, BLACK, button_exit, border_radius=25)
                self.monitor.blit(exit, (button_exit.centerx - 90, button_exit.centery - 25))
                if mouse_click[0]:
                    self.terminate()

            pygame.display.flip()
            self.timer.tick(20)

    def dead_menu(self):
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
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sound/hit.mp3')
            pygame.mixer.music.play()
            pygame.draw.rect(self.monitor, RED, button_reexit, border_radius=25)
            self.monitor.blit(reexit, (button_reexit.centerx - 75, button_reexit.centery - 15))
            if mouse_click[0]:
                self.terminate()
        pygame.display.flip()
        self.timer.tick(20)
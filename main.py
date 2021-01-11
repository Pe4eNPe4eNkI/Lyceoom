# Импорт необходимых элементов
import sys
from gamer import Gamer
from sprites import *
from r_c import walls_with_ray_cast
from malen import Malen
from interaction import Interaction


# Функция выхода из игры
def terminate():
    pygame.quit()
    sys.exit()

# Запуск и инициализация основных файлов игры
pygame.init()
monitor = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Lyceoom')
mon_map = pygame.Surface(MAP_RES)
pygame.mouse.set_visible(False)
timer = pygame.time.Clock()
sprites = Sprites()
gamer = Gamer(sprites)
malen = Malen(monitor, mon_map, gamer, timer)
malen.menu()
interaction = Interaction(gamer, sprites, malen, malen.diff_level)
interaction.play_music()

# Запуск цикла игры
while True:
    pygame.mouse.set_visible(False)
    gamer.movement()
    malen.bg(gamer.angle)
    flag = gamer.return_flag()
    walls, wall_shot = walls_with_ray_cast(gamer, malen.texture)
    # Отрисовка элементов
    malen.world(walls + [obj.object_locate(gamer, walls) for obj in sprites.list_of_sprites] + \
                        [obj.object_locate(gamer, walls) for obj in sprites.list_of_sprites_2] + \
                        [obj.object_locate(gamer, walls) for obj in sprites.list_of_sprites_3] +
                        [obj.object_locate(gamer, walls) for obj in sprites.list_of_sprites_doors])
    malen.fps(timer)
    malen.hp(gamer.hp)
    malen.mini_map()

    malen.choice_weapon([wall_shot, sprites.sprite_shot], flag)

    interaction.interaction_objects()
    interaction.npc_action()
    interaction.wins()
    interaction.deads()
    gamer.is_dead()
    sprites.delete_objects(malen.corps_on)
    pygame.display.flip()
    timer.tick(FPS)
import pygame as pg
import numpy as np
import random as rnd
from time import time
from scipy.ndimage import gaussian_filter
from upscale_func import upscale, add, generate
from shipsgen import *
from Hero import *
import os
import sys

horizontal_borders = pg.sprite.Group()
vertical_borders = pg.sprite.Group()

class Border(pg.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pg.Surface([1, y2 - y1])
            self.rect = pg.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pg.Surface([x2 - x1, 1])
            self.rect = pg.Rect(x1, y1, x2 - x1, 1)


width = 500
height = 700
'''Border(5, 5, width - 5, 5)
Border(5, height - 5, width - 5, height - 5)
Border(5, 5, 5, height - 5)
Border(width - 5, 5, width - 5, height - 5)'''

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


pg.init()
screen_size = (500, 700)
screen = pg.display.set_mode(screen_size)
FPS = 60

running = True
clock = pg.time.Clock()
a = np.array([1, 0, 0, 1])
a = a.reshape(2, 2)
map2 = [[1, 0, 1, 0], [0, 1, 1, 1], [0, 0, 1, 0], [0, 1, 0, 0]]
map = []

all_sprites = pg.sprite.Group()
enemies = pg.sprite.Group()

powerups = pg.sprite.Group()
bullets = pg.sprite.Group()
background = load_image("background2.png")
background_rect = background.get_rect()

hero_image = pg.transform.scale(load_image("ship.png"), (
    74, 96))  # размер изображения: 37*48
mini_image_ship = pg.transform.scale(load_image("mini_image_ship.png"), (
    28, 40))  # размер изображения: 14*20
laser_img = pg.transform.scale(load_image("laser.png"), (8, 18))  # размер изображения: 4*9
enemy_img = pg.transform.scale(load_image("test_enemy.png"), (28*2, 18*2))

sprite_group, hero_group = pg.sprite.Group(), pg.sprite.Sprite(all_sprites)
hero_group.image = hero_image
hero_group.rect = hero_group.image.get_rect()
hero_group.rect.x = -100
hero_group.rect.y = -100


enemy_sprite = pg.sprite.Sprite()
enemy_sprite.image = enemy_img
enemy_sprite.rect = enemy_sprite.image.get_rect()
enemy_sprite.rect.x = -10
enemy_sprite.rect.y = -70
all_sprites.add(enemy_sprite)


laser_sprite = pg.sprite.Sprite()
laser_sprite.image = laser_img
laser_sprite.rect = laser_sprite.image.get_rect()
laser_sprite.rect.x = -50
laser_sprite.rect.y = -50
all_sprites.add(laser_sprite)

'''for i in range(16):
    s = []
    for j in range(16):
        s.append(rnd.randint(0, 100) / 100)
    map.append(s)

a = []
for i in range(4):
    s = []
    for j in range(4):
        s.append(rnd.randint(0, 100) / 100)
    a.append(s)

map2 = upscale(map2, 64, 64)
tic = time()
a = upscale(a, 64, 64)
a = np.array(a,"float")
a = gaussian_filter(a, sigma=20)
#map2 = blur(map2, 20)1
toc = time()
print(toc - tic)

map = upscale(map, 16, 16)
#map = blur(map, 3)
map = gaussian_filter(np.array(map), sigma=10)
map = add(map, a, 1)

map = np.array(map)
t1 = time()
map = generate(64,64,8,10)
a = generate(4,4,128,50,1)
map = add(map, a, 0.5)
t2 = time()
print(t2-t1)'''
# map2 = ship()
# map = []

map = generate(32, 32, 4, 3)

for i in range(len(map)):
    for j in range(len(map[0])):
        map[i][j] **= 4
# for i in map2:
#    map.append(i[::-1]+i)

# pprint(map)

# map = upscale(map,16,16)
ai = EnemyAI()
clr = (200, 200, 200)
hero = Hero(220, 500, 5, [0, 0], [0, 0], 5, 10, hero_image, all_sprites)
#hero_group.rect.x = hero.get_coord()[0]
#hero_group.rect.y = hero.get_coord()[1]
bulls = []
while running:
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            if event.key == pg.K_p:
                pause = True
            if event.key == pg.K_UP or event.key == pg.K_w:
                hero.get_dir("up")
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                hero.get_dir("down")
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                hero.get_dir("left")
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                hero.get_dir("right")

            if event.key == pg.K_SPACE:
                b = hero.shoot(laser_img, hero.get_coord()[0], hero.get_coord()[1], -1, 2, 10, 0, all_sprites)

                all_sprites.add(laser_sprite)
                bulls.append(b)

        else:
            hero.get_dir('none')
    ai.get_screen_info(1,[],hero.get_info(),bulls)
    ai.difficult_level_calc()
    ai.difficult_level_change(enemy_img, enemy_sprite, all_sprites)
    ai.act(hero.get_coord())
    #print(ai.get_enemy_list)
    # hero.debug()
    # print(len(bulls))
    hero.move()
    for i in bulls:
        i.shoot()
        c = i.get_coord()
        if c[1] < -20:
            bulls.remove(i)
    #hero_group.rect.x = hero.get_coord()[0]
    #ёhero_group.rect.y = hero.get_coord()[1]

    # laser_sprite.rect.x =

    screen.fill(pg.Color("black"))
    screen.blit(background, background_rect)
    # hero_group.rect
    # for i in range(len(map)):
    # for j in range(len(map[0])):
    # screen.set_at((j, i), (int(map[i][j] * 255), int(map[i][j] * 255), int(map[i][j] * 255)))
    # pass
    # if map[i][j] == 1:
    #    screen.set_at((j, i), clr)
    all_sprites.draw(screen)
    bullets.draw(screen)
    clock.tick(FPS)
    # pg.display.flip()
    pg.display.update()
pg.quit()

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
bullets = pg.sprite.Group()
powerups = pg.sprite.Group()

background = load_image("background2.png")
background_rect = background.get_rect()

hero_image = pg.transform.scale(load_image("ship.png"), (
    74, 96)) # размер изображения: 37*48
mini_image_ship = pg.transform.scale(load_image("mini_image_ship.png"), (
    28, 40)) # размер изображения: 14*20
laser_img = pg.transform.scale(load_image("laser.png"), (
    8, 18)) # размер изображения: 4*9
sprite_group, hero_group = pg.sprite.Group(), pg.sprite.Sprite(all_sprites)
hero_group.image = hero_image



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
#map2 = blur(map2, 20)
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
#map2 = ship()
#map = []

map = generate(32,32,4,3)

for i in range(len(map)):
    for j in range(len(map[0])):
        map[i][j] **= 4
#for i in map2:
#    map.append(i[::-1]+i)

#pprint(map)

#map = upscale(map,16,16)
clr = (200,200,200)
hero = Hero(220, 500, 5, 2, 0, 5, 10)
hero_group.rect.x = hero.get_coord()[0]
hero_group.rect.y = hero.get_coord()[1]

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
            elif event.key == pg.K_p:
                pause = True
            elif event.key == pg.K_UP or event.key == pg.K_w:
                hero.move("up")
            elif event.key == pg.K_DOWN or event.key == pg.K_s:
                hero.move("down")
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                hero.move("left")
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                hero.move("right")
            elif event.key == pg.K_SPACE:
                hero.shoot(hero.get_coord()[0],hero.get_coord()[1],-1,2,2)

    screen.fill(pg.Color("black"))
    screen.blit(background, background_rect)
    # hero_group.rect
    for i in range(len(map)):
        for j in range(len(map[0])):
            #screen.set_at((j, i), (int(map[i][j] * 255), int(map[i][j] * 255), int(map[i][j] * 255)))
            pass
            #if map[i][j] == 1:
            #    screen.set_at((j, i), clr)
    all_sprites.draw(screen)
    clock.tick(FPS)
    #pg.display.flip()
    pg.display.update()
pg.quit()

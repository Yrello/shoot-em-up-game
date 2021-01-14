import os
import pygame
import sys
import random
from Hero import *
size = width, height = 500, 700
screen = pygame.display.set_mode(size)
FPS = 60

clock = pygame.time.Clock()


def create_enemy():
    #enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def start_screen():
    intro_text = ["Пауза игры на [P]",
                  "Чтобы начать игру, нажмите на любую кнопку"]

    st_background = pygame.transform.scale(load_image(
        'start_background.png'), (width, height))

    screen.blit(st_background, (0, 0))
    font = pygame.font.Font(None, 30)
    x, y = width / 2, height / 2

    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.midtop = (x, y)
        y += 40
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    all_sprites = pygame.sprite.Group()

    game_over_image = load_image("gameover.png")
    game_over_image = pygame.transform.scale(game_over_image, (156, 76))
    game_over = pygame.sprite.Sprite(all_sprites)
    game_over.image = game_over_image
    game_over.rect = game_over.image.get_rect()

    game_over.rect.x, game_over.rect.y = (175, 300)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(120)


background = load_image("background.png")
background_rect = background.get_rect()

hero_image = pygame.transform.scale(load_image("ship.png"), (
    74, 96)) # размер изображения: 37*48
mini_image_ship = pygame.transform.scale(load_image("mini_image_ship.png"), (
    28, 40)) # размер изображения: 14*20
laser_img = pygame.transform.scale(load_image("laser.png"), (
    8, 18)) # размер изображения: 4*9

# 16*16
gun_img = pygame.transform.scale(load_image("gun.png"), (32, 32))
shield_img = pygame.transform.scale(load_image("shield.png"), (32, 32))
speed_img = pygame.transform.scale(load_image("speed.png"), (32, 32))

sprite_group, hero_group = pygame.sprite.Group(), pygame.sprite.Group()

running = True
start_screen()

all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()

hero = Hero()
all_sprites.add(hero)

for i in range(8):
    create_enemy()

score = 0
clock.tick(FPS)

pause = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_p:
                pause = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                move(hero, "up")
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                move(hero, "down")
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move(hero, "left")
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move(hero, "right")
            elif event.key == pygame.K_SPACE:
                hero.shoot()

        if pause:
            while pause:
                for p_event in pygame.event.get():
                    if p_event.type == pygame.KEYDOWN:
                        if p_event.key == pygame.K_ESCAPE:
                            running = False
                            break
                        elif p_event.key == pygame.K_p:
                            pause = False

                font = pygame.font.Font(None, 30)
                pause_color = (255, 255, 255)
                pause_rendered = font.render('Pause', 2, pause_color)
                coords_p = (200, 100)
                screen.blit(pause_rendered, coords_p)
                pygame.display.flip()

    all_sprites.update()

    # попадания во врагов
    for i in pygame.sprite.groupcollide(enemies, bullets, True, True):
        score += 50 - i.radius
        all_sprites.add(Enemy(enemies, image, pos, health, damage))
        if random.random() > 0.9:
            powerup = Powerups(i.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)
        create_enemy()

    # попадания в корабль
    for i in pygame.sprite.spritecollide(
            hero, enemies, True, pygame.sprite.collide_circle):
        hero.shield -= i.radius * 2
        all_sprites.add(Hero(
            hero_group, hero_image, hero_pos, hero_health, hero_damage))
        create_enemy()
        if hero.shield <= 0:
            hero.hide()
            hero.lives -= 1
            hero.shield = 100

    for i in pygame.sprite.spritecollide(hero, powerups, True):
        if i.type == 'gun':
            hero.powerup()
        elif i.type == 'speed':
            hero.speed += 5
        elif i.type == 'shield':
            hero.shield += random.randrange(10, 30)
            if hero.shield >= 100:
                hero.shield = 100

    if hero.lives == 0:
        running = False
    screen.fill((0, 0, 0))
    screen.blit(background, (0,0))

    all_sprites.draw(screen)

    font = pygame.font.Font(pygame.font.match_font('arial'), 18)
    text = font.render(str(score), True, pygame.Color('white'))
    text_rect = text.get_rect()
    text_rect.midtop = (160, height - 25)
    screen.blit(text, text_rect)

    for i in range(hero.lives):
        img_rect = hero.get_rect()
        img_rect.x = width - 100 + 30 * i
        img_rect.y = height - 40
        screen.blit(mini_image_ship, img_rect)

    fill = (max(hero.shield, 0) / 100) * 100
    outline_rect = pygame.Rect(5, height - 20, 100, 10)
    fill_rect = pygame.Rect(5, height - 20, fill, 10)
    pygame.draw.rect(screen, (73, 220, 120), fill_rect)
    pygame.draw.rect(screen, pygame.Color('white'), outline_rect, 2)

    pygame.display.flip()
end_screen()
pygame.quit()

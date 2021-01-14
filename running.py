import os
import pygame
import sys
import random
from Hero import *

def create_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)


size = width, height = 500, 500
screen = pygame.display.set_mode(size)
FPS = 60

clock = pygame.time.Clock()
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

        if pause is True:
            screen.fill(pygame.Color('black'))
            font = pygame.font.Font(None, 30)
            pause_color = (255, 0, 0)
            pause_rendered = font.render('Pause', 1, pause_color)
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
        all_sprites.add(Hero(hero_group, hero_image, hero_pos, hero_health, hero_damage))
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

    all_sprites.draw(screen)

    font = pygame.font.Font(None, 20)
    text_surface = font.render(str(score), True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (width / 2, 10)
    screen.blit(text_surface, text_rect)

    for i in range(hero.lives):
        img_rect = mini_image_ship.get_rect()
        img_rect.x = width - 100 + 30 * i
        img_rect.y = 5
        screen.blit(mini_image_ship, img_rect)

    fill = (max(hero.shield, 0) / 100) * 100
    outline_rect = pygame.Rect(5, 5, 100, 100)
    fill_rect = pygame.Rect(5, 5, fill, 100)
    pygame.draw.rect(screen, (255, 0, 0), fill_rect)
    pygame.draw.rect(screen, (0, 0, 0), outline_rect, 2)

    pygame.display.flip()
end_screen()
pygame.quit()

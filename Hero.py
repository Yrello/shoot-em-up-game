import pygame as pg
import random as rnd

class Hero(pg.sprite.Sprite):

    def __init__(self, x, y, hp, v, a, sp, damage, image, *group):
        super(Hero, self).__init__(*group)
        self.x = x
        self.y = y
        self.hp = hp
        self.v = v
        self.a = a
        self.sp = sp  # mb it will be shield points smts
        self.damage = damage
        self.ss = pg.mixer.Sound('audio/laser.wav')
        self.image = image
        self.rect = self.image.get_rect()
        self.group = group

    def debug(self):
        print(self.v)

    def get_dir(self, dir):
        self.dir = dir
        if self.dir == 'up':
            self.v[1] -= 1
        if self.dir == 'down':
            self.v[1] += 1
        if self.dir == 'left':
            self.v[0] -= 1
        if self.dir == 'right':
            self.v[0] += 1
        if self.dir == 'none':
            self.v = [0, 0]

    def set_dir(self, a, n):
        self.v[a] = n

    def move(self):
        if pg.sprite.spritecollideany(self, ):
            print('AAA')

        if self.a[0] != 0 or self.a[1] != 0:
            self.a[0] /= 1.2 ** 0.5
            self.a[1] /= 1.2 ** 0.5
        if abs(self.a[0]) < 5:
            self.a[0] += self.v[0] / 5
        if abs(self.a[1]) < 1.5:
            self.a[1] += self.v[1] / 5

        self.x, self.y = self.x + self.sp * self.a[0], self.y + self.sp * self.a[1]
        self.rect.x = self.x
        self.rect.y = self.y
        '''if abs(self.v[0]) == abs(self.v[1]):
            self.x /= 2**0.5
            self.y /= 2**0.5'''

    def get_coord(self):
        return (self.x, self.y)

    def shoot(self, image, x, y, dir, dmg, sp, angsp, group):
        b = Bullet(image, x, y, dir, dmg, sp, angsp, group)
        self.ss.play()
        # b.shoot()  # dir 1/-1, damage, speed
        return b

    def get_info(self):
        return [self.x, self.y, self.hp, self.damage]


class Bullet(pg.sprite.Sprite):
    def __init__(self, image, x, y, dir, dmg, sp, angsp, *groups):
        super().__init__(*groups)
        self.dir = dir
        self.dmg = dmg
        self.sp = sp
        self.angsp = angsp
        self.x = x + 35
        self.y = y
        self.image = image
        self.rect = self.image.get_rect()

    def shoot(self):
        self.y += self.sp * self.dir
        self.x += self.angsp
        self.rect.x = self.x
        self.rect.y = self.y

        # print(self.x,self.y)
        # print('boom')

    def get_coord(self):
        return self.x, self.y

    def get_sprite(self):
        return self.sprite


class Enemy(pg.sprite.Sprite):
    def __init__(self, image, x, y, hp, v, a, sp, damage, sprite, *groups):
        super().__init__(*groups)
        self.x = x
        self.y = y
        self.hp = hp
        self.v = v
        self.a = a
        self.delta = rnd.randint(-30,30)/15
        #self.delta = self.delta / 2 - self.delta
        self.sp = sp + self.delta
        self.damage = damage
        self.image = image
        self.sprite = sprite
        self.rect = self.image.get_rect()
        print(self.delta)
    def get_coord(self):
        return self.x, self.y

    def move(self, plx, ply):
        deltax = rnd.randint(1, 10) / 10
        deltax = deltax / 2 - deltax
        if self.x < plx + deltax:
            self.x += self.sp
        if self.x > plx + deltax:
            self.x -= self.sp
        if self.y < 50 + self.delta * 30:
            self.y += self.sp
        self.rect.x = self.x
        self.rect.y = self.y




class EnemyAI:
    def __init__(self):
        self.lst = []
        self.dif = 0
        self.std_dif = 11
        self.enemy_aggression = 0.5

    def get_enemy_info(self, a):
        return a.get_coord()

    def get_screen_info(self, game_time, enemy_list, player_info, bullet_list):
        self.time = game_time
        #self.lst = enemy_list
        self.player_info = player_info
        self.bullets = bullet_list

    def get_enemy_list(self):
        return self.lst

    def difficult_level_calc(self):
        self.dif = len(self.lst) + len(self.bullets) / 5 + 1 / (self.player_info[2]) + 1 / (self.player_info[3]) + \
                   self.time / 100 + self.enemy_aggression ** 2  # 7 + 12/5 + 1/2 + 1/5 + 1

    def difficult_level_change(self,img, sprite, group):
        if self.dif < self.std_dif:
            if rnd.randint(0, 2) == 0:
                e = Enemy(img, 30 + rnd.randint(-20, 60), -30, 3, [0, 0], [0, 0], 2, 2, sprite, group)
                self.lst.append(e)
            else:
                self.enemy_aggression += 0.15
        if self.dif > self.std_dif:
            self.std_dif -= 0.07

    def act(self, plcoord):
        #print(self.lst)
        for i in self.lst:
            i.move(plcoord[0],plcoord[1])
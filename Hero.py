class Hero:

    def __init__(self, x, y, hp, v, a, sp, damage):
        self.x = x
        self.y = y
        self.hp = hp
        self.v = v
        self.a = a
        self.sp = sp  # mb it will be shield points smts
        self.damage = damage

    def move(self, dir):
        self.dir = dir
        if self.dir == 'up':
            self.v = (0, 1)
        if self.dir == 'down':
            self.v = (0, -1)
        if self.dir == 'left':
            self.v = (-1, 0)
        if self.dir == 'right':
            self.v = (1, 0)
        if self.dir == 'none':
            self.v = (0, 0)

        self.x, self.y = self.sp * self.v[0], self.sp * self.v[1]

    def get_coord(self):
        return self.x, self.y

    def shoot(self, x, y, dir, dmg, sp, angsp=0):
        b = Bullet(x, y, dir, dmg, sp, angsp)
        b.shoot()  # dir 1/-1, damage, speed


class Bullet():
    def __init__(self, x, y, dir, dmg, sp, angsp=0):
        self.dir = dir
        self.dmg = dmg
        self.sp = sp
        self.angsp = angsp
        self.x = x
        self.y = y

    def shoot(self):
        self.y += self.sp * self.dir
        self.x += self.angsp

    def get_coord(self):
        return self.x, self.y


class Enemy(Hero):
    def __init__(self, x, y, hp, v, a, sp, damage):
        super().__init__(x, y, hp, v, a, sp, damage)
    def move(self, plx, ply):
        pass

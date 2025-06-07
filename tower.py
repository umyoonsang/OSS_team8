import pygame
import math

class Tower:
    name = "Basic"
    description = "Standard tower"
    value = 100
    sprite_location = "assets/basic_tower.png"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = 15
        self.cooldown = 60  # frames
        self.counter = 0

    def find_target(self, enemies):
        for enemy in enemies:
            dist = math.hypot(enemy.x - self.x, enemy.y - self.y)
            if dist <= self.range:
                return enemy
        return None

    def shoot(self, target):
        return Bullet(self.x, self.y, target, self.damage)

    def update(self, enemies, bullets):
        self.counter += 1
        if self.counter >= self.cooldown:
            target = self.find_target(enemies)
            if target:
                bullet = self.shoot(target)
                bullets.append(bullet)
                self.counter = 0

    def draw(self, win):
        image = pygame.image.load(self.sprite_location)
        image = pygame.transform.scale(image, (50, 50))
        win.blit(image, (self.x - 25, self.y - 25))
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), self.range, 1)


class Bullet:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 6
        self.damage = damage
        self.hit = False
        self.slow_effect = False

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist > self.speed:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist
        else:
            self.target.hp -= self.damage
            if self.slow_effect:
                self.target.speed *= 0.5  # 감속 적용
            self.hit = True

    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (int(self.x), int(self.y)), 5)


class SniperTower(Tower):
    name = "Sniper"
    description = "Long range, high damage"
    value = 200
    sprite_location = "assets/sniper_tower.png"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 200
        self.damage = 50
        self.cooldown = 120

    def draw(self, win):
        image = pygame.image.load(self.sprite_location)
        image = pygame.transform.scale(image, (50, 50))
        win.blit(image, (self.x - 25, self.y - 25))
        pygame.draw.circle(win, (255, 255, 0), (self.x, self.y), self.range, 1)


class SlowTower(Tower):
    name = "Slow"
    description = "Slows enemies"
    value = 150
    sprite_location = "assets/slow_tower.png"

    def __init__(self, x, y):
        super().__init__(x, y)
        self.range = 120
        self.damage = 5
        self.cooldown = 80

    def shoot(self, target):
        bullet = super().shoot(target)
        bullet.slow_effect = True
        return bullet

    def draw(self, win):
        image = pygame.image.load(self.sprite_location)
        image = pygame.transform.scale(image, (50, 50))
        win.blit(image, (self.x - 25, self.y - 25))
        pygame.draw.circle(win, (0, 255, 255), (self.x, self.y), self.range, 1)

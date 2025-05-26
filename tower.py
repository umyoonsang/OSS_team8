import pygame
import math

class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.damage = 15
        self.cooldown = 60  # 프레임 단위
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
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), 15)             # 타워 본체
        pygame.draw.circle(win, (0, 0, 255), (self.x, self.y), self.range, 1)  # 사정거리

class Bullet:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.speed = 6
        self.damage = damage
        self.hit = False

    def move(self):
        dx = self.target.x - self.x
        dy = self.target.y - self.y
        dist = math.hypot(dx, dy)
        if dist > self.speed:
            self.x += self.speed * dx / dist
            self.y += self.speed * dy / dist
        else:
            self.target.hp -= self.damage
            self.hit = True

    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), (int(self.x), int(self.y)), 5)

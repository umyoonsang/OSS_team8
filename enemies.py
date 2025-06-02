import pygame
import math

class Enemy:
    def __init__(self, x, y, path, speed=2, hp=100):
        self.x = x
        self.y = y
        self.path = path
        self.path_index = 0
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.alive = True

    def move(self):
        if self.path_index < len(self.path):
            tx, ty = self.path[self.path_index]
            dx = tx - self.x
            dy = ty - self.y
            dist = math.hypot(dx, dy)
            if dist > self.speed:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist
            else:
                self.path_index += 1
        else:
            self.alive = False

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.alive = False

    def draw(self, win):
        pygame.draw.circle(win, (0, 200, 0), (int(self.x), int(self.y)), 15)
        bar_width = 30
        bar_height = 5
        fill = max(self.hp, 0) / self.max_hp * bar_width
        pygame.draw.rect(
            win, (200, 0, 0),
            (int(self.x - bar_width/2), int(self.y - 25), bar_width, bar_height)
        )
        pygame.draw.rect(
            win, (0, 200, 0),
            (int(self.x - bar_width/2), int(self.y - 25), int(fill), bar_height)
        )

    def update(self):
        if self.alive:
            self.move()

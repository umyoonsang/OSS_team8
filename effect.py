import pygame
from UI import *

class ShootEffect(pygame.sprite.Sprite):
    def __init__(self, colour, startpos, endpos, timeout, screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.colour = colour
        self.startpos = startpos
        self.endpos = endpos
        self.timeout = timeout
        self.image = pygame.Surface(screen_size, pygame.SRCALPHA)
        pygame.draw.line(self.image, self.colour, self.startpos, self.endpos, 3)
        self.rect = self.image.get_rect()
        self.time_alive = 0

    def update(self):
        self.time_alive += 1
        if self.time_alive > self.timeout:
            self.kill()


class SpriteSheet(pygame.sprite.Sprite):
    def __init__(self, pos, sprite_location, frame_cols=5, frame_rows=5):
        super().__init__()
        self.spritesheet = pygame.image.load(sprite_location).convert_alpha()
        self.frame_cols = frame_cols
        self.frame_rows = frame_rows
        self.frame_width = self.spritesheet.get_width() // frame_cols
        self.frame_height = self.spritesheet.get_height() // frame_rows
        self.frames = frame_cols * frame_rows
        self.current_frame = 0

        self.image = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        if self.current_frame >= self.frames:
            self.kill()
            return

        col = self.current_frame % self.frame_cols
        row = self.current_frame // self.frame_cols
        frame_rect = pygame.Rect(
            col * self.frame_width, row * self.frame_height,
            self.frame_width, self.frame_height
        )

        self.image.fill((0, 0, 0, 0))  # clear with transparency
        self.image.blit(self.spritesheet, (0, 0), frame_rect)

        self.current_frame += 1


import pygame
import time

class WaveManager:
    def __init__(self, spawn_callback):
        self.wave_number = 0
        self.enemies_to_spawn = 0
        self.enemies_spawned = 0
        self.enemies_alive = 0
        self.spawn_delay = 1000  # milliseconds between spawns
        self.last_spawn_time = 0
        self.wave_in_progress = False
        self.spawn_callback = spawn_callback  # 함수를 통해 적 객체를 생성하도록 위임

    def start_next_wave(self):
        if self.wave_number < 10:  # 최대 10웨이브까지만
            self.wave_number += 1
            self.enemies_to_spawn = 5 + self.wave_number * 2  # wave마다 적 수 증가
            self.enemies_spawned = 0
            self.enemies_alive = 0
            self.last_spawn_time = pygame.time.get_ticks()
            self.wave_in_progress = True
            print(f"Wave {self.wave_number} 시작!")

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.wave_in_progress:
            if self.enemies_spawned < self.enemies_to_spawn:
                if current_time - self.last_spawn_time > self.spawn_delay:
                    self.spawn_callback(self.wave_number)
                    self.enemies_spawned += 1
                    self.enemies_alive += 1
                    self.last_spawn_time = current_time
            elif self.enemies_alive == 0:
                self.wave_in_progress = False
                print(f"Wave {self.wave_number} 완료!")

    def enemy_killed(self):
        self.enemies_alive -= 1

    def is_wave_cleared(self):
        return not self.wave_in_progress

    def get_wave_number(self):
        return self.wave_number
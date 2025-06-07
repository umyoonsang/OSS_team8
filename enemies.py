import pygame

class Enemy:
    def __init__(self, x, y, path, hp=100):
        # 초기 위치 및 경로 설정
        self.x = x
        self.y = y
        self.path = path
        self.path_index = 0

        # ✅ 적 이미지 불러오기
        raw_img = pygame.image.load("./assets/enemy1.png").convert_alpha()
        self.img = pygame.transform.smoothscale(raw_img, (50, 50))  # 폭발 이미지와 동일한 크기

        # 체력 설정
        self.hp = hp
        self.max_hp = hp
        self.alive = True
        self.speed = 1.0

        # ✅ 폭파 애니메이션 관련 변수
        self.exploding = False
        self.explosion_frames = self.load_explosion_frames()
        self.explosion_index = 0
        self.explosion_frame_delay = 2
        self.explosion_frame_count = 0
        self.gold_given = False  # 골드 중복 지급 방지

    def load_explosion_frames(self):
        # ✅ 250x250 스프라이트 시트를 50x50 크기로 25프레임 자르기
        sprite_sheet = pygame.image.load("./assets/explosion.png").convert_alpha()
        frames = []
        frame_width = 50
        frame_height = 50
        for y in range(5):
            for x in range(5):
                rect = pygame.Rect(x * frame_width, y * frame_height, frame_width, frame_height)
                frames.append(sprite_sheet.subsurface(rect))
        return frames

    def draw(self, win):
        # ✅ 폭발 중이라면 애니메이션 그리기
        if self.exploding:
            if self.explosion_index < len(self.explosion_frames):
                frame = self.explosion_frames[self.explosion_index]
                win.blit(frame, (self.x - frame.get_width() // 2, self.y - frame.get_height() // 2))
                self.explosion_frame_count += 1
                if self.explosion_frame_count >= self.explosion_frame_delay:
                    self.explosion_index += 1
                    self.explosion_frame_count = 0
            return  # 폭발 중이면 적 이미지는 그리지 않음

        # ✅ 적 이미지 그리기 (중심 기준)
        win.blit(self.img, (self.x - self.img.get_width() // 2, self.y - self.img.get_height() // 2))

        # 체력 바 그리기
        bar_width = 40
        bar_height = 6
        health_ratio = max(self.hp / self.max_hp, 0)
        pygame.draw.rect(win, (255, 0, 0), (self.x - bar_width // 2, self.y - 40, bar_width, bar_height))
        pygame.draw.rect(win, (0, 255, 0), (self.x - bar_width // 2, self.y - 40, bar_width * health_ratio, bar_height))

    def update(self):
        # ✅ 처치된 적은 폭발 애니메이션만 실행
        if not self.alive:
            if not self.exploding:
                self.exploding = True
            return

        # 경로를 따라 이동
        if self.path_index < len(self.path):
            target_x, target_y = self.path[self.path_index]
            dx = target_x - self.x
            dy = target_y - self.y
            dist = (dx ** 2 + dy ** 2) ** 0.5
            if dist < self.speed:
                self.path_index += 1
            else:
                self.x += self.speed * dx / dist
                self.y += self.speed * dy / dist

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            self.alive = False

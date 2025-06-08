import pygame

# 색상 상수 정의
TEXT_COLOUR = pygame.Color("white")
TOWER_BORDER = pygame.Color("gray")
TOWER_SELECTED = pygame.Color("cyan")

BUTTON_COLOUR = pygame.Color("darkgreen")
BUTTON_DISABLED_COLOUR = pygame.Color("darkgray")
MOUSE_SELECTOR_COLOUR = pygame.Color("yellow")
PATH_COLOUR = pygame.Color("red")
FRAME_COLOUR = pygame.Color("dimgray")

class Button:
    def __init__(self, rect, text, bg_color, text_color, font_size):
        self.rect = rect
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_size = font_size

        # ✅ 안전한 기본 시스템 폰트 사용
        self.font = pygame.font.Font(None, self.font_size)
        self.image = None

    def create_image(self):
        # 버튼 배경 Surface
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(self.bg_color)

        # 텍스트 렌더링
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surface, text_rect)

class TextDisplay:
    def __init__(self, rect, text, text_colour, text_size):
        self.rect = rect
        self.text = text
        self.text_colour = text_colour
        self.text_size = text_size

        # ✅ 완전 투명 배경이 가능한 Surface 생성
        self.image = pygame.Surface(rect.size, pygame.SRCALPHA)

    def create_image(self):
        self.image.fill((0, 0, 0, 0))  # 투명한 배경
        font = pygame.font.Font(None, self.text_size)
        text_surf = font.render(self.text, True, self.text_colour)
        text_rect = text_surf.get_rect(center=(self.rect.width // 2, self.rect.height // 2))
        self.image.blit(text_surf, text_rect)

class Shop:
    def __init__(self, screen, rect, towers):
        self.rect = rect
        self.towers = towers

        # ✅ 독립적인 Surface 생성 (subsurface ❌)
        self.image = pygame.Surface(rect.size)

        # 상단 제목 표시
        self.title = TextDisplay(pygame.Rect(20, 10, 300, 50), "Shop", TEXT_COLOUR, 40)
        self.title.create_image()

        # 타워 선택 버튼 생성
        self.buttons = []
        for i, tower in enumerate(towers):
            text = tower.__class__.__name__
            btn = Button(
                pygame.Rect(20, 70 + i * 80, 200, 60),
                text,
                pygame.Color("green"),
                TEXT_COLOUR,
                25
            )
            btn.create_image()  # ✅ 텍스트 포함된 버튼 이미지 생성
            self.buttons.append(btn)

    def render(self, selected):
        # 배경 채우기 (검정색)
        self.image.fill((0, 0, 0))
        self.image.blit(self.title.image, self.title.rect)

        # 버튼들 렌더링
        for i, btn in enumerate(self.buttons):
            self.image.blit(btn.image, btn.rect)

            # 선택된 버튼은 파란 테두리
            if i == selected:
                pygame.draw.rect(self.image, TOWER_SELECTED, btn.rect, 3)
            else:
                pygame.draw.rect(self.image, TOWER_BORDER, btn.rect, 2)

    def button_pressed(self, mouse_pos):
        # 마우스 좌표가 어떤 버튼 안에 있는지 확인
        for i, btn in enumerate(self.buttons):
            if btn.rect.collidepoint(mouse_pos):
                return i
        return -1

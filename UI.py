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

# 버튼 사이즈 상수
BUTTON_WIDTH = 180  # 초록 박스 너비
BUTTON_HEIGHT = 50  # 버튼 높이
VERTICAL_SPACING = 100  # 버튼 간 세로 간격

class Button:
    def __init__(self, rect, text, bg_color, text_color, font_size):
        self.rect = rect
        self.text = text
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_size = font_size
        self.font = pygame.font.Font(None, self.font_size)
        self.image = None

    def create_image(self):
        self.image = pygame.Surface(self.rect.size)
        self.image.fill(self.bg_color)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.rect.width//2, self.rect.height//2))
        self.image.blit(text_surf, text_rect)

class TextDisplay:
    def __init__(self, rect, text, text_colour, text_size):
        self.rect = rect
        self.text = text
        self.text_colour = text_colour
        self.text_size = text_size
        self.image = pygame.Surface(rect.size, pygame.SRCALPHA)

    def create_image(self):
        self.image.fill((0,0,0,0))
        font = pygame.font.Font(None, self.text_size)
        text_surf = font.render(self.text, True, self.text_colour)
        text_rect = text_surf.get_rect(center=(self.rect.width//2, self.rect.height//2))
        self.image.blit(text_surf, text_rect)

class Shop:
    def __init__(self, screen, rect, towers):
        self.screen = screen
        self.rect = rect
        self.towers = towers
        self.image = pygame.Surface(rect.size)
        self.font_small = pygame.font.Font(None, 24)
        # 제목
        self.title = TextDisplay(pygame.Rect(20,10,300,50), "Shop", TEXT_COLOUR, 40)
        self.title.create_image()
        # 각 타워 버튼 및 데이터
        self.buttons = []
        self.tower_images = []
        self.descriptions = []
        self.cost_texts = []
        for i, tower in enumerate(towers):
            y = 70 + i * VERTICAL_SPACING
            btn = Button(
                pygame.Rect(20, y, BUTTON_WIDTH, BUTTON_HEIGHT),
                tower.__class__.__name__,
                BUTTON_COLOUR,
                TEXT_COLOUR,
                25
            )
            btn.create_image()
            self.buttons.append(btn)
            # 이미지
            img = pygame.image.load(tower.sprite_location)
            img = pygame.transform.scale(img, (50,50))
            self.tower_images.append(img)
            # 설명
            desc = self.font_small.render(tower.description, True, TEXT_COLOUR)
            self.descriptions.append(desc)
            # 비용
            cost = self.font_small.render(f"Cost: {tower.value}", True, TEXT_COLOUR)
            self.cost_texts.append(cost)

    def render(self, selected_index):
        self.image.fill((0,0,0))
        # 제목
        self.image.blit(self.title.image, self.title.rect)
        # 각 버튼 및 정보
        for i, btn in enumerate(self.buttons):
            self.image.blit(btn.image, btn.rect)
            # 선택 테두리
            color = TOWER_SELECTED if i == selected_index else TOWER_BORDER
            pygame.draw.rect(self.image, color, btn.rect, 3 if i == selected_index else 2)
            # 이미지 위치
            img_rect = self.tower_images[i].get_rect(topleft=(btn.rect.right+10, btn.rect.y))
            self.image.blit(self.tower_images[i], img_rect)
            # 설명 위치
            desc_rect = self.descriptions[i].get_rect(topleft=(img_rect.right+10, img_rect.y))
            self.image.blit(self.descriptions[i], desc_rect)
            # 비용 위치
            cost_rect = self.cost_texts[i].get_rect(topleft=(img_rect.right+10, desc_rect.bottom+5))
            self.image.blit(self.cost_texts[i], cost_rect)
        # Shop 창 렌더
        self.screen.blit(self.image, self.rect)

    def button_pressed(self, mouse_pos):
        # Shop 좌표 기준 상대 위치 mouse_pos
        for idx, btn in enumerate(self.buttons):
            if btn.rect.collidepoint(mouse_pos):
                return idx
        return -1

import pygame
import math

# 색상 설정
FRAME_COLOUR = pygame.Color("BLACK")
BACKGROUND_COLOUR = pygame.Color("GRAY")
BUTTON_COLOUR = pygame.Color(66, 235, 244)
TEXT_COLOUR = pygame.Color("WHITE")
SHOP_BACKGROUND_COLOUR = pygame.Color(60, 60, 60)
BUTTON_DISABLED_COLOUR = pygame.Color("RED")
PATH_COLOUR = pygame.Color("BLUE")
MOUSE_SELECTOR_COLOUR = pygame.Color("WHITE")

GRID_SIZE = 50

# 유틸리티
def adjustCoordsByOffset(coords, offset):
    return (coords[0] - offset[0], coords[1] - offset[1])

# ---------------------------
# Button
# ---------------------------
class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, background_colour, text_colour, text_size):
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface((rect.width, rect.height))
        self.text = text
        self.__background_colour = background_colour
        self.text_colour = text_colour
        self.text_size = text_size
        self.create_image()

    @property
    def background_colour(self):
        return self.__background_colour

    @background_colour.setter
    def background_colour(self, colour):
        self.__background_colour = colour
        self.create_image()

    def contains(self, point):
        return self.rect.collidepoint(point)

    def create_image(self):
        self.image.fill(self.background_colour)
        font = pygame.font.Font(None, self.text_size)
        text_surf = font.render(self.text, True, self.text_colour)
        self.image.blit(text_surf, (
            self.rect.width // 2 - text_surf.get_width() // 2,
            self.rect.height // 2 - text_surf.get_height() // 2
        ))

# ---------------------------
# TextDisplay
# ---------------------------
class TextDisplay(pygame.sprite.Sprite):
    def __init__(self, rect, text, text_colour, text_size):
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        self.__text = text
        self.text_colour = text_colour
        self.text_size = text_size
        self.create_image()

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new_text):
        self.__text = new_text
        self.create_image()

    def create_image(self):
        self.image.fill((0, 0, 0, 0))
        font = pygame.font.Font(None, self.text_size)
        text_surf = font.render(self.text, True, self.text_colour)
        self.image.blit(text_surf, (
            self.rect.width // 2 - text_surf.get_width() // 2,
            self.rect.height // 2 - text_surf.get_height() // 2
        ))

# ---------------------------
# ShopButton
# ---------------------------
class ShopButton(pygame.sprite.Sprite):
    def __init__(self, tower_model, pos, text_size, text_colour):
        super().__init__()
        self.model = tower_model
        sprite = pygame.image.load(tower_model.sprite_location).convert_alpha()
        sprite = pygame.transform.scale(sprite, (50, 50))

        font = pygame.font.Font(None, text_size)
        text_surf = font.render(tower_model.name, True, text_colour)

        width = sprite.get_width() + text_surf.get_width() + 15
        height = max(sprite.get_height(), text_surf.get_height()) + 10
        self.rect = pygame.Rect(pos, (width, height))
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        self.text = tower_model.name
        self.sprite = sprite
        self.text_surf = text_surf
        self.text_colour = text_colour
        self.text_size = text_size

        self.create_image()

    def create_image(self):
        self.image.fill((0, 0, 0, 0))
        self.image.blit(self.sprite, (5, 5))
        self.image.blit(self.text_surf, (self.sprite.get_width() + 10, 5))

    def contains(self, point):
        return self.rect.collidepoint(point)

# ---------------------------
# Shop
# ---------------------------
class Shop:
    def __init__(self, screen, rect, tower_models):
        self.rect = rect
        self.image = screen.subsurface(rect)
        self.title = TextDisplay(pygame.Rect(20, 10, 300, 50), "Shop", TEXT_COLOUR, 40)
        self.tower_models = tower_models
        self.buttons = []

        y = 80  # 버튼 시작 위치
        for tower in tower_models:
            button = ShopButton(tower, (20, y), 24, TEXT_COLOUR)
            self.buttons.append(button)
            y += 70

        # 설명 박스를 TextDisplay로 구성
        info_x = 200
        self.description_rects = [
            TextDisplay(pygame.Rect(info_x, 80, 180, 30), "", TEXT_COLOUR, 20),
            TextDisplay(pygame.Rect(info_x, 115, 180, 60), "", TEXT_COLOUR, 18)
        ]

    def render(self, selected_index):
        self.image.fill(SHOP_BACKGROUND_COLOUR)
        self.image.blit(self.title.image, self.title.rect)

        for i, button in enumerate(self.buttons):
            self.image.blit(button.image, button.rect)
            if i == selected_index:
                pygame.draw.rect(self.image, MOUSE_SELECTOR_COLOUR, button.rect, 2)

        # 선택된 타워 정보 표시
        self.description_rects[0].text = f"Cost: {self.tower_models[selected_index].value}"
        self.description_rects[1].text = self.tower_models[selected_index].description

        for popup in self.description_rects:
            self.image.blit(popup.image, popup.rect)

    def button_pressed(self, point):
        for i, button in enumerate(self.buttons):
            if button.contains(point):
                return i
        return -1

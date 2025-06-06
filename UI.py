import pygame
import math

# -----------------------------
# 색상 설정 및 게임 관련 상수 정의
# -----------------------------
FRAME_COLOUR = pygame.Color("BLACK")      # 테두리 색상
BACKGROUND_COLOUR = pygame.Color("GRAY")  # 배경 색상
BUTTON_COLOUR = pygame.Color(66, 235, 244, 0)  # 버튼 색상 (하늘색)
TEXT_COLOUR = pygame.Color("WHITE")       # 텍스트 색상
SHOP_BACKGROUND_COLOUR = pygame.Color(60, 60, 60, 0)  # 상점 배경 색상
BUTTON_DISABLED_COLOUR = pygame.Color("RED")         # 비활성화된 버튼 색상
PATH_COLOUR = pygame.Color("BLUE")        # 경로 색상
MOUSE_SELECTOR_COLOUR = pygame.Color("WHITE")  # 마우스 선택자 색상

# -----------------------------
# 게임 전역 설정
# -----------------------------
GRID_SIZE = 50   # 격자 크기

# 방향 상수
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# 게임 상태
STATE_MAIN_MENU = 1
STATE_PRE_WAVE = 2
STATE_WAVE = 3
STATE_PAUSED = 4
STATE_GAME_OVER = 5

# 사용자 정의 이벤트
ENEMY_REACHED_END = pygame.USEREVENT+1  # 적이 끝까지 도달했을 때 이벤트
ENEMY_KILLED = pygame.USEREVENT+2       # 적이 죽었을 때 이벤트
TOWER_BOUGHT = pygame.USEREVENT+3       # 타워 구매 이벤트
EVENT_STATE_CHANGED = pygame.USEREVENT+4  # 상태 변경 이벤트

# -----------------------------
# 유틸리티 함수 정의
# -----------------------------
def negateCoords(coords):
    return tuple([-coords[0], -coords[1]])

def adjustCoordsByOffset(coords, offset):
    return tuple([coords[0]-offset[0], coords[1]-offset[1]])

def posToGridCoords(pos, grid_size):
    return tuple([pos[0] // grid_size, pos[1] // grid_size])

def gridCoordToPos(grid_coord, grid_size):
    return tuple([grid_coord[0]*grid_size + grid_size//2, grid_coord[1]*grid_size + grid_size//2])

def getDistance(pos1, pos2):
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

def getDirection(pos1, pos2):
    if abs(pos1[0]-pos2[0]) > abs(pos1[1]-pos2[1]):
        return LEFT if pos1[0] > pos2[0] else RIGHT
    else:
        return UP if pos1[1] > pos2[1] else DOWN

# -----------------------------
# 경로 클래스 정의
# -----------------------------
# Path 클래스: 게임 내 적이 따라가는 경로를 정의하고 시각화하는 클래스
class Path(pygame.sprite.Sprite):
    def __init__(self, colour, waypoints=[], grid_size=50):
        pygame.sprite.Sprite.__init__(self)
        highest_x = max([pt[0] for pt in waypoints], default=0)
        highest_y = max([pt[1] for pt in waypoints], default=0)
        self.image = pygame.Surface(((highest_x+3)*GRID_SIZE, (highest_y+3)*GRID_SIZE))
        self.image.fill(BACKGROUND_COLOUR)
        self.rect = self.image.get_rect()
        self.colour = colour
        self.waypoints = waypoints
        self.grid_size = grid_size
        self.rectangles = []
        self.generateRectangles()

    def addToPath(self, coords):
        self.waypoints.append(coords)
        self.generateRectangles()

    def generateRectangles(self):
        self.rectangles = []
        for i in range(len(self.waypoints)-1):
            first, second = self.waypoints[i], self.waypoints[i+1]
            top_left = (min(first[0], second[0]), min(first[1], second[1]))
            bottom_right = (max(first[0], second[0]), max(first[1], second[1]))
            rect = pygame.Rect(top_left[0]*self.grid_size,
                               top_left[1]*self.grid_size,
                               (bottom_right[0]+1-top_left[0])*self.grid_size,
                               (bottom_right[1]+1-top_left[1])*self.grid_size)
            pygame.draw.rect(self.image, self.colour, rect)
            self.rectangles.append(rect)

    def contains(self, point):
        return any(rect.collidepoint(point) for rect in self.rectangles)

# -----------------------------
# UI 클래스들 정의
# -----------------------------
# Button 클래스: 클릭 가능한 사각형 버튼을 생성하고 렌더링하는 클래스
class Button(pygame.sprite.Sprite):
    def __init__(self, rect, text, background_colour, text_colour, text_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height))
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
        font = pygame.font.SysFont("Arial", self.text_size)
        text_surf = font.render(self.text, True, self.text_colour)
        self.image.blit(text_surf, (self.rect.width // 2 - text_surf.get_width() // 2,
                                    self.rect.height // 2 - text_surf.get_height() // 2))

# TextDisplay 클래스: 화면에 텍스트를 렌더링하는 UI 요소 클래스
class TextDisplay(pygame.sprite.Sprite):
    def __init__(self, rect, text, text_colour, text_size):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
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
        font = pygame.font.SysFont("Arial", self.text_size)
        text_surf = font.render(self.text, True, self.text_colour)
        self.image.blit(text_surf, (self.rect.width // 2 - text_surf.get_width() // 2,
                                    self.rect.height // 2 - text_surf.get_height() // 2))


# ShopButton 클래스: 상점에서 타워 구매를 위한 버튼. 버튼에 이미지와 이름 표시
class ShopButton(Button):
    def __init__(self, tower_model, pos, text_size, text_colour):
        pygame.sprite.Sprite.__init__(self)
        self.model = tower_model
        sprite = pygame.image.load(tower_model.sprite_location)
        font = pygame.font.SysFont("Arial", text_size)
        text_surf = font.render(tower_model.name, True, text_colour)
        self.rect = pygame.Rect(pos, (text_surf.get_width() + sprite.get_width() + 10, sprite.get_height() + 10))
        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.image.blit(sprite, (0, 5))
        self.image.blit(text_surf, (sprite.get_width() + 10, 0))


# Shop 클래스: 타워 선택 UI를 구성하고 버튼 및 설명 팝업을 관리하는 클래스
class Shop():
    def __init__(self, screen, rect, tower_models):
        self.rect = rect
        self.image = screen.subsurface(rect)
        self.title = TextDisplay(pygame.Rect(50, 50, 300, 80), "Shop", TEXT_COLOUR, 60)
        self.tower_models = tower_models
        self.buttons = []
        self.info_popups = []
        current_y = 250
        for tower in tower_models:
            self.buttons.append(ShopButton(tower, (50, current_y), 50, TEXT_COLOUR))
            self.info_popups.append([
                Button(pygame.Rect(0, 500, 400, 80), "Cost: " + str(tower.value), SHOP_BACKGROUND_COLOUR, TEXT_COLOUR, 30),
                Button(pygame.Rect(0, 580, 400, 80), tower.description, SHOP_BACKGROUND_COLOUR, TEXT_COLOUR, 25)
            ])
            current_y += 100

    def render(self, selected):
        mouse_pos = adjustCoordsByOffset(pygame.mouse.get_pos(), self.image.get_abs_offset())
        self.image.fill(SHOP_BACKGROUND_COLOUR)
        self.image.blit(self.title.image, self.title.rect)
        for button in self.buttons:
            self.image.blit(button.image, button.rect)
        pygame.draw.rect(self.image, MOUSE_SELECTOR_COLOUR, self.buttons[selected].rect, 2)
        for i, button in enumerate(self.buttons):
            if button.contains(mouse_pos):
                for p in self.info_popups[i]:
                    self.image.blit(p.image, p.rect)

    def button_pressed(self, point):
        for i, button in enumerate(self.buttons):
            if button.contains(point):
                return i
        return -1

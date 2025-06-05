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


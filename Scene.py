from UI import *
from Towers import *
from Wave import *
from Enemies import *

# Scene 클래스: 모든 씬의 공통 기능을 정의한 추상 클래스
class Scene:
    def __init__(self, screen_size, screen):
        # 게임 화면 내부에 실제로 그려지는 서브 화면 영역 정의
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.game_screen = screen.subsurface(self.rect)

    def update(self, **kwargs):
        # 프레임마다 상태를 업데이트. 하위 클래스에서 재정의 필요
        pass

    def render(self, **kwargs):
        # 프레임마다 화면을 렌더링. 하위 클래스에서 재정의 필요
        pass

# GameOver 클래스: 게임 오버 화면을 그리는 씬
class GameOver(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect((0, 0), screen_size)
        self.screen = screen.subsurface(self.rect)
        self.title = TextDisplay(pygame.Rect((screen_size[0]//2-300, screen_size[1]//3), (600, 100)), "GAME OVER", TEXT_COLOUR, 100)
        self.survival_message = TextDisplay(pygame.Rect((screen_size[0]//2-300, screen_size[1]//2), (600, 100)), "You survived until wave 999", TEXT_COLOUR, 50)
        self.main_menu_button = Button(pygame.Rect((screen_size[0]//2-225, 2*screen_size[1]//3-50), (450, 100)), "Main Menu", BUTTON_COLOUR, TEXT_COLOUR, 100)

    def render(self, **kwargs):
        # 게임 오버 화면 구성 요소 렌더링
        self.screen.blit(self.title.image, self.title.rect)
        self.screen.blit(self.survival_message.image, self.survival_message.rect)
        self.screen.blit(self.main_menu_button.image, self.main_menu_button.rect)


# MainMenu 클래스: 메인 메뉴 씬 정의
class MainMenu(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(0, 0, screen_size[0], screen_size[1])
        self.menu_screen = screen.subsurface(self.rect)

        # 게임 제목
        self.title = TextDisplay(pygame.Rect(0, 100, screen_size[0], 100), "Tower Defence Game", TEXT_COLOUR, 100)

        # 게임 설명 텍스트
        self.instructions = []
        self.instructions.append(TextDisplay(pygame.Rect(0, 300, screen_size[0], 65), "Left click a free space to place a tower", TEXT_COLOUR, 50))
        self.instructions.append(TextDisplay(pygame.Rect(0, 365, screen_size[0], 65), "Click a tower in the shop or press a number to change the tower you place", TEXT_COLOUR, 50))
        self.instructions.append(TextDisplay(pygame.Rect(0, 430, screen_size[0], 65), "Right click a tower to sell it", TEXT_COLOUR, 50))
        self.instructions.append(TextDisplay(pygame.Rect(0, 495, screen_size[0], 65), "Press 'Next wave' or press the space bar to start the wave", TEXT_COLOUR, 50))
        self.instructions.append(TextDisplay(pygame.Rect(0, 560, screen_size[0], 65), "Try to survive as long as you can", TEXT_COLOUR, 50))

        # 시작 및 종료 버튼
        self.play_button = Button(pygame.Rect((screen_size[0]/2) - 150, 630, 150, 80), "Play", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.quit_button = Button(pygame.Rect((screen_size[0]/2) + 50, 630, 150, 80), "Quit", BUTTON_COLOUR, TEXT_COLOUR, 50)

        # 음악 저작권 표기
        self.music_credit = TextDisplay(pygame.Rect(100, 900, 700, 50), "Music: 'Quando a revolução vier' by OVO (Released under CC)", TEXT_COLOUR, 30)

    def render(self, **kwargs):
        # 메인 메뉴 화면 구성 요소 렌더링
        self.menu_screen.blit(self.title.image, self.title.rect)
        for instruction in self.instructions:
            self.menu_screen.blit(instruction.image, instruction.rect)
        self.menu_screen.blit(self.play_button.image, self.play_button.rect)
        self.menu_screen.blit(self.quit_button.image, self.quit_button.rect)
        self.menu_screen.blit(self.music_credit.image, self.music_credit.rect)


# Pause 클래스: 일시 정지 화면을 나타내는 씬
class Pause(Scene):
    def __init__(self, screen_size, screen):
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.pause_overlay = screen.subsurface(self.rect)
        self.pause_message = TextDisplay(pygame.Rect(360, 200, 180, 60), "PAUSED", TEXT_COLOUR, 50)
        self.resume_button = Button(pygame.Rect(200, 340, 225, 75), "Resume", BUTTON_COLOUR, TEXT_COLOUR, 50)
        self.quit_button = Button(pygame.Rect(475, 340, 225, 75), "Main Menu", BUTTON_COLOUR, TEXT_COLOUR, 50)

    def render(self, **kwargs):
        # 일시 정지 화면 구성 요소 렌더링
        kwargs["SCENE_GAME"].render(screen=kwargs["screen"], current_state=kwargs["current_state"])
        self.pause_overlay.blit(self.pause_message.image, self.pause_message.rect)
        self.pause_overlay.blit(self.resume_button.image, self.resume_button.rect)
        self.pause_overlay.blit(self.quit_button.image, self.quit_button.rect)

# Game 클래스: 실제 게임이 진행되는 주요 씬
class Game(Scene):
    def __init__(self, screen_size, screen):
        self.screen_size = screen_size
        self.rect = pygame.Rect(100, 100, screen_size[0]-200, screen_size[1]-200)
        self.game_screen = screen.subsurface(self.rect)
        self.offset = self.game_screen.get_abs_offset()

        # 스프라이트 그룹 초기화
        self.towers = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        # 게임 변수 초기화
        self.lives = 20
        self.money = 200
        self.selected_tower = 0
        self.path = Path(PATH_COLOUR, [(1, -1), (1, 5), (4, 5), (4, 1), (6, 1), (6, 5), (8, 5), (8, 1), (17, 1), (17, 5), (14, 5),
                          (14, 8), (17, 8), (17, 13), (12, 13), (12, 8), (9, 8), (9, 11), (7, 11), (7, 8), (5, 8),
                          (5, 11), (3, 11), (3, 8), (-1, 8)])  # 적이 이동할 경로 정의
        self.wave_handler = WaveHandler(self.path.waypoints[0])
        self.enemies_alive = 0

        # 타워 모델 등록
        self.tower_models = []
        tower_model = TowerModel("Basic Tower", 1, 20, 2, 100, pygame.Color("GREEN"), 'assets/tower1.png', "Low damage, low range, high firerate")
        self.tower_models.append(tower_model)
        tower_model = TowerModel("Sniper Tower", 3, 100, 5, 300, pygame.Color("WHITE"), 'assets/tower2.png', "High damage, high range, low firerate")
        self.tower_models.append(tower_model)

        # 상단 바 UI 요소
        self.next_wave_button = Button(pygame.Rect(100, 25, 160, 50), "Next Wave", BUTTON_COLOUR, TEXT_COLOUR, 40)
        self.pause_button = Button(pygame.Rect(270, 25, 95, 50), "Pause", BUTTON_DISABLED_COLOUR, TEXT_COLOUR, 40)
        self.wave_display = TextDisplay(pygame.Rect(375, 25, 210, 50), "Current Wave: " + str(self.wave_handler.current_wave_number), TEXT_COLOUR, 30)
        self.enemy_count_display = TextDisplay(pygame.Rect(595, 25, 280, 50), "Enemies Remaining: " + str(self.enemies_alive), TEXT_COLOUR, 30)
        self.lives_display = TextDisplay(pygame.Rect(885, 25, 120, 50), "Lives: " + str(self.lives), TEXT_COLOUR, 30)
        self.money_display = TextDisplay(pygame.Rect(1015, 25, 160, 50), "Money: " + str(self.money), TEXT_COLOUR, 30)

        # 상점 UI
        self.shop = Shop(screen, pygame.Rect(adjustCoordsByOffset(self.path.rect.topright, (-self.offset[0], -self.offset[1])), (400, self.path.rect.height)), self.tower_models)

    def update(self, **kwargs):
        # 게임 상태 갱신 (웨이브, 적, 타워, 효과 등)
        self.wave_handler.update(self.enemies)
        self.enemies.update(self.path.waypoints, GRID_SIZE)
        self.towers.update(self.enemies, self.effects, self.game_screen)
        self.effects.update()
        self.money_display.text = "Money: " + str(self.money)

    def render(self, **kwargs):
        screen = kwargs['screen']
        screen.fill(pygame.Color("BLACK"))

        # 상단 UI 렌더링
        screen.blit(self.next_wave_button.image, self.next_wave_button.rect)
        screen.blit(self.pause_button.image, self.pause_button.rect)
        screen.blit(self.wave_display.image, self.wave_display.rect)
        screen.blit(self.enemy_count_display.image, self.enemy_count_display.rect)
        screen.blit(self.lives_display.image, self.lives_display.rect)
        screen.blit(self.money_display.image, self.money_display.rect)

        # 게임 메인 화면 렌더링
        self.game_screen.fill(FRAME_COLOUR)
        self.game_screen.blit(self.path.image, (0, 0))
        self.enemies.draw(self.game_screen)
        self.towers.draw(self.game_screen)
        self.effects.draw(self.game_screen)

        # 상점 렌더링
        self.shop.render(self.selected_tower)

        # 마우스 셀렉터 그리기 (게임이 일시정지가 아닐 때)
        if kwargs["current_state"] != STATE_PAUSED:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pos = (mouse_pos[0] - self.offset[0], mouse_pos[1] - self.offset[1])
            if not self.path.contains(mouse_pos):
                if 0 < mouse_pos[0] < self.path.rect.width and 0 < mouse_pos[1] < self.path.rect.height:
                    size = 5 if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2] else 2
                    pygame.draw.rect(self.game_screen, MOUSE_SELECTOR_COLOUR,
                                     pygame.Rect(mouse_pos[0] - (mouse_pos[0] % GRID_SIZE),
                                                 mouse_pos[1] - (mouse_pos[1] % GRID_SIZE),
                                                 GRID_SIZE, GRID_SIZE), size)


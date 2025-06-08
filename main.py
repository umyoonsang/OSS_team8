# main.py - Tower Defense 게임 메인 실행 파일

import pygame
import math
from enemies import Enemy  # 적 유닛 정의
from tower import Tower, SniperTower, SlowTower  # 타워 클래스들
from wave_manager import WaveManager  # 웨이브 관리 클래스
from UI import *  # UI 요소들 (Button, TextDisplay 등)
from Scene import *  # 메인 메뉴 씬

# Pygame 초기화 및 창 설정
pygame.init()
win = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()

# 타일 설정
TILE_SIZE = 50
screen_size = (1500, 1000)

# 적이 이동할 경로 좌표 정의 (그리드 기준)
tile_path = [
    (1, 0), (1, 5), (4, 5), (4, 1), (6, 1), (6, 5), (8, 5), (8, 1),
    (17, 1), (17, 5), (14, 5), (14, 8), (17, 8), (17, 13),
    (12, 13), (12, 8), (9, 8), (9, 11), (7, 11), (7, 8),
    (5, 8), (5, 11), (3, 11), (3, 8), (0, 8)
]
# 픽셀 좌표로 변환
path = [(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2) for x, y in tile_path]

# 특정 점이 선분에 얼마나 가까운지 계산 (타워 배치 제한에 사용)
def distance_point_to_segment(p, a, b):
    px, py = p
    ax, ay = a
    bx, by = b
    abx = bx - ax
    aby = by - ay
    apx = px - ax
    apy = py - ay
    ab_squared = abx ** 2 + aby ** 2
    if ab_squared == 0:
        return math.hypot(px - ax, py - ay)
    t = max(0, min(1, (apx * abx + apy * aby) / ab_squared))
    closest_x = ax + abx * t
    closest_y = ay + aby * t
    return math.hypot(px - closest_x, py - closest_y)

# 타워를 경로 근처에 설치하지 못하게 제한
def is_point_near_path(pos, path_points, threshold=TILE_SIZE // 2):
    for i in range(len(path_points) - 1):
        if distance_point_to_segment(pos, path_points[i], path_points[i + 1]) < threshold:
            return True
    return False

# 유효한 타워 위치인지 검사
def is_valid_tower_position(pos):
    return not is_point_near_path(pos, path)

# 적 스폰 함수 (웨이브 매니저가 호출)
def spawn_enemy(wave_number):
    enemy = Enemy(path[0][0], path[0][1], path, hp=80 + wave_number * 10)
    enemies.append(enemy)

# 게임 상태 초기화 함수
def reset_game():
    global enemies, bullets, towers, wave_manager, escaped_enemies, gold, waves_started
    enemies = []
    bullets = []
    towers = []
    wave_manager = WaveManager(spawn_enemy)
    escaped_enemies = 0
    gold = 400
    waves_started = False

# 게임 설정 상수
MAX_WAVES = 10  # 최대 웨이브 수
MAX_ESCAPED = 2  # 허용 가능한 탈출 수
font = pygame.font.Font(None, 40)  # 텍스트 폰트

# 씬 인스턴스 생성
game_state = "menu"  # 상태: menu, playing, paused, gameover
menu_scene = MainMenu(screen_size, win)
pause_scene = Pause(screen_size, win)
gameover_scene = GameOver(screen_size, win)
clear_scene = ClearScene(screen_size, win)

# 게임 구성 요소 초기화
reset_game()
tower_models = [Tower(0, 0), SniperTower(0, 0), SlowTower(0, 0)]  # 타워 모델 리스트
selected_tower_index = 0
shop_open = False
shop_button = Button(pygame.Rect(1320, 20, 160, 60), "Shop", pygame.Color("blue"), pygame.Color("white"), 30)
shop_button.create_image()
shop = Shop(win, pygame.Rect(1050, 100, 400, 800), tower_models)
gold_text = TextDisplay(pygame.Rect(20, 800, 200, 50), f"Gold: {gold}", pygame.Color("gold"), 36)
gold_text.create_image()
house_image = pygame.image.load("assets/house.png")
house_image = pygame.transform.scale(house_image, (60, 60))
house_pos = (path[-1][0] - 30, path[-1][1] - 30)  # 도착 지점 위치

# 메인 게임 루프
running = True
while running:
    clock.tick(60)  # FPS 설정

    # 메인 메뉴 처리
    if game_state == "menu":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if menu_scene.play_button.rect.collidepoint(pos):
                    reset_game()
                    game_state = "playing"
                elif menu_scene.quit_button.rect.collidepoint(pos):
                    running = False
        win.fill((0, 0, 0))
        menu_scene.render()
        pygame.display.update()
        continue

    # 일시정지 처리
    elif game_state == "paused":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            result = pause_scene.handle_event(event)
            if result == "resume":
                pygame.event.clear()  # Pause 이후 남은 키 이벤트 제거 (버그 방지)
                game_state = "playing"
                break  # resume 누르면 반복문 탈출
            elif result == "menu":
                game_state = "menu"
                break

        # 여전히 일시정지 상태라면 pause 화면을 렌더링하고 루프 스킵
        if game_state == "paused":
            pause_scene.render(screen=win, current_state="paused", SCENE_GAME=None)
            pygame.display.update()
            continue

    # 게임 오버 처리
    elif game_state == "gameover":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            result = gameover_scene.handle_event(event)
            if result == "restart":
                reset_game()
                game_state = "playing"
            elif result == "quit":
                running = False
        gameover_scene.render()
        pygame.display.update()
        continue

    #게임 클리어    
    elif game_state == "clear":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            result = clear_scene.handle_event(event)
            if result == "menu":
                game_state = "menu"
            elif result == "quit":
                running = False
        clear_scene.render()
        pygame.display.update()
        continue

    # 플레이 중일 때 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_state = "paused"  # 일시정지 전환
            elif event.key == pygame.K_SPACE:
                # 웨이브 시작은 KEYDOWN 이벤트로 처리
                if wave_manager.is_wave_cleared() and not enemies:
                    wave_manager.start_next_wave()
                    waves_started = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            tile_x = mouse_pos[0] // TILE_SIZE
            tile_y = mouse_pos[1] // TILE_SIZE
            center_x = tile_x * TILE_SIZE + TILE_SIZE // 2
            center_y = tile_y * TILE_SIZE + TILE_SIZE // 2

            if shop_button.rect.collidepoint(mouse_pos):
                shop_open = not shop_open
            elif shop_open:
                rel_pos = (mouse_pos[0] - shop.rect.x, mouse_pos[1] - shop.rect.y)
                selected = shop.button_pressed(rel_pos)
                if selected != -1:
                    selected_tower_index = selected
                    shop_open = False
            else:
                tower_class = tower_models[selected_tower_index].__class__
                tower_cost = tower_class.value
                if is_valid_tower_position((center_x, center_y)) and gold >= tower_cost:
                    towers.append(tower_class(center_x, center_y))
                    gold -= tower_cost


    # 배경 그리기 및 경로 출력
    win.fill((200, 200, 200))
    pygame.draw.lines(win, (255, 0, 0), False, path, TILE_SIZE)
    win.blit(house_image, house_pos)

    # 웨이브 및 적 업데이트

    if waves_started:
        wave_manager.update()
        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(win)


            if enemy.path_index >= len(path) and enemy.alive:
                escaped_enemies += 1
                enemies.remove(enemy)
                wave_manager.enemy_killed()

                if escaped_enemies >= MAX_ESCAPED:
                    game_state = "gameover"
                continue
            if not enemy.alive and not enemy.gold_given:
                gold += 25
                enemy.gold_given = True

            if not enemy.alive and enemy.explosion_index >= len(enemy.explosion_frames):
                enemies.remove(enemy)
                wave_manager.enemy_killed()


    # 타워 및 총알 처리
    for tower in towers:
        tower.update(enemies, bullets)
        tower.draw(win)

    for bullet in bullets[:]:
        bullet.move()
        if bullet.hit:
            bullet.target.take_damage(bullet.damage)
            bullets.remove(bullet)
        else:
            bullet.draw(win)


    # UI 표시 (골드, 웨이브, 라이프)
    gold_text.text = f"Gold: {gold}"
    gold_text.create_image()
    win.blit(gold_text.image, gold_text.rect)
    wave_text = font.render(f"Wave: {wave_manager.get_wave_number()} / {MAX_WAVES}", True, (255, 255, 255))
    lives_text = font.render(f"Lives: {MAX_ESCAPED - escaped_enemies} / {MAX_ESCAPED}", True, (255, 100, 100))
    win.blit(wave_text, (220, 800))
    win.blit(lives_text, (400, 800))

        # ✅ 클리어 조건 검사 위치 (여기 이동!)
    if wave_manager.get_wave_number() == MAX_WAVES and wave_manager.is_wave_cleared() and not enemies:
        game_state = "clear"

    # 상점 버튼 및 상점 열기

    win.blit(shop_button.image, shop_button.rect)
    if shop_open:
        shop.render(selected_tower_index)
        win.blit(shop.image, shop.rect)
    
    # 골드 UI 렌더링
    win.blit(gold_text.image, gold_text.rect)

    # 마우스 커서 타일 강조
    mouse_pos = pygame.mouse.get_pos()
    grid_x = mouse_pos[0] - (mouse_pos[0] % TILE_SIZE)
    grid_y = mouse_pos[1] - (mouse_pos[1] % TILE_SIZE)
    pygame.draw.rect(win, (0, 0, 0), (grid_x, grid_y, TILE_SIZE, TILE_SIZE), 2)

    pygame.display.update()

# 게임 종료
pygame.quit()
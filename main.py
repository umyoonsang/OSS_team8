import pygame
import math
from enemies import Enemy
from tower import Tower, SniperTower, SlowTower
from wave_manager import WaveManager
from UI import *

pygame.init()
win = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()

TILE_SIZE = 50

# 타일 단위 경로 (중심 기준으로 변환 예정)
tile_path = [
    (1, 0), (1, 5), (4, 5), (4, 1), (6, 1), (6, 5), (8, 5), (8, 1),
    (17, 1), (17, 5), (14, 5), (14, 8), (17, 8), (17, 13),
    (12, 13), (12, 8), (9, 8), (9, 11), (7, 11), (7, 8),
    (5, 8), (5, 11), (3, 11), (3, 8), (0, 8)
]

# 중심 기준 경로
path = [(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2) for x, y in tile_path]

# 경로 거리 체크 함수
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

# 경로 근처 여부
def is_point_near_path(pos, path_points, threshold=TILE_SIZE // 2):
    for i in range(len(path_points) - 1):
        if distance_point_to_segment(pos, path_points[i], path_points[i + 1]) < threshold:
            return True
    return False

def is_valid_tower_position(pos):
    return not is_point_near_path(pos, path)

# 게임 구성요소
enemies = []
bullets = []
towers = []
tower_models = [Tower(0, 0), SniperTower(0, 0), SlowTower(0, 0)]

shop_open = False
shop_button = Button(
    pygame.Rect(1320, 20, 160, 60), "Shop",
    pygame.Color("blue"), pygame.Color("white"), 30
)
shop_button.create_image()

selected_tower_index = 0
shop = Shop(win, pygame.Rect(1050, 100, 400, 800), tower_models)

# 적 생성
def spawn_enemy(wave_number):
    enemy = Enemy(path[0][0], path[0][1], path, hp=80 + wave_number * 10)
    enemies.append(enemy)

# 골드 관련 변수와 UI
gold = 400  # 시작 골드
gold_text = TextDisplay(
    pygame.Rect(20, 800, 200, 50),
    f"Gold: {gold}",
    pygame.Color("gold"),
    36
)
gold_text.create_image()

wave_manager = WaveManager(spawn_enemy)
waves_started = False

# 게임 상태 변수 추가
MAX_WAVES = 10  # 총 웨이브 수
escaped_enemies = 0  # 탈출한 적 수
MAX_ESCAPED = 2  # 최대 허용 탈출 수
game_over = False

# 집 이미지 로드
house_image = pygame.image.load("assets/house.png")
house_image = pygame.transform.scale(house_image, (60, 60))
house_pos = (path[-1][0] - 30, path[-1][1] - 30)  # 경로 끝점에 위치

# 게임오버 텍스트
game_over_text = TextDisplay(
    pygame.Rect(600, 400, 300, 100),
    "YOU LOSE",
    pygame.Color("red"),
    72
)
game_over_text.create_image()

# 메인 루프
running = True
while running:
    clock.tick(60)
    win.fill((200, 200, 200))

    # 골드 텍스트 업데이트
    gold_text.text = f"Gold: {gold}"
    gold_text.create_image()

    # 경로 그리기
    pygame.draw.lines(win, (255, 0, 0), False, path, TILE_SIZE)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
                tower_cost = tower_class.value  # 타워 가격
                if is_valid_tower_position((center_x, center_y)) and gold >= tower_cost:
                    towers.append(tower_class(center_x, center_y))
                    gold -= tower_cost  # 타워 설치 시 골드 차감

    # 웨이브 시작
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and wave_manager.is_wave_cleared() and not enemies:
        wave_manager.start_next_wave()
        waves_started = True

    if game_over:
        # 게임 오버 화면 표시
        win.blit(game_over_text.image, game_over_text.rect)
        pygame.display.update()
        continue
        
    # 집 이미지 그리기
    win.blit(house_image, house_pos)
    
    # 웨이브 체크
    if wave_manager.get_wave_number() > MAX_WAVES and wave_manager.is_wave_cleared() and not enemies:
        game_over = True
        game_over_text.text = "YOU WIN!"
        game_over_text.text_colour = pygame.Color("green")
        game_over_text.create_image()
    
    # 적 업데이트 부분 수정
    if waves_started:
        wave_manager.update()

        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(win)
            
            # 적이 경로 끝에 도달했는지 체크
            if enemy.path_index >= len(path) and enemy.alive:
                escaped_enemies += 1
                enemies.remove(enemy)
                wave_manager.enemy_killed()
                
                if escaped_enemies >= MAX_ESCAPED:
                    game_over = True
                    game_over_text.create_image()
                continue

            # 적이 죽었을 때 골드 획득
            if not enemy.alive and not enemy.gold_given:
                gold += 25
                enemy.gold_given = True
            
            if not enemy.alive and enemy.explosion_index >= len(enemy.explosion_frames):
                enemies.remove(enemy)
                wave_manager.enemy_killed()

    # 타워
    for tower in towers:
        tower.update(enemies, bullets)
        tower.draw(win)

    # 총알
    for bullet in bullets[:]:
        bullet.move()
        if bullet.hit:
            bullet.target.take_damage(bullet.damage)
            bullets.remove(bullet)
        else:
            bullet.draw(win)

    # UI 렌더링
    win.blit(shop_button.image, shop_button.rect)
    if shop_open:
        shop.render(selected_tower_index)
        win.blit(shop.image, shop.rect)
    
    # 골드 UI 렌더링
    win.blit(gold_text.image, gold_text.rect)

    # 마우스 셀 강조
    mouse_pos = pygame.mouse.get_pos()
    grid_x = mouse_pos[0] - (mouse_pos[0] % TILE_SIZE)
    grid_y = mouse_pos[1] - (mouse_pos[1] % TILE_SIZE)
    pygame.draw.rect(win, (0, 0, 0), (grid_x, grid_y, TILE_SIZE, TILE_SIZE), 2)

    pygame.display.update()

pygame.quit()

import pygame
from enemies import Enemy
from tower import Tower, SniperTower, SlowTower
from wave_manager import WaveManager
from UI import Shop, Button

# 초기화
pygame.init()
win = pygame.display.set_mode((1500, 1000))
clock = pygame.time.Clock()

# 경로 (적 이동 경로)
path = [
    (1 * 50, -1 * 50), (1 * 50, 5 * 50), (4 * 50, 5 * 50), (4 * 50, 1 * 50),
    (6 * 50, 1 * 50), (6 * 50, 5 * 50), (8 * 50, 5 * 50), (8 * 50, 1 * 50),
    (17 * 50, 1 * 50), (17 * 50, 5 * 50), (14 * 50, 5 * 50), (14 * 50, 8 * 50),
    (17 * 50, 8 * 50), (17 * 50, 13 * 50), (12 * 50, 13 * 50), (12 * 50, 8 * 50),
    (9 * 50, 8 * 50), (9 * 50, 11 * 50), (7 * 50, 11 * 50), (7 * 50, 8 * 50),
    (5 * 50, 8 * 50), (5 * 50, 11 * 50), (3 * 50, 11 * 50), (3 * 50, 8 * 50),
    (-1 * 50, 8 * 50)
]

# 게임 요소
enemies = []
bullets = []
towers = []

# 타워 모델 (상점용, placeholder 위치로 생성)
tower_models = [
    Tower(0, 0),
    SniperTower(0, 0),
    SlowTower(0, 0)
]

# 상점 관련 변수
shop_open = False
shop_button = Button(pygame.Rect(1300, 920, 120, 50), "Shop", pygame.Color("blue"), pygame.Color("white"), 30)
selected_tower_index = 0
shop = Shop(win, pygame.Rect(1050, 100, 400, 800), tower_models)

# 적 생성 함수
def spawn_enemy(wave_number):
    enemy = Enemy(path[0][0], path[0][1], path, hp=80 + wave_number * 10)
    enemies.append(enemy)

# 웨이브 매니저 초기화
wave_manager = WaveManager(spawn_enemy)
wave_manager.start_next_wave()

# 메인 루프
running = True
while running:
    clock.tick(60)
    win.fill((255, 255, 255))  # 배경 흰색

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if shop_button.rect.collidepoint(mouse_pos):
                shop_open = not shop_open  # 상점 열고 닫기
            elif shop_open:
                rel_pos = (mouse_pos[0] - shop.rect.x, mouse_pos[1] - shop.rect.y)
                selected = shop.button_pressed(rel_pos)
                if selected != -1:
                    selected_tower_index = selected
                    shop_open = False
            else:
                # 상점 닫힌 상태에서 화면 클릭 시 타워 설치
                tower_class = tower_models[selected_tower_index].__class__
                towers.append(tower_class(mouse_pos[0], mouse_pos[1]))

    # 웨이브 업데이트
    wave_manager.update()

    # 적 업데이트 및 그리기
    for enemy in enemies[:]:
        enemy.update()
        enemy.draw(win)
        if not enemy.alive:
            enemies.remove(enemy)
            wave_manager.enemy_killed()

    # 타워 업데이트
    for tower in towers:
        tower.update(enemies, bullets)
        tower.draw(win)

    # 총알 이동 및 충돌 처리
    for bullet in bullets[:]:
        bullet.move()
        if bullet.hit:
            bullet.target.take_damage(bullet.damage)
            bullets.remove(bullet)
        else:
            bullet.draw(win)

    # 다음 웨이브 시작 (스페이스바)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and wave_manager.is_wave_cleared():
        wave_manager.start_next_wave()

    # Shop 버튼 및 상점 렌더링
    shop_button.create_image()
    win.blit(shop_button.image, shop_button.rect)
    if shop_open:
        shop.render(selected_tower_index)

    pygame.display.update()

pygame.quit()

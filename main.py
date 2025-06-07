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
    (1 * 60, -1 * 60), (1 * 60, 5 * 60), (4 * 60, 5 * 60), (4 * 60, 1 * 60), (6 * 60, 1 * 60),
    (6 * 60, 5 * 60), (8 * 60, 5 * 60), (8 * 60, 1 * 60), (17 * 60, 1 * 60), (17 * 60, 5 * 60),
    (14 * 60, 5 * 60), (14 * 60, 8 * 60), (17 * 60, 8 * 60), (17 * 60, 13 * 60),
    (12 * 60, 13 * 60), (12 * 60, 8 * 60), (9 * 60, 8 * 60), (9 * 60, 11 * 60),
    (7 * 60, 11 * 60), (7 * 60, 8 * 60), (5 * 60, 8 * 60), (5 * 60, 11 * 60),
    (3 * 60, 11 * 60), (3 * 60, 8 * 60), (-1 * 60, 8 * 60)
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
shop_button = Button(pygame.Rect(1340, 20, 120, 50), "Shop", pygame.Color("blue"), pygame.Color("white"), 30)
selected_tower_index = 0
shop = Shop(win, pygame.Rect(1050, 100, 400, 800), tower_models)

# 적 생성 함수
def spawn_enemy(wave_number):
    enemy = Enemy(path[0][0], path[0][1], path, hp=80 + wave_number * 10)
    enemies.append(enemy)

# 웨이브 매니저 초기화
wave_manager = WaveManager(spawn_enemy)
waves_started = False

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
                tower_class = tower_models[selected_tower_index].__class__
                towers.append(tower_class(mouse_pos[0], mouse_pos[1]))

    # 스페이스 키로 웨이브 시작
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and wave_manager.is_wave_cleared() and not enemies:
        wave_manager.start_next_wave()
        waves_started = True

    # 웨이브 및 유닛 업데이트
    if waves_started:
        wave_manager.update()
        for enemy in enemies[:]:
            enemy.update()
            enemy.draw(win)
            if not enemy.alive:
                enemies.remove(enemy)
                wave_manager.enemy_killed()

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

    # Shop 버튼 및 상점 렌더링
    shop_button.create_image()
    win.blit(shop_button.image, shop_button.rect)
    if shop_open:
        shop.render(selected_tower_index)

    pygame.display.update()

pygame.quit()

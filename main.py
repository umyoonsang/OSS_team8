import pygame
from enemies import Enemy
from tower import Tower, Bullet
from wave_manager import WaveManager

# 초기화
pygame.init()
win = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# 경로 (적 이동 경로)
path = [(50, 100), (200, 100), (200, 300), (600, 300), (750, 500)]

# 게임 요소
enemies = []
bullets = []
towers = [Tower(400, 250)]

# 적 생성 함수 (WaveManager에 넘겨줄 콜백)
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

    # 웨이브 업데이트 (적 스폰)
    wave_manager.update()

    # 적 업데이트 및 그리기
    for enemy in enemies[:]:
        enemy.update()
        enemy.draw(win)
        if not enemy.alive:
            enemies.remove(enemy)
            wave_manager.enemy_killed()

    # 타워 업데이트 (적 찾아서 총알 발사)
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

    # 다음 웨이브 수동 시작 (스페이스바)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and wave_manager.is_wave_cleared():
        wave_manager.start_next_wave()

    pygame.display.update()

pygame.quit()

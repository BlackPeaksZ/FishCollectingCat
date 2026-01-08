import pygame
import random

pygame.init()
screen = pygame.display.set_mode((950, 555))
pygame.display.set_caption('Кот собиратель рыбы')

icon = pygame.image.load('icons/icon.jpg').convert()
pygame.display.set_icon(icon)

bg = pygame.image.load('icons/bg.jpg').convert()  # Основной фон с домом
bg2 = pygame.image.load('icons/bg.jpg').convert()  # Второй фон без дома

fish = pygame.image.load('icons/fish.png').convert_alpha()
shack = pygame.image.load('icons/shack.png').convert_alpha()

# кот
player_left = [
    pygame.image.load('icons/cat/left/icon1.png').convert_alpha(),
    pygame.image.load('icons/cat/left/icon2.png').convert_alpha()
]
player_right = [
    pygame.image.load('icons/cat/right/icon1.png').convert_alpha(),
    pygame.image.load('icons/cat/right/icon2.png').convert_alpha()
]
player_stop = [
    pygame.image.load('icons/cat/stop/icon1.png').convert_alpha(),
    pygame.image.load('icons/cat/stop/icon2.png').convert_alpha()
]

player_speed = 9
player_x = 250
player_y = 360
player_count = 0
player_anim_counter = 0
player_anim_speed = 0.3  # Скорость анимации
player_direction = 0  # 0 - стоит, -1 - влево, 1 - вправо

# Настройки дома
shack_x = 100
shack_y = 320

# Настройки фона
bg_x = 0
bg2_x = 950
bg_speed = 15

running = True
is_jump = False
carrying_fish = False
ground_level = 360  # Уровень земли

# Настройки рыбы
fish_list = []
score = 0
show_score_animation = False
score_animation_timer = 0

jump_count = 7
jump_speed = 0

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Таймер для спавна рыбы
last_fish_time = pygame.time.get_ticks()
fish_spawn_interval = 10000  # 10 секунд

# Таймер
clock = pygame.time.Clock()

while running:
    # Время
    current_time = pygame.time.get_ticks()
    delta_time = clock.tick(60) / 1000.0  # Время в секундах

    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE and not is_jump:
                is_jump = True
                jump_count = 7

    # Получение нажатых клавиш
    keys = pygame.key.get_pressed()

    # Отрисовка фона
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg2, (bg2_x, 0))

    score_text = font.render(f'Рыб: {score}', True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Отображение дома (только на основном фоне)
    shack_screen_x = shack_x + bg_x
    if -shack.get_width() < shack_screen_x < 950:
        screen.blit(shack, (shack_screen_x, shack_y))
    shack_rect = shack.get_rect(topleft=(shack_screen_x, shack_y))

    # Отображение рыбы (только на втором фоне)
    fish_to_remove = []
    for i, (fish_x, fish_y) in enumerate(fish_list):
        fish_screen_x = fish_x + bg2_x
        # Проверяем, видна ли рыба на экране
        if -fish.get_width() < fish_screen_x < 950:
            screen.blit(fish, (fish_screen_x, fish_y))

    player_anim_counter += delta_time
    if player_anim_counter >= player_anim_speed:
        player_anim_counter = 0
        player_count = (player_count + 1) % 2

    player_rect = pygame.Rect(player_x, player_y,
                              player_stop[0].get_width(),
                              player_stop[0].get_height())

    if keys[pygame.K_LEFT]:
        screen.blit(player_left[player_count], (player_x, player_y))
        player_direction = -1
    elif keys[pygame.K_RIGHT]:
        screen.blit(player_right[player_count], (player_x, player_y))
        player_direction = 1
    else:
        screen.blit(player_stop[player_count], (player_x, player_y))
        player_direction = 0

    # Движение кота и фона
    if keys[pygame.K_RIGHT]:
        if player_x < 400: #движение слева
            player_x += player_speed
        else:  # Двигаем фон, игрок остается на месте
            bg_x -= bg_speed
            bg2_x -= bg_speed
    elif keys[pygame.K_LEFT]:
        if player_x > 100: #движение справа
            player_x -= player_speed
        else:  # Двигаем фон
            bg_x += bg_speed
            bg2_x += bg_speed

    # зацикленное движение фона
    if bg_x <= -950:
        bg_x += 1900
    elif bg_x >= 950:
        bg_x -= 1900

    if bg2_x <= -950:
        bg2_x += 1900
    elif bg2_x >= 950:
        bg2_x -= 1900

    if is_jump:
        if jump_count >= -7:
            neg = 1
            if jump_count < 0:
                neg = -1
            player_y -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            is_jump = False
            jump_count = 7
            player_y = ground_level

    # Проверка сбора рыбы
    for i, (fish_x, fish_y) in enumerate(fish_list[:]):
        fish_screen_x = fish_x + bg2_x
        fish_rect = fish.get_rect(topleft=(fish_screen_x, fish_y))

        if not carrying_fish and player_rect.colliderect(fish_rect):
            carrying_fish = True
            fish_to_remove.append((fish_x, fish_y))

    # Удаляем собранную рыбу
    for fish_pos in fish_to_remove:
        if fish_pos in fish_list:
            fish_list.remove(fish_pos)

    # Проверка доставки рыбы в дом
    if carrying_fish:
        # Отображаем рыбу над котом
        screen.blit(fish, (player_x + 30, player_y - 40))

        if player_rect.colliderect(shack_rect):
            carrying_fish = False
            score += 1
            show_score_animation = True
            score_animation_timer = 60 

    if show_score_animation:
        plus_text = big_font.render("+1", True, (255, 215, 0))
        screen.blit(plus_text, (player_x, player_y - 80))
        score_animation_timer -= 1
        if score_animation_timer <= 0:
            show_score_animation = False

    # Спавн новой рыбы по таймеру
    if current_time - last_fish_time > fish_spawn_interval:
        # Спавним рыбу в пределах второго фона
        fish_x = random.randint(0, 950)
        fish_y = 360
        fish_list.append((fish_x, fish_y))
        last_fish_time = current_time

    # Обновление экрана
    pygame.display.update()

pygame.quit()

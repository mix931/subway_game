import pygame, sys, random

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Бегущий герой")

clock = pygame.time.Clock()
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)

font = pygame.font.SysFont(None, 36)

# Загрузка фона и музыки
background = pygame.image.load("background.jpg")  # Добавьте изображение фона
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.mixer.music.load("background_music.mp3")  # Добавьте фоновую музыку
pygame.mixer.music.play(-1)

# Движущиеся полосы на дороге
road_lines = [pygame.Rect(SCREEN_WIDTH//2 - 5, i * 100, 10, 80) for i in range(6)]

def pause_game():
    """Функция для паузы игры"""
    paused = True
    pause_text = font.render("Пауза. Нажмите ESC для продолжения", True, WHITE)
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
    while paused:
        screen.fill(BLACK)
        screen.blit(pause_text, pause_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = False

def run_game():
    """Основной цикл игры"""
    player_width, player_height = 40, 60
    player_x, player_y = SCREEN_WIDTH // 2 - player_width // 2, SCREEN_HEIGHT - player_height - 10
    player_speed = 5
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    obstacle_width, obstacle_height, obstacle_speed = 40, 60, 5
    obstacle_frequency = 1500
    pygame.time.set_timer(pygame.USEREVENT+1, obstacle_frequency)
    obstacles = []

    score = 0
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_game()
            if event.type == pygame.USEREVENT+1:
                x_pos = random.randint(0, SCREEN_WIDTH - obstacle_width)
                new_obstacle = pygame.Rect(x_pos, -obstacle_height, obstacle_width, obstacle_height)
                obstacles.append(new_obstacle)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed

        for obstacle in obstacles[:]:
            obstacle.y += obstacle_speed
            if obstacle.top > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                running = False

        # Отрисовка фона и движения дороги
        screen.blit(background, (0, 0))
        for line in road_lines:
            pygame.draw.rect(screen, WHITE, line)
            line.y += obstacle_speed
            if line.y > SCREEN_HEIGHT:
                line.y = -80

        pygame.draw.rect(screen, BLUE, player_rect)
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)

        score_text = font.render(f"Счет: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
    
    return score

def game_over_screen(score):
    """Экран окончания игры с анимацией затемнения"""
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill(BLACK)
    alpha = 0
    
    while alpha < 255:
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        alpha += 5
        clock.tick(30)
    
    while True:
        screen.fill(GRAY)

        game_over_text = font.render("Игра окончена!", True, WHITE)
        final_score_text = font.render(f"Счет: {score}", True, WHITE)
        button_text = font.render("Повторить", True, BLACK)

        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
        button_rect = button_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
        button_bg_rect = pygame.Rect(button_rect.left - 10, button_rect.top - 10, button_rect.width + 20, button_rect.height + 20)

        pygame.draw.rect(screen, WHITE, button_bg_rect)
        pygame.draw.rect(screen, BLACK, button_bg_rect, 2)

        screen.blit(game_over_text, game_over_rect)
        screen.blit(final_score_text, final_score_rect)
        screen.blit(button_text, button_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_bg_rect.collidepoint(event.pos):
                    return

        clock.tick(FPS)

while True:
    score = run_game()
    game_over_screen(score)
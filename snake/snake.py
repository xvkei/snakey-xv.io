import pygame, sys, time, random

# Initialize pygame
pygame.init()

# Window settings
frame_size_x = 720
frame_size_y = 480
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))
pygame.display.set_caption('Snake Eater')

# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
grey = pygame.Color(100, 100, 100)

# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
food_spawn = True
obstacles = []
direction = 'RIGHT'
change_to = direction
score = 0
paused = False
difficulty = 10

# FPS controller
fps_controller = pygame.time.Clock()

# Fonts
menu_font = pygame.font.SysFont('times new roman', 50)
game_font = pygame.font.SysFont('times new roman', 20)

# Draw the main menu
def main_menu():
    game_window.fill(black)
    title_surface = menu_font.render('Snake Eater', True, green)
    play_surface = menu_font.render('Press ENTER to Play', True, white)
    quit_surface = menu_font.render('Press ESC to Quit', True, white)

    title_rect = title_surface.get_rect(center=(frame_size_x // 2, frame_size_y // 4))
    play_rect = play_surface.get_rect(center=(frame_size_x // 2, frame_size_y // 2))
    quit_rect = quit_surface.get_rect(center=(frame_size_x // 2, frame_size_y // 1.5))

    game_window.blit(title_surface, title_rect)
    game_window.blit(play_surface, play_rect)
    game_window.blit(quit_surface, quit_rect)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Start game
                    return
                elif event.key == pygame.K_ESCAPE:  # Quit game
                    pygame.quit()
                    sys.exit()

# Generate obstacles
def generate_obstacles(count):
    return [[random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10] for _ in range(count)]

# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('GAME OVER', True, red)
    game_over_rect = game_over_surface.get_rect(midtop=(frame_size_x / 2, frame_size_y / 4))
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Show score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

# Pause the game
def pause_game():
    global paused
    paused = not paused

def game_loop():
    global direction, change_to, food_spawn, food_pos, snake_body, score, paused, difficulty
    obstacles = generate_obstacles(5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and direction != 'DOWN':
                    change_to = 'UP'
                if event.key == pygame.K_s and direction != 'UP':
                    change_to = 'DOWN'
                if event.key == pygame.K_a and direction != 'RIGHT':
                    change_to = 'LEFT'
                if event.key == pygame.K_d and direction != 'LEFT':
                    change_to = 'RIGHT'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_p:  # Pause game
                    pause_game()

        if paused:
            pause_surface = menu_font.render('Game Paused - Press P to Resume', True, white)
            pause_rect = pause_surface.get_rect(center=(frame_size_x // 2, frame_size_y // 2))
            game_window.fill(black)
            game_window.blit(pause_surface, pause_rect)
            pygame.display.flip()
            continue

        # Update snake direction
        direction = change_to

        # Move snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 1
            difficulty += 1
            food_spawn = False
        else:
            snake_body.pop()

        # Spawn food
        if not food_spawn:
            food_pos = [random.randrange(1, (frame_size_x // 10)) * 10, random.randrange(1, (frame_size_y // 10)) * 10]
        food_spawn = True

        # Game over conditions
        if (snake_pos[0] < 0 or snake_pos[0] > frame_size_x - 10 or
                snake_pos[1] < 0 or snake_pos[1] > frame_size_y - 10 or
                snake_pos in snake_body[1:] or snake_pos in obstacles):
            game_over()

        # Graphics
        game_window.fill(black)
        for pos in snake_body:
            pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        for obstacle in obstacles:
            pygame.draw.rect(game_window, grey, pygame.Rect(obstacle[0], obstacle[1], 10, 10))

        show_score(1, white, 'times', 20)
        pygame.display.update()
        fps_controller.tick(difficulty)

# Run the game
main_menu()
game_loop()
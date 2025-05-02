import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐱 Cat Dodge!")

# Set up clock
clock = pygame.time.Clock()
FPS = 60

# Set up colors
WHITE = (255, 255, 255)
PINK = (255, 105, 180)  # Pink color for the cat
RED = (255, 0, 0)  # Red color for the dog
BLACK = (0, 0, 0)

# Player settings
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 7

# Enemy settings
enemy_size = 50
enemy_list = [[random.randint(0, WIDTH - enemy_size), 0]]
enemy_speed = 5

# Score
score = 0
font = pygame.font.SysFont("Arial", 32)

def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, WIDTH - enemy_size)
        enemy_list.append([x_pos, 0])

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(win, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_positions(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list[:]):
        if enemy_pos[1] < HEIGHT:
            enemy_pos[1] += enemy_speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def detect_collision(player_pos, enemy_pos):
    px, py = player_pos
    ex, ey = enemy_pos

    if (ex < px < ex + enemy_size or ex < px + player_size < ex + enemy_size) and \
       (ey < py < ey + enemy_size or ey < py + player_size < ey + enemy_size):
        return True
    return False

def check_collisions(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

# Game loop
running = True
while running:
    win.fill(WHITE)  # White background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    drop_enemies(enemy_list)
    score = update_enemy_positions(enemy_list, score)

    if check_collisions(enemy_list, player_pos):
        print(f"💥 Game Over! Final Score: {score}")
        running = False

    draw_enemies(enemy_list)
    pygame.draw.rect(win, PINK, (player_pos[0], player_pos[1], player_size, player_size))

    text = font.render(f"Score: {score}", True, BLACK)
    win.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()

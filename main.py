import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platformer with Obstacles')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (135, 206, 235)
RED = (255, 0, 0)

clock = pygame.time.Clock()

player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_vel = [0, 0]
player_speed = 5
player_jump = -15
player_jump_count = 0
max_jumps = 2
scroll_speed = 5

floor = [0, HEIGHT - 20, WIDTH, 20]
obstacles = [
    [WIDTH + 200, HEIGHT - 70, 50, 50],
    [WIDTH + 600, HEIGHT - 70, 50, 50],
    [WIDTH + 1000, HEIGHT - 70, 50, 50],
]

score = 0
font = pygame.font.SysFont('Arial', 30)

def generate_obstacle():
    x = random.randint(WIDTH, WIDTH + 400)
    y = HEIGHT - 70
    return [x, y, 50, 50]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE] and player_jump_count < max_jumps:
        player_vel[1] = player_jump
        player_jump_count += 1

    player_vel[1] += 1
    player_pos[1] += player_vel[1]

    if player_pos[0] < 0:
        player_pos[0] = 0
    if player_pos[0] > WIDTH - player_size:
        player_pos[0] = WIDTH - player_size

    player_on_ground = False

    if (player_pos[1] + player_size >= floor[1] and
            player_pos[1] + player_size - player_vel[1] <= floor[1] and
            player_pos[0] + player_size > floor[0] and
            player_pos[0] < floor[0] + floor[2]):
        player_pos[1] = floor[1] - player_size
        player_vel[1] = 0
        player_on_ground = True
        player_jump_count = 0

    for obstacle in obstacles:
        if (player_pos[1] + player_size >= obstacle[1] and
                player_pos[1] <= obstacle[1] + obstacle[3] and
                player_pos[0] + player_size > obstacle[0] and
                player_pos[0] < obstacle[0] + obstacle[2]):
            if player_vel[1] > 0:
                player_vel[1] = 0
                player_pos[1] = obstacle[1] - player_size
            else:
                player_pos[0] = obstacle[0] - player_size

    if player_pos[1] > HEIGHT - player_size:
        player_pos[1] = HEIGHT - player_size
        player_vel[1] = 0
        player_on_ground = True
        player_jump_count = 0

    for obstacle in obstacles:
        obstacle[0] -= scroll_speed

    for obstacle in obstacles:
        if obstacle[0] + obstacle[2] < 0:
            obstacles.remove(obstacle)
            new_obstacle = generate_obstacle()
            obstacles.append(new_obstacle)

    score += 1

    win.fill(BG_COLOR)

    pygame.draw.rect(win, BLACK, floor)

    for obstacle in obstacles:
        pygame.draw.rect(win, RED, obstacle)

    pygame.draw.rect(win, BLUE, (*player_pos, player_size, player_size))

    score_text = font.render(f'Score: {score}', True, BLACK)
    win.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()

import pygame
import sys
import random

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (135, 206, 235)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Advanced Platformer')

# Game Variables
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_vel = [0, 0]
player_speed = 5
player_jump = -15
player_gravity = 1
player_jump_count = 0
max_jumps = 2
scroll_speed = 5

floor = [0, HEIGHT - 20, WIDTH, 20]
obstacles = [
    [WIDTH + 200, HEIGHT - 70, 50, 50],
    [WIDTH + 600, HEIGHT - 70, 50, 50],
    [WIDTH + 1000, HEIGHT - 70, 50, 50],
]

power_ups = []
power_up_size = 30
power_up_effect_duration = 300  # frames

backgrounds = [pygame.Surface((WIDTH, HEIGHT)) for _ in range(2)]
backgrounds[0].fill(BG_COLOR)
backgrounds[1].fill(BG_COLOR)
bg_x = [0, WIDTH]

score = 0
font = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()

# Functions
def generate_obstacle():
    x = random.randint(WIDTH, WIDTH + 400)
    y = HEIGHT - 70
    width = random.randint(40, 80)
    height = random.randint(40, 80)
    return [x, y, width, height]

def generate_power_up():
    x = random.randint(WIDTH, WIDTH + 400)
    y = HEIGHT - 100  # Place power-ups closer to the ground
    return [x, y, power_up_size, power_up_size]

def draw_player():
    pygame.draw.rect(win, BLUE, (*player_pos, player_size, player_size))

def draw_obstacles():
    for obstacle in obstacles:
        pygame.draw.rect(win, RED, obstacle)

def draw_power_ups():
    for power_up in power_ups:
        pygame.draw.rect(win, GREEN, power_up)

def draw_background():
    for i in range(2):
        win.blit(backgrounds[i], (bg_x[i], 0))
        bg_x[i] -= scroll_speed // 2
        if bg_x[i] <= -WIDTH:
            bg_x[i] = WIDTH

def handle_player_movement(keys):
    global player_jump_count
    if keys[pygame.K_a]:
        player_pos[0] -= player_speed
    if keys[pygame.K_d]:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE] and player_jump_count < max_jumps:
        player_vel[1] = player_jump
        player_jump_count += 1

def apply_gravity():
    player_vel[1] += player_gravity
    player_pos[1] += player_vel[1]

def check_collisions():
    global player_jump_count, player_vel, player_pos, score, power_ups, power_up_effect_duration

    player_on_ground = False
    if player_pos[1] + player_size >= floor[1]:
        player_pos[1] = floor[1] - player_size
        player_vel[1] = 0
        player_on_ground = True
        player_jump_count = 0

    for obstacle in obstacles:
        if (player_pos[1] + player_size > obstacle[1] and
            player_pos[1] < obstacle[1] + obstacle[3] and
            player_pos[0] + player_size > obstacle[0] and
            player_pos[0] < obstacle[0] + obstacle[2]):
            if player_vel[1] > 0:
                player_vel[1] = 0
                player_pos[1] = obstacle[1] - player_size
            elif player_vel[1] < 0:
                player_vel[1] = 0
                player_pos[1] = obstacle[1] + obstacle[3]
            if player_vel[0] > 0:
                player_pos[0] = obstacle[0] - player_size
            elif player_vel[0] < 0:
                player_pos[0] = obstacle[0] + obstacle[2]

    for power_up in power_ups:
        if (player_pos[1] + player_size > power_up[1] and
            player_pos[1] < power_up[1] + power_up[3] and
            player_pos[0] + player_size > power_up[0] and
            player_pos[0] < power_up[0] + power_up[2]):
            power_ups.remove(power_up)
            score += 100
            power_up_effect_duration = 300

    if player_pos[1] > HEIGHT - player_size:
        player_pos[1] = HEIGHT - player_size
        player_vel[1] = 0
        player_on_ground = True
        player_jump_count = 0

    return player_on_ground

def update_obstacles():
    for obstacle in obstacles:
        obstacle[0] -= scroll_speed
    if obstacles and obstacles[0][0] + obstacles[0][2] < 0:
        obstacles.pop(0)
        obstacles.append(generate_obstacle())

def update_power_ups():
    for power_up in power_ups:
        power_up[0] -= scroll_speed
    if power_ups and power_ups[0][0] + power_ups[0][2] < 0:
        power_ups.pop(0)
    if random.randint(1, 200) == 1:  # Less frequent power-up generation
        power_ups.append(generate_power_up())

def draw_score():
    score_text = font.render(f'Score: {score}', True, BLACK)
    win.blit(score_text, (10, 10))

# Main game loop
running = True
while running:
    win.fill(WHITE)
    draw_background()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    handle_player_movement(keys)
    apply_gravity()
    player_on_ground = check_collisions()

    update_obstacles()
    update_power_ups()

    draw_obstacles()
    draw_power_ups()
    draw_player()
    draw_score()

    score += 1
    if power_up_effect_duration > 0:
        power_up_effect_duration -= 1

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()

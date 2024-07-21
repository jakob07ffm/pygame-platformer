import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platformer')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_vel = [0, 0]
player_speed = 5
player_jump = -15
player_on_ground = False
player_jump_count = 0
max_jumps = 2

platforms = [
    [0, HEIGHT - 20, WIDTH, 20],
    [WIDTH // 3, HEIGHT - 100, 200, 10],
    [WIDTH * 2 // 3, HEIGHT - 200, 200, 10]
]

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
    if keys[pygame.K_SPACE] and player_jump_count <= max_jumps:
        player_vel[1] = player_jump
        player_jump_count += 1

    player_vel[1] += 1
    player_pos[1] += player_vel[1]

    if player_pos[0] < 0:
        player_pos[0] = 0
    if player_pos[0] > WIDTH - player_size:
        player_pos[0] = WIDTH - player_size

    player_on_ground = False

    for platform in platforms:
        if (player_pos[1] + player_size >= platform[1] and
                player_pos[1] + player_size - player_vel[1] <= platform[1] and
                player_pos[0] + player_size > platform[0] and
                player_pos[0] < platform[0] + platform[2]):
            player_pos[1] = platform[1] - player_size
            player_vel[1] = 0
            player_on_ground = True
            player_jump_count = 0

    if player_pos[1] > HEIGHT - player_size:
        player_pos[1] = HEIGHT - player_size
        player_vel[1] = 0
        player_on_ground = True
        player_jump_count = 0

    win.fill(WHITE)

    for platform in platforms:
        pygame.draw.rect(win, BLACK, platform)

    pygame.draw.rect(win, BLUE, (*player_pos, player_size, player_size))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()

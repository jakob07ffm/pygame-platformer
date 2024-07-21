import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('platformer')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

player_size = 50
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_vel = [0, 0]
player_speed = 5
player_jump = -15

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
    
    win.fill(WHITE)
    
    for platform in platforms:
        pygame.draw.rect(win, BLACK, platform)
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_SPACE] and player_vel[1] == 0:
        player_vel[1] = player_jump

    player_vel[1] += 1  
    player_pos[1] += player_vel[1]

    for platform in platforms:
        if (player_pos[1] + player_size >= platform[1] and
            player_pos[1] + player_size <= platform[1] + platform[3] and
            player_pos[0] + player_size > platform[0] and
            player_pos[0] < platform[0] + platform[2]):
            player_pos[1] = platform[1] - player_size
            player_vel[1] = 0
    
    pygame.draw.rect(win, BLUE, (*player_pos, player_size, player_size))
                                    
    pygame.display.flip()
    
    clock.tick(30)

pygame.quit()
sys.exit()

#todos:
#-make the player only jump once or twice
#-making it so the player cant leav the win

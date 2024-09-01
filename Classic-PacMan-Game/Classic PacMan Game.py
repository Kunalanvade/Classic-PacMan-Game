import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 400, 400
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pacman Clone")

# Pacman and pellet variables
pacman_x, pacman_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
pacman_direction = (0, 0)
pellets = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) if (x, y) != (pacman_x, pacman_y)]
random.shuffle(pellets)

# Ghost variables
ghosts = [(2, 2), (GRID_WIDTH - 3, 2), (2, GRID_HEIGHT - 3), (GRID_WIDTH - 3, GRID_HEIGHT - 3)]

# Score variables
score = 0
font = pygame.font.Font(None, 36)

# Score area
score_area = pygame.Rect(10, HEIGHT - 40, 100, 30)

def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))

def draw_pellets():
    for pellet_x, pellet_y in pellets:
        pygame.draw.circle(screen, YELLOW, (pellet_x * GRID_SIZE + GRID_SIZE // 2, pellet_y * GRID_SIZE + GRID_SIZE // 2), 5)

def move_pacman(mouse_pos):
    global pacman_x, pacman_y, score
    target_x, target_y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
    pacman_direction = (target_x - pacman_x, target_y - pacman_y)

    # Check for collisions with walls
    new_x = pacman_x + pacman_direction[0]
    new_y = pacman_y + pacman_direction[1]
    if (0 <= new_x < GRID_WIDTH) and (0 <= new_y < GRID_HEIGHT):
        pacman_x = new_x
        pacman_y = new_y

    # Check for pellet collisions
    for pellet_x, pellet_y in pellets[:]:
        if (pacman_x, pacman_y) == (pellet_x, pellet_y):
            pellets.remove((pellet_x, pellet_y))
            score += 10

def move_ghosts():
    global ghosts
    for i in range(len(ghosts)):
        dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        new_x = ghosts[i][0] + dx
        new_y = ghosts[i][1] + dy

        # Check for collisions with walls
        if (0 <= new_x < GRID_WIDTH) and (0 <= new_y < GRID_HEIGHT):
            ghosts[i] = (new_x, new_y)

def check_collisions():
    global score

    # Check for ghost collisions
    for ghost_x, ghost_y in ghosts:
        if (pacman_x, pacman_y) == (ghost_x, ghost_y):
            return True

    return False

def main():
    global score
    clock = pygame.time.Clock()
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

        mouse_pos = pygame.mouse.get_pos()
        move_pacman(mouse_pos)
        move_ghosts()
        game_over = check_collisions()

        screen.fill(BLACK)
        draw_grid()
        draw_pellets()

        for ghost_x, ghost_y in ghosts:
            pygame.draw.rect(screen, RED, (ghost_x * GRID_SIZE, ghost_y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        pygame.draw.circle(screen, YELLOW, (pacman_x * GRID_SIZE + GRID_SIZE // 2, pacman_y * GRID_SIZE + GRID_SIZE // 2), 10)

        # Display score in the score area
        pygame.draw.rect(screen, BLACK, score_area)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (score_area.x + 10, score_area.y + 5))

        pygame.display.flip()
        clock.tick(10)

    # Display "Game Over" and final score on a black screen
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Final Score: {score}", True, RED)
    screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2 - 20))
    screen.blit(score_text, (WIDTH // 2 - 80, HEIGHT // 2 + 20))
    pygame.display.flip()
    pygame.time.wait(2000)  # Display the game over message for 2 seconds

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

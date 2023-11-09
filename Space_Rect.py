import time
import pygame
import random

# Initialize Pygame and set up the window
pygame.font.init()
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("space rect")

# Load background image and set up player and star properties
BG = pygame.transform.scale(pygame.image.load("add_photo-here"), (WIDTH, HEIGHT))
PLAYER_WIDTH, PLAYER_HEIGHT = 40, 60
PLAYER_VEL = 5
STAR_WIDTH, STAR_HEIGHT = 10, 20
STAR_VEL = 3
FONT = pygame.font.SysFont("comicsans", 30)

# Function to draw game objects on the window
def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    # Display elapsed time
    time_txt = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_txt, (10, 10))

    # Draw player and stars
    pygame.draw.rect(WIN, "red", player)
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

# Main game loop
def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        # Add stars to the screen at regular intervals
        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL

        # Update star positions and check for collisions with the player
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height > player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        # If the player is hit, display a message and exit the game loop
        if hit:
            lost_txt = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_txt, (WIDTH/2 - lost_txt.get_width()/2, HEIGHT/2 - lost_txt.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        # Draw game objects
        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == '__main__':
    main()

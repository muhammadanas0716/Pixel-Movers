import sys

import pygame

pygame.init()

# GLOBAL VARIABLES 🎓
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
ICON = pygame.image.load("graphics/Player/jump.png")
TITLE = "Pixel Movers UNDER CONSTRUCTION - RESTRICTED"  # TODO: Change the Title
FONT = pygame.font.Font("font/Pixeltype.ttf", 50)

# GAME CONFIG 📐
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()

# SURFACES
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

score_surface = FONT.render("Score", False, (64, 64, 64))
score_rectangle = score_surface.get_rect(center=(400, 50))

player_surface = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_rectangle = player_surface.get_rect(topleft=(50, 216))

snail_surface = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(topleft=(600, 263))

# EVENT LOOP 🖼
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("Byeee 👊")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("jump")

    # Draw all objects/surfaces 🎭
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    pygame.draw.rect(screen, "#c0e8ec", score_rectangle)
    pygame.draw.rect(screen, "#c0e8ec", score_rectangle, 6)
    screen.blit(score_surface, score_rectangle)
    screen.blit(player_surface, player_rectangle)

    # SNAIL MOVING LOGIC
    snail_rectangle.x -= 1
    if snail_rectangle.x < -100:
        snail_rectangle.x = 850
    screen.blit(snail_surface, snail_rectangle)

    # COLLISION LOGIC
    if snail_rectangle.colliderect(player_rectangle):
        print("COLLISION")

    # Update the display 🎯
    pygame.display.update()
    clock.tick(120)

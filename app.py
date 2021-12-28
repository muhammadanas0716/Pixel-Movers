import sys

import pygame

pygame.init()

# GLOBAL VARIABLES 🎓
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
ICON = pygame.image.load("graphics/Player/jump.png")
TITLE = "Pixel Movers UNDER CONSTRUCTION - RESTRICTED"  # TODO: Change the Title
FONT = pygame.font.Font("font/Pixeltype.ttf", 50)


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = FONT.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time


# GAME CONFIG 📐
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()
GAME_ACTIVE = False
start_time = 0
score = 0

# SURFACES
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# PLAYER SURFACE
player_surface = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_rectangle = player_surface.get_rect(topleft=(50, 216))
player_gravity = 0

# INTRO SCREEN
player_stand_start_screen = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand_start_screen = pygame.transform.rotozoom(player_stand_start_screen, 0, 2)
player_stand_start_screen_rectangle = player_stand_start_screen.get_rect(center=(400, 200))
player_stand_start_screen_text = FONT.render("PRESS SPACE BAR TO START GAME", False, (64, 64, 64))

game_title = FONT.render("PIXEL RUNNER", False, (111, 196, 169))
game_title_rectangle = game_title.get_rect(center=(400, 80))

game_instruction = FONT.render("PRESS SPACE TO START GAME", False, (111, 196, 169))
game_instruction_rectangle = game_instruction.get_rect(center=(400, 320))



# SNAIL SURFACE
snail_surface = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
snail_rectangle = snail_surface.get_rect(topleft=(600, 263))

# EVENT LOOP 🖼
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("Byeee 👊")

        if GAME_ACTIVE:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom == 300:
                    player_gravity = -21

            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom == 300:
                if player_rectangle.collidepoint(event.pos):
                    player_gravity = -21
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GAME_ACTIVE = True
                snail_rectangle.x = 850
                start_time = int(pygame.time.get_ticks() / 1000)

    if GAME_ACTIVE:
        # Draw all objects/surfaces 🎭
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player - LOGIC - ALL
        screen.blit(player_surface, player_rectangle)
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300

        # SNAIL MOVING LOGIC - ALL
        snail_rectangle.x -= 4
        if snail_rectangle.x < -100:
            snail_rectangle.x = 850
        screen.blit(snail_surface, snail_rectangle)

        # COLLISION LOGIC/GAME END - ALL
        if snail_rectangle.colliderect(player_rectangle):
            GAME_ACTIVE = False

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_start_screen, player_stand_start_screen_rectangle)
        screen.blit(game_title, game_title_rectangle)
        game_score = FONT.render(f"SCORE: {score}", False, (111, 196, 169))
        game_score_rectangle = game_score.get_rect(center=(400, 330))
        if score == 0:
            screen.blit(game_instruction, game_instruction_rectangle)
        else:
            screen.blit(game_score, game_score_rectangle)

    # Update the display 🎯
    pygame.display.update()
    clock.tick(60)

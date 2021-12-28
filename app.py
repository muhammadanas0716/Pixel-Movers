import sys
import pygame
from random import randint

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walking_animations = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walking_animations[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300


    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.08
            if self.player_index >= len(self.player_walking_animations):
                self.player_index = 0
            self.image = self.player_walking_animations[int(self.player_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


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
game_active = False
start_time = 0
score = 0

player = pygame.sprite.GroupSingle()
player.add(Player())


# DISPLAY SCORE - FUNCTION
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = FONT.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time


# OBSTACLE MOVEMENT - FUNCTION
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


# COLLISION - FUNCTION
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


# PLAYER ANIMATION
def player_animation():
    global player_surface, player_index
    if player_rectangle.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.08
        if player_index >= len(player_walking_animations):
            player_index = 0
        player_surface = player_walking_animations[int(player_index)]


# SURFACES
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# PLAYER SURFACE
player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walking_animations = [player_walk_1, player_walk_2]
player_index = 0
player_surface = player_walking_animations[player_index]
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

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

# ####**OBSTACLES**#####
# SNAIL SURFACE
snail_frame_1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
snail_index = 0
snail_frames = [snail_frame_1, snail_frame_2]
snail_surface = snail_frames[snail_index]

# FLY SURFACE
fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_index = 0
fly_surface = fly_frames[fly_index]

# OBSTACLE RECTS LIST
obstacle_rect_list = []

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# EVENT LOOP 🖼
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("Byeee 👊")

        # COLLISION LOGIC
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom == 300:
                    player_gravity = -21

            if event.type == pygame.MOUSEBUTTONDOWN and player_rectangle.bottom == 300:
                if player_rectangle.collidepoint(event.pos):
                    player_gravity = -21
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        # ENEMY SPAWN and ANIMATION LOGIC
        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surface.get_rect(bottomright=(randint(900, 1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(bottomright=(randint(900, 1100), 200)))
            if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index = 0
                snail_surface = snail_frames[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_frames[fly_index]

    # DRAWING ALL OBJECTS LOGIC
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        # Player - LOGIC - ALL
        player_animation()
        screen.blit(player_surface, player_rectangle)
        player_gravity += 1
        player_rectangle.y += player_gravity
        if player_rectangle.bottom >= 300:
            player_rectangle.bottom = 300
        player.draw(screen)
        player.update()

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        game_active = collisions(player_rectangle, obstacle_rect_list)

    # START AND GAME END SCREEN
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_start_screen, player_stand_start_screen_rectangle)
        screen.blit(game_title, game_title_rectangle)
        obstacle_rect_list.clear()
        game_score = FONT.render(f"SCORE: {score}", False, (111, 196, 169))
        game_score_rectangle = game_score.get_rect(center=(400, 330))

        if score == 0:
            screen.blit(game_instruction, game_instruction_rectangle)
        else:
            screen.blit(game_score, game_score_rectangle)

    # Update the display 🎯
    pygame.display.update()
    clock.tick(60)

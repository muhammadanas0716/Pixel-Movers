import sys
import pygame
from random import randint, choice

pygame.init()


# PLAYER CLASS
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walking_animations = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walking_animations[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

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


# OBSTACLE CLASS
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly_frame_1 = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_position = 210
        else:
            snail_frame_1 = pygame.image.load("graphics/Snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphics/Snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_position = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_position))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


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
background_music = pygame.mixer.Sound("audio/music.wav")
background_music.set_volume(0.8)

# GROUPS
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()
obstacle_group.add(Obstacle("fly"))


# DISPLAY SCORE - FUNCTION
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = FONT.render(f"Score: {current_time}", False, (64, 64, 64))
    score_rectangle = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rectangle)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# SURFACES
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# INTRO SCREEN
player_stand_start_screen = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand_start_screen = pygame.transform.rotozoom(player_stand_start_screen, 0, 2)
player_stand_start_screen_rectangle = player_stand_start_screen.get_rect(center=(400, 200))
player_stand_start_screen_text = FONT.render("PRESS SPACE BAR TO START GAME", False, (64, 64, 64))

game_title = FONT.render("PIXEL RUNNER", False, (111, 196, 169))
game_title_rectangle = game_title.get_rect(center=(400, 80))

game_instruction = FONT.render("PRESS SPACE TO START GAME", False, (111, 196, 169))
game_instruction_rectangle = game_instruction.get_rect(center=(400, 320))


# Timer(s)
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# EVENT LOOP 🎁
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit("Game Over!")

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                background_music.play(loops=-1)

    # DRAWING ALL OBJECTS LOGIC
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    # START AND GAME END SCREEN
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

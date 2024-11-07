import sys
import pygame
from random import randint, choice
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400
PLAYER_START_POS = (80, 300)
PLAYER_GRAVITY = 1
PLAYER_JUMP_FORCE = -20
OBSTACLE_SPEED = 6
OBSTACLE_SPAWN_INTERVAL = 1500
ICON_PATH = os.path.join("graphics", "Player", "jump.png")
FONT_PATH = os.path.join("font", "Pixeltype.ttf")
BACKGROUND_MUSIC_PATH = os.path.join("audio", "music.wav")
JUMP_SOUND_PATH = os.path.join("audio", "jump.mp3")

# Set up Display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pixel Movers")
pygame.display.set_icon(pygame.image.load(ICON_PATH))

# Font
FONT = pygame.font.Font(FONT_PATH, 50)

# Load Background Music
background_music = pygame.mixer.Sound(BACKGROUND_MUSIC_PATH)
background_music.set_volume(0.2)

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.load_assets()
        self.image = self.player_walking_animations[self.player_index]
        self.rect = self.image.get_rect(midbottom=PLAYER_START_POS)
        self.gravity = 0

    def load_assets(self):
        self.player_walking_animations = [
            pygame.image.load(os.path.join("graphics", "Player", "player_walk_1.png")).convert_alpha(),
            pygame.image.load(os.path.join("graphics", "Player", "player_walk_2.png")).convert_alpha()
        ]
        self.player_jump = pygame.image.load(os.path.join("graphics", "Player", "jump.png")).convert_alpha()
        self.player_index = 0
        self.jump_sound = pygame.mixer.Sound(JUMP_SOUND_PATH)
        self.jump_sound.set_volume(0.8)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = PLAYER_JUMP_FORCE
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += PLAYER_GRAVITY
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

# Obstacle Class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.frames = self.load_obstacle_frames(type)
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), self.get_y_position(type)))

    def load_obstacle_frames(self, type):
        if type == "fly":
            return [
                pygame.image.load(os.path.join("graphics", "Fly", "Fly1.png")).convert_alpha(),
                pygame.image.load(os.path.join("graphics", "Fly", "Fly2.png")).convert_alpha()
            ]
        elif type == "snail":
            return [
                pygame.image.load(os.path.join("graphics", "Snail", "snail1.png")).convert_alpha(),
                pygame.image.load(os.path.join("graphics", "Snail", "snail2.png")).convert_alpha()
            ]
        else:
            raise ValueError(f"Unknown obstacle type: {type}")

    @staticmethod
    def get_y_position(type):
        return 210 if type == "fly" else 300

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.x <= -100:
            self.kill()

# Functions
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

# Surfaces
sky_surface = pygame.image.load(os.path.join("graphics", "Sky.png")).convert()
ground_surface = pygame.image.load(os.path.join("graphics", "ground.png")).convert()
player_stand_start_screen = pygame.image.load(os.path.join("graphics", "Player", "player_stand.png")).convert_alpha()
player_stand_start_screen = pygame.transform.rotozoom(player_stand_start_screen, 0, 2)
player_stand_start_screen_rectangle = player_stand_start_screen.get_rect(center=(400, 200))
game_title = FONT.render("PIXEL RUNNER", False, (111, 196, 169))
game_title_rectangle = game_title.get_rect(center=(400, 80))
game_instruction = FONT.render("PRESS SPACE TO START GAME", False, (111, 196, 169))
game_instruction_rectangle = game_instruction.get_rect(center=(400, 320))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, OBSTACLE_SPAWN_INTERVAL)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

# Game Variables
clock = pygame.time.Clock()
game_active = False
start_time = 0
score = 0

# Game Loop
while True:
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

    # Draw and Update Game Elements
    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        score = display_score()

        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()
        game_active = collision_sprite()
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

    pygame.display.update()
    clock.tick(60)

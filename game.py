import pygame
from pygame.locals import *
import sys
import random
import os

pygame.init()

# Game window size
width = 800
height = 600

# Create the game window
screen = pygame.display.set_mode((width, height))

# Set the window title
pygame.display.set_caption("Pokemon Battle: Pikachu vs Meowth")

# Load and scale images
bg_img = pygame.image.load("bg_img.png")
bg_img = pygame.transform.scale(bg_img, (width, height))

pikachu_img = pygame.image.load("pikachu_img.png")
pikachu_img = pygame.transform.scale(pikachu_img, (200, 200))

meowth_img = pygame.image.load("meowth_img.png")
meowth_img = pygame.transform.scale(meowth_img, (250, 250))


meowthko_img = pygame.image.load("meowthko_img.png")
meowthko_img = pygame.transform.scale(meowthko_img, (250, 250))


# Load sounds
battle_music = pygame.mixer.Sound("./sounds/battle_music.mp3")
pikachu_attack_sound = pygame.mixer.Sound("./sounds/thunderpika.wav")
meowth_attack_sound = pygame.mixer.Sound("./sounds/meowth_attack.wav")

# Animation
def load_animation_images(folder_path):
    animation_imgs = []
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith('.png'):
            img_path = os.path.join(folder_path, file_name)
            img = pygame.image.load(img_path)
            animation_imgs.append(img)
    return animation_imgs

thunder_imgs = load_animation_images("animation/thunder")
scratch_imgs = load_animation_images("animation/scratch")

class Pokemon:
    def __init__(self, name, image, hp, attack_power, attack_name, attack_sound, animation_imgs, animation_x_offset, animation_y_offset):
        self.name = name
        self.image = image
        self.hp = hp
        self.attack_power = attack_power
        self.attack_name = attack_name
        self.attack_sound = attack_sound
        self.visible = True
        self.attacked_time = -10000  # Store the time when the Pokémon was attacked
        self.animation_imgs = animation_imgs
        self.animation_frame_duration = 100
        self.animation_x_offset = animation_x_offset
        self.animation_y_offset = animation_y_offset
        self.anim_start_time = 0  # Added this line
        self.anim_frame = 0  # Added this line

    def attack(self, opponent):
        opponent.hp -= self.attack_power
        pygame.mixer.Sound.play(self.attack_sound)
        opponent.attacked_time = pygame.time.get_ticks()  # Record the time of the attack

    def play_animation(self, screen, x, y, animation_duration):
        if self.anim_start_time == 0:
            self.anim_start_time = pygame.time.get_ticks()

        elapsed_time = pygame.time.get_ticks() - self.anim_start_time
        if elapsed_time < animation_duration:
            self.anim_frame = (self.anim_frame + 1) % len(self.animation_imgs)
            current_frame = self.animation_imgs[self.anim_frame]
            screen.blit(current_frame, (x + self.animation_x_offset, y + self.animation_y_offset))
        else:
            self.anim_start_time = 0
            self.anim_frame = 0
            return True
        return False

# Set animation offsets (change these values to adjust the animation positions)
pikachu_animation_offset_x = 50
pikachu_animation_offset_y = -20

meowth_animation_offset_x = 100
meowth_animation_offset_y = 100
pikachu = Pokemon("Pikachu", pikachu_img, 100, 30, "Thunderbolt", pikachu_attack_sound, thunder_imgs, pikachu_animation_offset_x, pikachu_animation_offset_y)
meowth = Pokemon("Meowth", meowth_img, 100, 15, "Scratch", meowth_attack_sound, scratch_imgs, meowth_animation_offset_x, meowth_animation_offset_y)

# Desired position for Pikachu
desired_x_pika = 115
desired_y_pika = 395

# Desired position for Meowth
desired_x_meo = 450
desired_y_meo = 150

clock = pygame.time.Clock()
FPS = 60
player_turn = True
battle_music.play(-1)

# Function to draw the health bars
def draw_health_bars():
    hp_bar_width = 200
    hp_bar_height = 15

    # Position for Pikachu's HP bar
    pikachu_hp_bar_x = width * 0.20
    pikachu_hp_bar_y = height * 0.65

    # Position for Meowth's HP bar
    meowth_hp_bar_x = width * 0.70
    meowth_hp_bar_y = height * 0.28

    # Background
    pygame.draw.rect(screen, (255, 0, 0), (pikachu_hp_bar_x, pikachu_hp_bar_y, hp_bar_width, hp_bar_height))
    pygame.draw.rect(screen, (255, 0, 0), (meowth_hp_bar_x, meowth_hp_bar_y, hp_bar_width, hp_bar_height))

    # Health
    pygame.draw.rect(screen, (0, 0, 255), (pikachu_hp_bar_x, pikachu_hp_bar_y, pikachu.hp * hp_bar_width // 100, hp_bar_height))
    pygame.draw.rect(screen, (0, 0, 255), (meowth_hp_bar_x, meowth_hp_bar_y, meowth.hp * hp_bar_width // 100, hp_bar_height))
    # HP labels
    font = pygame.font.Font(None, 24)
    hp_label = font.render("HP", True, (255, 255, 255))
    screen.blit(hp_label, (pikachu_hp_bar_x - 30, pikachu_hp_bar_y + 5))
    screen.blit(hp_label, (meowth_hp_bar_x - hp_label.get_width() - 10, meowth_hp_bar_y + 5))

# Function to check the winner and display the result
def check_winner():
    if pikachu.hp <= 0 or meowth.hp <= 0:
        font = pygame.font.Font(None, 72)
        winner = "Pikachu" if pikachu.hp > meowth.hp else "Meowth"
        text = font.render(f"{winner} wins!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, int(height * 0.1)))
        screen.blit(text, text_rect)


# Main game loop
animation_playing = False
charging = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE and not animation_playing and not charging:
                if player_turn:
                    pikachu.attack(meowth)
                    meowth.attacked_time = pygame.time.get_ticks()
                else:
                    meowth.attack(pikachu)
                    pikachu.attacked_time = pygame.time.get_ticks()

                animation_playing = True
                player_turn = not player_turn

    current_time = pygame.time.get_ticks()

    meowth.visible = not (current_time - meowth.attacked_time < 3000 and current_time % 200 < 100)
    pikachu.visible = not (current_time - pikachu.attacked_time < 1000 and current_time % 200 < 100)

    screen.blit(bg_img, (0, 0))

    if pikachu.visible:
        screen.blit(pikachu.image, (desired_x_pika, desired_y_pika))

    if meowth.visible:
        if meowth.hp <= 0:
            screen.blit(meowthko_img, (desired_x_meo, desired_y_meo))
        else:
            screen.blit(meowth.image, (desired_x_meo, desired_y_meo))

    if animation_playing:
        if player_turn:
            animation_playing = not meowth.play_animation(screen, desired_x_pika, desired_y_pika, 1000)
        else:
            animation_playing = not pikachu.play_animation(screen,desired_x_meo, desired_y_meo , 3000)

    draw_health_bars()
    check_winner()

    pygame.display.update()
    clock.tick(FPS)


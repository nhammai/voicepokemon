import pygame
from pygame.locals import *
import sys
import random


pygame.init()

# Game window size
width = 800
height = 600

# Create the game window
screen = pygame.display.set_mode((width, height))

# Set the window title
pygame.display.set_caption("Pokemon Battle: Pikachu vs Meowth")

# # Load images
# bg_img = pygame.image.load("bg_img.png")
# pikachu_img = pygame.image.load("pikachu_img.png")
# meowth_img = pygame.image.load("meowth_img.png")





# Load and scale images
bg_img = pygame.image.load("bg_img.png")
bg_img = pygame.transform.scale(bg_img, (width, height))

pikachu_img = pygame.image.load("pikachu_img.png")
pikachu_img = pygame.transform.scale(pikachu_img, (200, 200))

meowth_img = pygame.image.load("meowth_img.png")
meowth_img = pygame.transform.scale(meowth_img, (250, 250))




# # Position characters
# pikachu_x = 100
# pikachu_y = height // 2 - pikachu_img.get_height() // 2

# meowth_x = width - meowth_img.get_width() - 100
# meowth_y = height // 2 - meowth_img.get_height() // 2





# Load sounds
battle_music = pygame.mixer.Sound("./sounds/battle_music.mp3")
pikachu_attack_sound = pygame.mixer.Sound("./sounds/pikachu_attack.wav")
meowth_attack_sound = pygame.mixer.Sound("./sounds/meowth_attack.wav")


class Pokemon:
    def __init__(self, name, image, hp, attack_power, attack_name, attack_sound):
        self.name = name
        self.image = image
        self.hp = hp
        self.attack_power = attack_power
        self.attack_name = attack_name
        self.attack_sound = attack_sound

    def attack(self, opponent):
        opponent.hp -= self.attack_power
        pygame.mixer.Sound.play(self.attack_sound)


pikachu = Pokemon("Pikachu", pikachu_img, 100, 20, "Thunderbolt", pikachu_attack_sound)
meowth = Pokemon("Meowth", meowth_img, 100, 15, "Scratch", meowth_attack_sound)


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

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                if player_turn:
                    pikachu.attack(meowth)
                else:
                    meowth.attack(pikachu)

                player_turn = not player_turn

    # Update game display
    screen.blit(bg_img, (0, 0))
    # screen.blit(pikachu.image, (pikachu_x, pikachu_y))
    screen.blit(meowth.image, (desired_x_meo, desired_y_meo))

    # Update game display
    screen.blit(pikachu.image, (desired_x_pika, desired_y_pika))


    # Update health bars
    hp_bar_width = 200
    hp_bar_height = 15

    # Position for Pikachu's HP bar
    pikachu_hp_bar_x = width * 0.20  # 20% of the width
    pikachu_hp_bar_y = height * 0.65  # 65% of the height

    # Position for Meowth's HP bar
    meowth_hp_bar_x = width * 0.70   # 70% of the width
    meowth_hp_bar_y = height * 0.28  # 28% of the height

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




       # Check for a winner
    font = pygame.font.Font(None, 36)
    if pikachu.hp <= 0 or meowth.hp <= 0:
        winner = "Pikachu" if pikachu.hp > meowth.hp else "Meowth"
        text = font.render(f"{winner} wins!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

    pygame.display.update()
    clock.tick(FPS)

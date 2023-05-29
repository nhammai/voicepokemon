import pygame
from pygame.locals import *
import sys
import random
import os
import time
from understandjson import load_json_file

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

ko_img = pygame.image.load("KO.png")
ko_img = pygame.transform.scale(ko_img, (250, 125))  # Adjust the size as needed

pikachu_front_img = pygame.image.load("pikachu_front_img.png")
pikachu_front_img = pygame.transform.scale(pikachu_front_img, (320, 320))

pikachuko_img = pygame.image.load("pikachuuuuuu.png")
pikachuko_img = pygame.transform.scale(pikachuko_img, (250, 141))

meowth_win_img = pygame.image.load("meowth_win.png")
meowth_win_img = pygame.transform.scale(meowth_win_img, (250, 250))


# Load sounds
battle_music = pygame.mixer.Sound("./sounds/battle_music.mp3")
battle_music.set_volume(0.3)  # Add this line to adjust the volume

ko_sound = pygame.mixer.Sound("./sounds/KObig.wav")
ko_sound.set_volume(1.0)  # Adjust the volume; 1.0 is the maximum volume


victory_full_sound = pygame.mixer.Sound("./sounds/victorfull.wav")
victory_full_sound.set_volume(0.9)

pikachu_sound = pygame.mixer.Sound("./sounds/pikapika_big.wav")

pikachu_e_charge = pygame.mixer.Sound("./sounds/echarge.wav")
# play pikachu sound
def play_pikachu_sound():
    pygame.mixer.Sound.play(pikachu_sound)

# play pikachu sound
def play_pikachu_ready():
    pygame.mixer.Sound.play(pikachu_e_charge)

superthundersound = pygame.mixer.Sound("./sounds/pikachu_attack.wav")

# attack sound
## pikachu attack sound
thunder_attack_sound = pygame.mixer.Sound("./sounds/thunderpika.wav")
electricball_attack_sound = pygame.mixer.Sound("./sounds/superelectricballshort.wav")
irontail_attack_sound = pygame.mixer.Sound("./sounds/irontailsuper.wav")

## meo attack sound
scratch_attack_sound = pygame.mixer.Sound("./sounds/scratch.wav")
bite_attack_sound = pygame.mixer.Sound("./sounds/bite.wav")
bomb_attack_sound = pygame.mixer.Sound("./sounds/bomb.wav")



# Animation
def load_animation_images(folder_path):
    animation_imgs = []
    for file_name in sorted(os.listdir(folder_path)):
        if file_name.endswith('.png'):
            img_path = os.path.join(folder_path, file_name)
            img = pygame.image.load(img_path)
            animation_imgs.append(img)
    return animation_imgs

# Load animation file
thunder_imgs = load_animation_images("animation/thunder")
electricball_imgs = load_animation_images("animation/electricball4")
irontail_imgs = load_animation_images("animation/irontail")
bite_imgs = load_animation_images("animation/bite")
bomb_imgs = load_animation_images("animation/bomb")
scratch_imgs = load_animation_images("animation/scratch")
thunder_weak_imgs = load_animation_images("animation/thunder_weak")
thunder_super = load_animation_images("animation/thunder_tim")


# animation offset (location of the animate)
thunder_animation_offset_x = 50
thunder_animation_offset_y = -20
electricball_animation_offset_x =70
electricball_animation_offset_y = 50
irontail_animation_offset_x = 70
irontail_animation_offset_y = 70

## location for animation meowth attack
scratch_animation_offset_x = 100
scratch_animation_offset_y = 100

bite_animation_offset_x = 100
bite_animation_offset_y = 100

bomb_animation_offset_x = 100
bomb_animation_offset_y = 100




# Create meo option the make it auto attack
meo_options = ["scratch", "scratch", "scratch", "bite", "bite", "bomb", "bomb"]
def meo_auto(options):
    return random.choice(options)

# choice = meo_auto(meo_options)
# if choice == "scratch":
# elif choice == "bite":
# elif choice == "bomb":

# add play again button

def text_objects(text, font):
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()


def draw_button(screen, message, x, y, w, h, ic, ac, action=None):
    # ic is the inactive color (when the mouse is not hovering over it)
    # ac is the active color (when the mouse is hovering over it)
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Increase the button size
    w += 20  # Increase the width
    h += 10  # Increase the height

    # Draw button with rounded corners
    rect = pygame.Rect(x, y, w, h)
    alpha = 0  # This makes corners invisible

    # Draw the rectangles that will be used for creating rounded corners
    pygame.draw.rect(screen, (0, 0, 0, alpha), rect, border_radius=25)
    pygame.draw.rect(screen, ic, rect.inflate(-4, -4), border_radius=25)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, (0, 0, 0, alpha), rect, border_radius=25)
        pygame.draw.rect(screen, ac, rect.inflate(-4, -4), border_radius=25)
        if click[0] == 1 and action != None:
            action()   

    # Increase the text size
    smallText = pygame.font.Font(None, 25)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurf, textRect)


def reset_game():
    
    global pikachu, meowth, player_turn, animation_playing, last_pikachu_attack
    pikachu = Pokemon("Pikachu", pikachu_img, 42, 100, 100,20, "Thunderbolt", thunder_attack_sound, thunder_imgs, thunder_animation_offset_x, thunder_animation_offset_y)
    meowth = Pokemon("Meowth", meowth_img, 50,100,100, 15, "Scratch", scratch_attack_sound, scratch_imgs, scratch_animation_offset_x, scratch_animation_offset_y)
    player_turn = True
    animation_playing = False
    last_pikachu_attack = 0
    battle_music.play(-1)



class Pokemon:
    def __init__(self, name, image, level, hp,max_hp, attack_power, attack_name, attack_sound, animation_imgs, animation_x_offset, animation_y_offset):
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
        self.defeated = False  # Add this line
        self.ko_sound_played = False  # Add this line
        self.ko_displayed = False  # Add this line
        self.winner_banner_displayed = False  # Add this line
        self.sound_played = False  # Add this line
        self.level = level
        self.max_hp = max_hp
        


    def attack(self, opponent):
        if not self.defeated and not opponent.defeated:  # Add this line to check if either Pokemon is defeated
            opponent.hp -= self.attack_power
            pygame.mixer.Sound.play(self.attack_sound)
            opponent.attacked_time = pygame.time.get_ticks()  # Record the time of the attack

    def play_animation(self, screen, x, y, animation_duration):
        if not self.defeated:  # Add this line to check if the Pokemon is defeated
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
# pikachu_animation_offset_x = 50
# pikachu_animation_offset_y = -20

scratch_animation_offset_x = 100
scratch_animation_offset_y = 100


# pikachu = Pokemon("Pikachu", pikachu_img, 100, 20, "Thunderbolt", thunder_attack_sound, thunder_imgs, thunder_animation_offset_x, thunder_animation_offset_y)
# meowth = Pokemon("Meowth", meowth_img, 100, 15, "Scratch", scratch_attack_sound, scratch_imgs, scratch_animation_offset_x, scratch_animation_offset_y)

# Desired position for Pikachu
desired_x_pika = 115
desired_y_pika = 395

# Desired position for Pikachu KO
desired_x_pikako = 115 - 20
desired_y_pikako = 395 + 70

# Desired position for Meowth
desired_x_meo = 450
desired_y_meo = 150

clock = pygame.time.Clock()
FPS = 60
player_turn = True
battle_music.play(-1)

# Function to draw the health bars
def draw_health_bars():
    if not (pikachu.winner_banner_displayed or meowth.winner_banner_displayed):  # Update this line

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
        pikachu.defeated = pikachu.hp <= 0
        meowth.defeated = meowth.hp <= 0

        current_time = pygame.time.get_ticks()
        if pikachu.defeated and not pikachu.ko_sound_played and current_time - pikachu.attacked_time >= 3000:
            ko_sound.play()
            pikachu.ko_sound_played = True
        if meowth.defeated and not meowth.ko_sound_played and current_time - meowth.attacked_time >= 3000:
            ko_sound.play()
            meowth.ko_sound_played = True

        if (pikachu.defeated and current_time - pikachu.attacked_time >= 3000) or (meowth.defeated and current_time - meowth.attacked_time >= 3000):
            if not ((pikachu.defeated and current_time - pikachu.attacked_time >= 5000) or (meowth.defeated and current_time - meowth.attacked_time >= 5000)):
                screen.blit(ko_img, (200, 200))
                
        current_time = pygame.time.get_ticks()  # This returns the time in milliseconds

        if (pikachu.defeated and current_time - pikachu.attacked_time >= 6000) or (meowth.defeated and current_time - meowth.attacked_time >= 6000):
            pikachu.winner_banner_displayed = True  # Add this line
            meowth.winner_banner_displayed = True  # Add this line
            if pikachu.hp > meowth.hp:
                pikachu.image = pikachu_front_img
                pikachu_winner_pos_x = desired_x_pika -50
                pikachu_winner_pos_y = desired_y_pika - 60  # Adjust this value to move Pikachu's image higher
                screen.blit(pikachu.image, (pikachu_winner_pos_x, pikachu_winner_pos_y))

            elif meowth.hp > pikachu.hp:
                meowth.image = meowth_win_img


            # font = pygame.font.Font(None, 72)
            # winner = "Pikachu" if pikachu.hp > meowth.hp else "Meowth"
            # text = font.render(f"{winner} wins!", True, (255, 255, 255))
            # text_rect = text.get_rect(center=(width // 2, int(height * 0.1)))

            # screen.blit(text, text_rect)
            # draw_button(screen, "Play Again", 350, 450, 100, 50, (0, 200, 0), (0, 255, 0), reset_game)
            winner = "Pikachu" if pikachu.hp > meowth.hp else "Meowth"

            # Create the text and the shadow text
            font = pygame.font.Font(None, 72)  # Increase the size for more epic look
            text = font.render(f"{winner} wins!", True, (255, 215, 0))  # Gold color
            shadow_text = font.render(f"{winner} wins!", True, (0, 0, 0))  # Black color for shadow

            text_rect = text.get_rect(center=(width // 2, int(height * 0.1)))

            # Calculate the position for the shadow text
            shadow_pos = (text_rect.x + 3, text_rect.y + 3)

            # Draw the shadow text and the actual text
            screen.blit(shadow_text, shadow_pos)
            screen.blit(text, text_rect)

            draw_button(screen, "Play Again", 350, 450, 100, 50, (0, 200, 0), (0, 255, 0), reset_game)


        if pikachu.winner_banner_displayed or meowth.winner_banner_displayed:
            if not pikachu.sound_played and not meowth.sound_played:

                victory_full_sound.play()
                pikachu.sound_played = True
                meowth.sound_played = True
                battle_music.stop()  # Stop the background sound


def draw_databox(pokemon, x, y):
    # Two fonts are created here: one for the name and one for the other stats.
    name_font = pygame.font.Font(None, 35)  # Larger size for name
    level_font = pygame.font.Font(None, 30)  # Larger size for level
    databox_font = pygame.font.Font(None, 24)  # Size for other data

    # Load the correct databox image based on the Pokemon.
    if pokemon.name == "Pikachu":
        databox_img = pygame.image.load('databox_normal.png')
        # Scale the image.
        scaled_width = 320  # You can adjust this as needed.
        scaled_height = (scaled_width*84)/260  # You can adjust this as needed.
        databox_img = pygame.transform.scale(databox_img, (scaled_width, scaled_height))

        # Set the text and health bar positions for Pikachu.
        name_position = (x + 50, y + 15)
        level_position = (x + 230, y + 20)
        hp_position = (x + 190, y + 68)
        health_bar_position = (x + 167, y + 51)
    else:
        databox_img = pygame.image.load('databox_normal_foe.png')
                # Scale the image.
        scaled_width = 320  # You can adjust this as needed.
        scaled_height = (scaled_width*62)/260  # You can adjust this as needed.
        databox_img = pygame.transform.scale(databox_img, (scaled_width, scaled_height))

        # Set the text and health bar positions for Meowth.
        name_position = (x + 10, y + 15)  # Adjust as needed.
        level_position = (x + 210, y + 20)  # Adjust as needed.
        hp_position = (x + 40, y + 50)  # Adjust as needed.
        health_bar_position = (x + 145, y + 51)  # Adjust as needed.

    # Get the width of the databox image.
    databox_width = databox_img.get_rect().width

    # Draw the box.
    screen.blit(databox_img, (x, y))

    # Draw the text.
    name_text = name_font.render(f'{pokemon.name.upper()}', True, (98, 98, 99))  # Custom gray text, name is uppercase
    level_text = level_font.render(f'Lv: {pokemon.level}', True, (98, 98, 99))  # Custom gray text
    hp_text = databox_font.render(f'{pokemon.hp}/{pokemon.max_hp}', True, (98, 98, 99))  # Custom gray text

    # Display the text inside the box.
    screen.blit(name_text, name_position)
    screen.blit(level_text, level_position)
    if pokemon.name == "Pikachu":
        screen.blit(hp_text, hp_position)
    

    # Draw the health bar.
    health_ratio = pokemon.hp / pokemon.max_hp
    health_bar_color = (88, 220, 139)  # Hex color #58dc8b
    health_bar_width = int(120 * health_ratio)
    pygame.draw.rect(screen, health_bar_color, pygame.Rect(*health_bar_position, health_bar_width, 6))

    # Return the width of the databox.
    return databox_width






def display_image_and_play_sound(image_path, sound_path, display_time):
    # Load the image
    image = pygame.image.load(image_path)

    # Load the sound
    sound = pygame.mixer.Sound(sound_path)

    # Play the sound
    sound.play()

    # Display the image
    screen.blit(image, (0, 0))

    # Update the screen
    pygame.display.flip()

    # Wait for the specified amount of time
    pygame.time.wait(display_time)


def create_icon_with_border(icon_img, border_color, border_size):
    # Create a new surface with a size larger than the icon by the border size.
    border_img = pygame.Surface((icon_img.get_width() + border_size * 2, icon_img.get_height() + border_size * 2))

    # Fill the new surface with the border color.
    border_img.fill(border_color)

    # Blit the icon onto the middle of the new surface.
    border_img.blit(icon_img, (border_size, border_size))

    return border_img


def apply_glow_effect(icon_img):
    # Create a white surface with the same size as the icon and with per-pixel alpha.
    glow_img = pygame.Surface(icon_img.get_size(), pygame.SRCALPHA)

    # Fill the surface with white and set the alpha value to create a semi-transparent overlay.
    glow_img.fill((255, 255, 255, 128))  # RGBA color

    # Blend the white overlay onto the icon image.
    icon_img.blit(glow_img, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

    return icon_img

def draw_command_box():
    # Load the command box image.
    command_box_img = pygame.image.load('commandbox.png')

    # Scale the image.
    command_box_scaled_width = 405  # Adjust this to your desired size.
    command_box_scaled_height = 180  # Adjust this to your desired size.
    command_box_img = pygame.transform.scale(command_box_img, (command_box_scaled_width, command_box_scaled_height))

    border_color = (0, 0, 0)  # The color of the border. Adjust this to your desired color.
    border_size = 2  # The size of the border. Adjust this to your desired size.

    # Load the command icons.
    pikachu_icon_img = pygame.image.load('iconss/pikachu_icon.png')
    thunder_icon_img = pygame.image.load('iconss/thunder_icon.png')
    electricball_icon_img = pygame.image.load('iconss/electricball_icon.png')
    irontail_icon_img = pygame.image.load('iconss/irontail_icon.png')

    # Scale the icons.
    icon_scaled_width = 60  # Adjust this to your desired size.
    icon_scaled_height = 60  # Adjust this to your desired size.
    pikachu_icon_img = pygame.transform.scale(pikachu_icon_img, (icon_scaled_width, icon_scaled_height))
    thunder_icon_img = pygame.transform.scale(thunder_icon_img, (icon_scaled_width, icon_scaled_height))
    electricball_icon_img = pygame.transform.scale(electricball_icon_img, (icon_scaled_width, icon_scaled_height))
    irontail_icon_img = pygame.transform.scale(irontail_icon_img, (icon_scaled_width, icon_scaled_height))

    # Add borders to the icons.
    pikachu_icon_img = create_icon_with_border(pikachu_icon_img, border_color, border_size)
    thunder_icon_img = create_icon_with_border(thunder_icon_img, border_color, border_size)
    electricball_icon_img = create_icon_with_border(electricball_icon_img, border_color, border_size)
    irontail_icon_img = create_icon_with_border(irontail_icon_img, border_color, border_size)

    # Define the text.
    font = pygame.font.Font(None, 30)  # Adjust the font size to fit your command box.
    pikachu_text = font.render("Pikachu", True, (255, 255, 255))
    thunder_text = font.render("Phóng điện", True, (255, 255, 255))
    electricball_text = font.render("Quả cầu điện", True, (255, 255, 255))
    irontail_text = font.render("Đuôi thép", True, (255, 255, 255))
    instruction_text = font.render("Đọc to Pikachu để kích hoạt và ra lệnh", True, (255, 255, 255))

    # Draw the command box.
    command_box_position = (402, 425)  # Bottom-right position, adjust this to fit
    # Bottom-right position, adjust this to fit your screen.
    screen.blit(command_box_img, command_box_position)

    # Draw the icons and corresponding text.
    icon_positions = [(430, 500), (520, 500), (610, 500), (700, 500)]  # Adjust these positions according to your desired layout.
    text_positions = [(430, 570), (500, 570), (600, 570), (700, 570)]  # Adjust these positions according to your desired layout.
    icons = [pikachu_icon_img, thunder_icon_img, electricball_icon_img, irontail_icon_img]
    texts = [pikachu_text, thunder_text, electricball_text, irontail_text]
    for icon_position, text_position, icon, text in zip(icon_positions, text_positions, icons, texts):
        screen.blit(icon, icon_position)
        screen.blit(text, text_position)

    # Draw the instruction text.
    instruction_text_position = (430, 470)  # Adjust this position to fit your desired layout.
    screen.blit(instruction_text, instruction_text_position)




# Main game loop
last_pikachu_attack_time = 0


def game_loop():
    global pikachu, meowth, player_turn, animation_playing, last_pikachu_attack, last_pikachu_attack_time

    pikachu = Pokemon("Pikachu", pikachu_img, 42,100,100, 20, "Thunderbolt", thunder_attack_sound, thunder_imgs, thunder_animation_offset_x, thunder_animation_offset_y)
    meowth = Pokemon("Meowth", meowth_img, 50, 100,100, 15, "Scratch", scratch_attack_sound, scratch_imgs, scratch_animation_offset_x, scratch_animation_offset_y)
    player_turn = True
    animation_playing = False
    last_pikachu_attack = 0
    battle_music.play(-1)
    # display_image_and_play_sound('pikachuvsmeowth.png', 'sounds/vs.wav', 4000)

    # meowth_attack_delay = random.randint(3000, 6000)  # 3 or 6 seconds in milliseconds
    timedelay = 0



    while True:


        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_a:  # Reset the game when 'A' is pressed
                    pikachu = Pokemon("Pikachu", pikachu_img, 42, 100,100, 20, "Thunderbolt", thunder_attack_sound, thunder_imgs, thunder_animation_offset_x, thunder_animation_offset_y)
                    meowth = Pokemon("Meowth", meowth_img, 50, 100,100, 15, "Scratch", scratch_attack_sound, scratch_imgs, scratch_animation_offset_x, scratch_animation_offset_y)
                    player_turn = True
                    animation_playing = False
                    last_pikachu_attack = 0
                    battle_music.play(-1)

                if event.key == K_SPACE and not animation_playing and player_turn:
                    # cm = read_command("command.txt") ## read the amount to modify power
                    command = load_json_file('command.json')

                    print(command)

                    if (command["command"] == "thunder"):
                        play_pikachu_ready()
                        timedelay = random.randint(5000, 7000)
                        pikachu.attack_name = "Thunderbolt"
                        pikachu.animation_imgs = thunder_imgs
                        
                        pikachu.attack_power = command["amount"]*40/10000
                        pikachu.attack_sound = thunder_attack_sound
                        print(pikachu.attack_power)
                        if(pikachu.attack_power <40): # change the animation depend on the attack power
                            pikachu.animation_imgs = thunder_weak_imgs
                        if(pikachu.attack_power>400):
                            pikachu.animation_imgs = thunder_super
                            superthundersound.play()
                            superthundersound.play()
                        time.sleep(2)
                    elif (command["command"] == "electricball"):
                        timedelay = random.randint(3000, 6000)
                        pikachu.attack_power = 30
                        pikachu.attack_name = "Electricball"
                        pikachu.attack_sound = electricball_attack_sound
                        pikachu.animation_imgs = electricball_imgs
                        pikachu.animation_x_offset = electricball_animation_offset_x
                        pikachu.animation_y_offset = electricball_animation_offset_y
                    elif (command["command"] == "irontail"):
                        timedelay = random.randint(2000, 5000)
                        pikachu.attack_power = 20
                        pikachu.attack_name = "Irontail"
                        pikachu.attack_sound = irontail_attack_sound
                        pikachu.animation_imgs = irontail_imgs
                        pikachu.animation_x_offset = irontail_animation_offset_x
                        pikachu.animation_y_offset = irontail_animation_offset_y

                    else:
                        timedelay = random.randint(5000, 7000)
                        pikachu.attack_name = "Thunderbolt"
                        pikachu.attack_power = command["amount"]*40/10000
                        pikachu.attack_sound = thunder_attack_sound
                        pikachu.animation_imgs = thunder_imgs


                    pikachu.attack(meowth)
                    pikachu.attack_power = 40 # return to normal attack power
                    
                    player_turn = not player_turn
                    animation_playing = True
                    last_pikachu_attack_time = pygame.time.get_ticks()

                elif event.key == K_p:
                    play_pikachu_sound()

        current_time = pygame.time.get_ticks()
        if not player_turn and not animation_playing and not meowth.defeated:
            
            choice = meo_auto(meo_options)
            if choice == "scratch":
                meowth.attack_power = 15
                meowth.attack_name = "Scratch"
                meowth.attack_sound = scratch_attack_sound
                meowth.animation_imgs = scratch_imgs
                meowth.animation_x_offset = scratch_animation_offset_x
                meowth.animation_y_offset = scratch_animation_offset_y
            elif choice == "bite":
                meowth.attack_power = 20
                meowth.attack_name = "Bite"
                meowth.attack_sound = bite_attack_sound
                meowth.animation_imgs = bite_imgs
                meowth.animation_x_offset = bite_animation_offset_x
                meowth.animation_y_offset = bite_animation_offset_y
            elif choice == "bomb":
                meowth.attack_power = 50
                meowth.attack_name = "Bomb"
                meowth.attack_sound = bomb_attack_sound
                meowth.animation_imgs = bomb_imgs
                meowth.animation_x_offset = bomb_animation_offset_x
                meowth.animation_y_offset = bomb_animation_offset_y
            


            # meowth.attack(pikachu)
            # pikachu.attacked_time = pygame.time.get_ticks()
            # animation_playing = True
            # player_turn = not player_turn
            if not player_turn and not animation_playing and not meowth.defeated and current_time - last_pikachu_attack_time >= timedelay:
                # Meowth's attack code here
                meowth.attack(pikachu)
                pikachu.attacked_time = pygame.time.get_ticks()
                animation_playing = True
                player_turn = not player_turn

        current_time = pygame.time.get_ticks()
        if (pikachu.attack_name == "Thunderbolt"):
            meowth.visible = not meowth.defeated and not (current_time - meowth.attacked_time < 3000 and current_time % 200 < 100)
        elif (pikachu.attack_name == "Electricball"):
            meowth.visible = not meowth.defeated and not (current_time - meowth.attacked_time < 2000 and current_time % 200 < 100)
        elif (pikachu.attack_name == "Irontail"):
            meowth.visible = not meowth.defeated and not (current_time - meowth.attacked_time < 1000 and current_time % 200 < 100)

        pikachu.visible = not pikachu.defeated and not (current_time - pikachu.attacked_time < 1000 and current_time % 200 < 100)

        screen.blit(bg_img, (0, 0))

        if pikachu.visible:
            if not pikachu.winner_banner_displayed:
                screen.blit(pikachu.image, (desired_x_pika, desired_y_pika))
        elif pikachu.defeated:  # Add this condition to display meowthko_img when Meowth is defeated
            screen.blit(pikachuko_img, (desired_x_pikako, desired_y_pikako))
        if meowth.visible:
            screen.blit(meowth.image, (desired_x_meo, desired_y_meo))
        elif meowth.defeated:  # Add this condition to display meowthko_img when Meowth is defeated
            screen.blit(meowthko_img, (desired_x_meo, desired_y_meo))

        if animation_playing:
            if player_turn:
                animation_playing = not meowth.play_animation(screen, desired_x_pika, desired_y_pika, 1000)
            else:
                if (pikachu.attack_name == "Thunderbolt"):
                    animation_playing = not pikachu.play_animation(screen,desired_x_meo, desired_y_meo , 3000)
                elif (pikachu.attack_name == "Electricball"):
                    animation_playing = not pikachu.play_animation(screen,desired_x_meo, desired_y_meo , 2000)
                elif (pikachu.attack_name == "Irontail"):
                    animation_playing = not pikachu.play_animation(screen,desired_x_meo, desired_y_meo , 1000)
        # Get the screen width.
        screen_width = screen.get_rect().width

        # Get the width of the databox image.
        pikachu_databox_width = pygame.image.load('databox_normal.png').get_rect().width

        # Calculate the positions.
        pikachu_databox_x = screen_width - pikachu_databox_width
        meowth_databox_x = 0

        # Draw the data boxes at the correct positions.
        draw_databox(pikachu,pikachu_databox_x - 60 , 350)
        draw_databox(meowth, meowth_databox_x, 100)
        draw_command_box()
        # draw_health_bars()
        check_winner()

        pygame.display.update()
        clock.tick(FPS)

game_loop()

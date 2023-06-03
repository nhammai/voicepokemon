import pygame
from pygame.locals import *
import sys
import random
import os
import time

from understandjson import load_json_file
# from girlnlp import speech2command_knowmore , speech2command_ready, speech2command_playagain
from playsound import playsound
import moviepy.editor

pygame.init()


# Game window size
width = 800
height = 600

# Create the game window
screen = pygame.display.set_mode((width, height))

# Set the window title
pygame.display.set_caption("Pokemon Battle: Pikachu and The Multiverse")

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
battle_music.set_volume(0.4)  # Add this line to adjust the volume

ko_sound = pygame.mixer.Sound("./sounds/KObig.wav")
ko_sound.set_volume(1.0)  # Adjust the volume; 1.0 is the maximum volume


victory_full_sound = pygame.mixer.Sound("./sounds/victorfull.wav")
victory_full_sound.set_volume(0.9)

pikachu_sound = pygame.mixer.Sound("./sounds/pikapika_big.wav")

listen_sound_path = pygame.mixer.Sound("./sounds/listening.mp3")

def play_listen_sound():
    pygame.mixer.Sound.play(listen_sound_path)
# play pikachu sound
def play_pikachu_sound():
    pygame.mixer.Sound.play(pikachu_sound)

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
    pikachu = Pokemon("Pikachu", pikachu_img, 100, 20, "Thunderbolt", thunder_attack_sound, thunder_imgs, thunder_animation_offset_x, thunder_animation_offset_y)
    meowth = Pokemon("Meowth", meowth_img, 100, 15, "Scratch", scratch_attack_sound, scratch_imgs, scratch_animation_offset_x, scratch_animation_offset_y)
    player_turn = True
    animation_playing = False
    last_pikachu_attack = 0
    battle_music.play(-1)



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
        self.defeated = False  # Add this line
        self.ko_sound_played = False  # Add this line
        self.ko_displayed = False  # Add this line
        self.winner_banner_displayed = False  # Add this line
        self.sound_played = False  # Add this line
        


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
# battle_music.play(-1)

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

            # draw_button(screen, "Play Again", 350, 450, 100, 50, (0, 200, 0), (0, 255, 0), reset_game)

           

            

        PLAY_AGAIN_EVENT = pygame.USEREVENT + 1


        if pikachu.winner_banner_displayed or meowth.winner_banner_displayed:
            if not pikachu.sound_played and not meowth.sound_played:
                k = 1500
                if meowth.winner_banner_displayed:
                    k = 1000
                
                victory_full_sound.play()
                pikachu.sound_played = True
                meowth.sound_played = True
                battle_music.stop()  # Stop the background sound
                pygame.time.set_timer(PLAY_AGAIN_EVENT, k)  # 1500 milliseconds = 1.5 seconds


        for event in pygame.event.get():
            if event.type == PLAY_AGAIN_EVENT:
                play_again = playagain_scene(pikachu.hp > meowth.hp)
                if play_again == "yes":
                    reset_game()
                pygame.time.set_timer(PLAY_AGAIN_EVENT, 0)  # clear the timer

                


# Guide

def play_video(screen, path):
    screen_width, screen_height = screen.get_size() # Get screen dimensions
    clip = moviepy.editor.VideoFileClip(path)
    clip = clip.resize(height=screen_height, width=screen_width) # Fit video to screen size
    clip.preview()
    pygame.display.set_mode((screen_width, screen_height)) # Recreate the pygame window

# from pyvidplayer import Video

# vid = Video("videos/guide.mp4")
# vid.set_size((800, 600))

# def guide():
#     while True:
#         vid.draw(screen, (0, 0))
#         pygame.display.update()
#         for event in pygame.event.get():
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 vid.close()
#                 # battle_scene()




# Play the video
# play_video('videos/guide.mp4')










# Transition

def transition_fade(screen, type='in', speed=1):
    screen_width, screen_height = screen.get_size()  # Get screen dimensions
    fade_surface = pygame.Surface((screen_width, screen_height))  # Create a surface for fading
    fade_surface.fill((0,0,0))  # Fill the surface with black color
    alpha = 0 if type == 'in' else 255

    while True:
        if type == 'in' and alpha >= 255:
            break
        elif type == 'out' and alpha <= 0:
            break

        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.update()
        pygame.time.delay(speed)

        alpha = alpha + speed if type == 'in' else alpha - speed





# Intro game

    



# Initialize pygame mixer with custom frequency and buffer size
pygame.mixer.init(frequency=44100, buffer=512)

# Assuming a 800x600 screen
screen = pygame.display.set_mode((800, 600))

import textwrap  # Module to handle text wrapping


def intro_scene():
    # Size of the screen
    screen_width, screen_height = screen.get_size()

    # Margin around the text
    margin = 50

    # Load Images and Sounds
    bg_image = pygame.image.load('intro_image/backgroundblank.png')
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))  # Resize bg_image to fit the screen

    katsumi_image = pygame.image.load('intro_image/katsumi.png')
    katsumi_image = pygame.transform.scale(katsumi_image, (200, 412))
    
        # Load Images and Sounds
    scene0 = pygame.image.load('guide/scene_0.png')
    scene0 = pygame.transform.scale(bg_image, (screen_width, screen_height)) 
    # Load Psyduck image
    psyduck_image = pygame.image.load('intro_image/psyduck.png')
    psyduck_image = pygame.transform.scale(psyduck_image, (142, 200))  # Resize psyduck_image to fit desired dimensions

    # Audio
    intro_sound = pygame.mixer.Sound('sounds/introbackground.wav')
    katsumi_voice_intro = pygame.mixer.Sound('sounds/girl_voice/1_intro.wav')
    katsumi_voice_duoctroi = pygame.mixer.Sound('sounds/girl_voice/2_duocroingangon.wav')
    katsumi_voice_radongiandungko = pygame.mixer.Sound('sounds/girl_voice/3_ratdongiandungko.wav')
    katsumi_voice_vaogame = pygame.mixer.Sound('sounds/girl_voice/6_totchungtasebatdau.wav')
    katsumi_voice_totphaivaychu = pygame.mixer.Sound('sounds/girl_voice/4_totphaivaychu.wav')
    katsumi_voice_chuasansangthikeanh = pygame.mixer.Sound('sounds/girl_voice/5_chuasansangthikeanh.wav')


    # katsumi_voice_guide = pygame.mixer.Sound('sounds/girl_voice/2_duocroingangon.wav')
    katsumi_voice_guide_long = pygame.mixer.Sound('sounds/girl_voice/mix02.wav')




    # Text
    intro_text = "Chào mừng Shatoshi đã trở lại với thế giới Pokemon. Em là Kasumi, hướng dẫn viên xinh đẹp. Hôm nay, chúng ta sẽ bắt đầu một hành trình đầy bất ngờ và thú vị. Anh có cần em giới thiệu một tí về cách thức chơi không nhỉ?"

    duocroi_text = "Được rồi, em sẽ giới thiệu ngắn gọn nhé!"

    vaogame_text = "Tốt. Chúng ta sẽ bắt đầu với trận đấu đầu tiên với một nhân vật hết sức quen thuộc và khốn nạn hồi nhỏ. Chúc anh may mắn nhé!"
    ratdongiandungko_text  = "Rất đơn giản đúng không. Anh chỉ cần hô to pikachu và đọc to chiêu thức lên là xong. Vậy anh đã sẵn sàng chưa nào?"


    totphaivaychu_text = "Tốt. Chồng em phải vậy chứ. Chúng ta sẽ bắt đầu với trận đấu đầu tiên với một nhân vật hết sức khốn nạn hồi nhỏ. Gút lấc!"
    chuasansangthikeanh_text = "Chưa sẵn sàng thì kệ anh. Cứ chơi đi rồi sẽ biết. Nào chúng ta bắt đầu trận đấu giữa pikachu và một nhân vật hết sức quen thuộc và khốn nạn. Lét gâu !!"

    




    # time delay
    delay_per_char_intro = 11000 / len(intro_text) # 14 s
    delay_per_char_duocroi = 2000 / len(duocroi_text)
    delay_per_char_vaogame = 6000 / len(vaogame_text)
    delay_per_char_ratdongiandungko = 6000 / len(ratdongiandungko_text)
    delay_per_char_totphaivaychu = 6000 / len(totphaivaychu_text)
    delay_per_char_chuasansangthikeanh = 8000 / len(totphaivaychu_text)



    # Set volume
    intro_sound.set_volume(0.3)
    # katsumi_voice_.set_volume(1.0)

    # Play sounds using separate channels
    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)

    channel1.play(intro_sound, -1)
    pygame.time.wait(1000)


    import cv2
    import numpy as np

    def play_video(filename):
        # Open the video file
        cap = cv2.VideoCapture(filename)

        # Get the frame rate of the video
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Calculate new fps to play the video in 44 seconds
        video_length_in_seconds = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
        new_fps = cap.get(cv2.CAP_PROP_FRAME_COUNT) / 37.5  # new fps to make the video play in 44 seconds

        # Get screen size
        screen_res = '1920x1080'
        screen_width, screen_height = map(int, screen_res.split('x'))

        # Set the window to fullscreen
        cv2.namedWindow('Video', cv2.WINDOW_NORMAL)
        cv2.setWindowProperty('Video', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

        while(cap.isOpened()):
            # Read a frame from the video file
            ret, frame = cap.read()

            # If the frame was read successfully
            if ret:
                # Resize the frame
                aspect_ratio = frame.shape[1] / float(frame.shape[0])
                if(aspect_ratio > screen_width / screen_height):
                    # Based on width
                    new_width = screen_width
                    new_height = np.round(new_width / aspect_ratio).astype(int)
                else:
                    # Based on height
                    new_height = screen_height
                    new_width = np.round(new_height * aspect_ratio).astype(int)
                frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

                # Display the frame in a window
                cv2.imshow('Video', frame)

                # Wait for a delay equivalent to the new frame rate of the video
                if cv2.waitKey(int(1000 / new_fps)) & 0xFF == ord('q'):
                    break
            else:
                break

        # Close the video file
        cap.release()

        # Close all OpenCV windows
        cv2.destroyAllWindows()


    # channel2.play(katsumi_voice_1)

    def display_background():
        screen.fill((0, 0, 0))
        screen.blit(bg_image, (0, 0))  # draw the background image

    def display_full_chacter_background():
        display_background()
        # Position katsumi_image at the center bottom of the screen
        x = screen_width / 2 - katsumi_image.get_width() / 2
        y = screen_height - katsumi_image.get_height()
        screen.blit(katsumi_image, (x, y))  # draw Katsumi on the screen
        # Position psyduck_image to the right of katsumi_image
        x_psyduck = x - katsumi_image.get_width() + 150  # 150 is the space between Katsumi and Psyduck
        y_psyduck = screen_height - psyduck_image.get_height()  # This aligns the bottom of the images
        screen.blit(psyduck_image, (x_psyduck, y_psyduck))  # Draw Psyduck on the screen





  
    
    waiting = True
    def text_generate(sound, text, text_delay):
        font = pygame.font.Font('Arial_Unicode.ttf', 20)  # Use a smaller font size that supports Vietnamese

        channel2.play(sound)

        # Time when the typing effect starts
        start_time = pygame.time.get_ticks()

        # Index of the character to display
        char_index = 0

        while waiting:
            current_time = pygame.time.get_ticks()
            if current_time - start_time >= text_delay:  # Time for the next character
                char_index += 1
                start_time = current_time

            # Concatenate the characters to display
            text_to_render = text[:char_index]

            # Split the text into lines that don't exceed the screen width minus margins
            wrapped_text = textwrap.wrap(text_to_render, width=(screen_width - 2 * margin) // 10)

            display_full_chacter_background()
            
            # Display each line
            y = margin  # Starting height for the text
            for line in wrapped_text:
                text_surface = font.render(line, True, (34, 34, 34)) # Change the color to yellow
                screen.blit(text_surface, (margin, y))
                y += font.get_height() + 5  # Increase y by the height of the font for the next line
            
            

            pygame.display.update()

            # Stop when all characters have been displayed
            if char_index >= len(text):
                break
    

    
    answer = "yes"

    def askquestion(sound, text, delay_per_char):
        text_generate(sound, text, delay_per_char )
        play_listen_sound()


    # text_generate(katsumi_voice_intro, intro_text, delay_per_char_intro )
    
    askquestion(katsumi_voice_intro, intro_text, delay_per_char_intro)
    # answer = speech2command_knowmore()
    answer = "no"    
    if answer == "yes":
        text_generate(katsumi_voice_duoctroi, duocroi_text, delay_per_char_duocroi)
        transition_fade(screen, 'in', 2)
        transition_fade(screen, 'out', 2)
        play_video(screen, 'videos/guide.mp4')
        channel2.play(katsumi_voice_guide_long)


        text_generate(katsumi_voice_radongiandungko, ratdongiandungko_text, delay_per_char_ratdongiandungko)
        # answer = speech2command_ready()
        answer = "yes"    

        if answer == "yes":
            #tot phai vay chu
            text_generate(katsumi_voice_totphaivaychu, totphaivaychu_text, delay_per_char_totphaivaychu)
            waiting = False

        else:
            #ke anh bat dau
            text_generate(katsumi_voice_chuasansangthikeanh, chuasansangthikeanh_text, delay_per_char_chuasansangthikeanh)
            waiting = False


    else:
        text_generate(katsumi_voice_vaogame, vaogame_text, delay_per_char_vaogame)
        waiting = False


    # After all characters have been displayed, wait until the Enter key is pressed to exit
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # Key down event (key is pressed)
                if event.key == pygame.K_RETURN:  # The key is the Enter key
                    waiting = False

        pygame.time.wait(50)  # Delay to prevent the CPU from running at full speed in the waiting loop


    channel1.stop()
    channel2.stop()



def playagain_scene(win):
    playagain = "yes"
    # Size of the screen
    screen_width, screen_height = screen.get_size()

    # Margin around the text
    margin = 50

    # Load Images and Sounds
    bg_image = pygame.image.load('intro_image/backgroundblank.png')
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))  # Resize bg_image to fit the screen

    katsumi_image = pygame.image.load('intro_image/katsumi.png')
    katsumi_image = pygame.transform.scale(katsumi_image, (200, 412))
    
        # Load Images and Sounds
    scene0 = pygame.image.load('guide/scene_0.png')
    scene0 = pygame.transform.scale(bg_image, (screen_width, screen_height)) 
    # Load Psyduck image
    psyduck_image = pygame.image.load('intro_image/psyduck.png')
    psyduck_image = pygame.transform.scale(psyduck_image, (142, 200))  # Resize psyduck_image to fit desired dimensions

    # Audio
    intro_sound = pygame.mixer.Sound('sounds/girl_voice/introbackground.wav')
    katsumi_voice_chucmungchoilaiko = pygame.mixer.Sound('sounds/girl_voice/7_chucmungchoilaiko.wav') # chien thang choi lai ko
    katsumi_voice_choilaigameko = pygame.mixer.Sound('sounds/girl_voice/8_pikachumatkhanangchiendau.wav') # pikachu mat kha nang chien dau
    katsumi_voice_batdaulaicolen = pygame.mixer.Sound('sounds/girl_voice/10_vaychungtabatdaulainaocolen.wav')
    katsumi_voice_okbatdaulai = pygame.mixer.Sound('sounds/girl_voice/9_okchungtabatdaulainao.wav')
    katsumi_voice_hengaplai = pygame.mixer.Sound('sounds/girl_voice/11_tambiet.wav')




    # Text
    chucmungchoilaiko_text = "Chúc mừng Shatoshi và Pikachu đã chiến thắng. Anh có muốn chơi lại không nhỉ?"
    choilaigameko_text = "Pikachu đã mất khả năng chiến đấu. Anh có muốn chơi lại game không nhỉ?"
    okbatdaulai_text = "Ok. Chúng ta bắt đầu lại trận đấu nào!!"
    batdaulaicolen_text  = "Vậy chúng ta bắt đầu lại trận đấu nào. Cố lên, anh và Pikachu sẽ làm được!!"
    hengaplai_text  = "Vậy tạm biệt anh nha. Em nghe giang hồ đồn các phiên bản tiếp theo sẽ vui hơn nhiều đấy! Nếu được, anh hãy để lại feedback cho người tạo game Mai Khánh Nhâm để anh ý biết ngõ để phát triển hoặc từ bỏ giấc mộng làm game nhé. Bái bai anh Shatoshi. Cảm ơn anh đã chơi game cùng em ^^"


    # time delay
    delay_per_char_chucmungchoilaiko = 4000 / len(chucmungchoilaiko_text) 
    delay_per_char_choilaigameko = 3000 / len(choilaigameko_text) 
    delay_per_char_okbatdaulai = 2000 / len(okbatdaulai_text)
    delay_per_char_batdaulaicolen = 4000 / len(batdaulaicolen_text)
    delay_per_char_hengaplai = 15000 / len(hengaplai_text)



    # Set volume
    intro_sound.set_volume(0.3)
    # katsumi_voice_.set_volume(1.0)

    # Play sounds using separate channels
    channel1 = pygame.mixer.Channel(0)
    channel2 = pygame.mixer.Channel(1)

    channel1.play(intro_sound, -1)
    pygame.time.wait(1000)


    # channel2.play(katsumi_voice_1)

    def display_background():
        screen.fill((0, 0, 0))
        screen.blit(bg_image, (0, 0))  # draw the background image

    def display_full_chacter_background():
        display_background()
        # Position katsumi_image at the center bottom of the screen
        x = screen_width / 2 - katsumi_image.get_width() / 2
        y = screen_height - katsumi_image.get_height()
        screen.blit(katsumi_image, (x, y))  # draw Katsumi on the screen
        # Position psyduck_image to the right of katsumi_image
        x_psyduck = x - katsumi_image.get_width() + 150  # 150 is the space between Katsumi and Psyduck
        y_psyduck = screen_height - psyduck_image.get_height()  # This aligns the bottom of the images
        screen.blit(psyduck_image, (x_psyduck, y_psyduck))  # Draw Psyduck on the screen
  
    
    waiting = True
    def text_generate(sound, text, text_delay):
        font = pygame.font.Font('Arial_Unicode.ttf', 20)  # Use a smaller font size that supports Vietnamese

        channel2.play(sound)

        # Time when the typing effect starts
        start_time = pygame.time.get_ticks()

        # Index of the character to display
        char_index = 0

        waiting = True
        while waiting:
            current_time = pygame.time.get_ticks()
            if current_time - start_time >= text_delay:  # Time for the next character
                char_index += 1
                start_time = current_time

            # Concatenate the characters to display
            text_to_render = text[:char_index]

            # Split the text into lines that don't exceed the screen width minus margins
            wrapped_text = textwrap.wrap(text_to_render, width=(screen_width - 2 * margin) // 10)

            display_full_chacter_background()
            
            # Display each line
            y = margin  # Starting height for the text
            for line in wrapped_text:
                text_surface = font.render(line, True, (34, 34, 34)) # Change the color to yellow
                screen.blit(text_surface, (margin, y))
                y += font.get_height() + 5  # Increase y by the height of the font for the next line
            
            

            pygame.display.update()


            # Stop when all characters have been displayed
            if char_index >= len(text):
                break
    


    def askquestion(sound, text, delay_per_char):
        text_generate(sound, text, delay_per_char )
        play_listen_sound()

    if win == True:
        askquestion(katsumi_voice_chucmungchoilaiko, chucmungchoilaiko_text, delay_per_char_chucmungchoilaiko)
        play_listen_sound()
        # again = speech2command_playagain()
        again = "no"
        if again == "yes":
            # ok bat dau lai
            text_generate(katsumi_voice_okbatdaulai, okbatdaulai_text, delay_per_char_okbatdaulai )

            #choi lai
            # reset_game()
            
        else:
            #ending scene
            text_generate(katsumi_voice_hengaplai, hengaplai_text, delay_per_char_hengaplai )
            playagain = "no"


    else:
        askquestion(katsumi_voice_choilaigameko, choilaigameko_text, delay_per_char_choilaigameko)
        play_listen_sound()
        # again = speech2command_playagain()
        again = "no"

        if again == "yes":
            # bat dau lai co len
            text_generate(katsumi_voice_batdaulaicolen, batdaulaicolen_text, delay_per_char_batdaulaicolen )
            # reset_game()

            # choi lai
        else:
            #ending scene
            text_generate(katsumi_voice_hengaplai, hengaplai_text, delay_per_char_hengaplai )
            playagain = "no"


    waiting = False            



    # After all characters have been displayed, wait until the Enter key is pressed to exit
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # Key down event (key is pressed)
                if event.key == pygame.K_RETURN:  # The key is the Enter key
                    waiting = False

        pygame.time.wait(50)  # Delay to prevent the CPU from running at full speed in the waiting loop


    channel1.stop()
    channel2.stop()
    return playagain





# Main game loop
last_pikachu_attack_time = 0
def battle_scene():
    global pikachu, meowth, player_turn, animation_playing, last_pikachu_attack, last_pikachu_attack_time

    pikachu = Pokemon("Pikachu", pikachu_img, 100, 20, "Thunderbolt", thunder_attack_sound, thunder_imgs, thunder_animation_offset_x, thunder_animation_offset_y)
    meowth = Pokemon("Meowth", meowth_img, 100, 15, "Scratch", scratch_attack_sound, scratch_imgs, scratch_animation_offset_x, scratch_animation_offset_y)
    player_turn = True
    animation_playing = False
    last_pikachu_attack = 0
    battle_music.play(-1)
    # meowth_attack_delay = random.randint(3000, 6000)  # 3 or 6 seconds in milliseconds
    timedelay = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_a:  # Reset the game when 'A' is pressed
                    pikachu = Pokemon("Pikachu", pikachu_img, 100, 20, "Thunderbolt", thunder_attack_sound, thunder_imgs, thunder_animation_offset_x, thunder_animation_offset_y)
                    meowth = Pokemon("Meowth", meowth_img, 100, 15, "Scratch", scratch_attack_sound, scratch_imgs, scratch_animation_offset_x, scratch_animation_offset_y)
                    player_turn = True
                    animation_playing = False
                    last_pikachu_attack = 0
                    battle_music.play(-1)

                if event.key == K_SPACE and not animation_playing and player_turn:
                    # cm = read_command("command.txt") ## read the amount to modify power
                    command = load_json_file('command.json')

                    print(command)

                    if (command["command"] == "thunder"):
                        timedelay = random.randint(5000, 7000)
                        pikachu.attack_name = "Thunderbolt"
                        pikachu.attack_power = command["amount"]*40/10000
                        pikachu.attack_sound = thunder_attack_sound
                        print(pikachu.attack_power)
                        if(pikachu.attack_power <40): # change the animation depend on the attack power
                            pikachu.animation_imgs = thunder_weak_imgs
                        if(pikachu.attack_power>400):
                            pikachu.animation_imgs = thunder_super
                            superthundersound.play()
                            superthundersound.play()
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
                meowth.attack_power = 10
                meowth.attack_name = "Scratch"
                meowth.attack_sound = scratch_attack_sound
                meowth.animation_imgs = scratch_imgs
                meowth.animation_x_offset = scratch_animation_offset_x
                meowth.animation_y_offset = scratch_animation_offset_y
            elif choice == "bite":
                meowth.attack_power = 15
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

        draw_health_bars()
        check_winner()


        pygame.display.update()
        clock.tick(FPS)







def main():
    intro_scene()  # Play the intro scene first
    battle_scene()  # Then transition to the main game
    

if __name__ == "__main__":
    main()

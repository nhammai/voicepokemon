import pygame
import threading
import speech_recognition as sr
import time

def listen_for_keyword(keyword_detected_event):
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    while True:
        with microphone as source:
            print("Listening for keyword...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        try:
            transcription = recognizer.recognize_google(audio)
            print("Heard:", transcription)
            if "pikachu" in transcription.lower():
                print("Keyword detected!")
                keyword_detected_event.set()
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

pikachu = pygame.image.load("pikachu_img.png")
pikachu.image = pikachu
pikachu.rect = pikachu.get_rect()
pikachu.rect.topleft = (200, 200)

pygame.mixer.init()
pika_sound = pygame.mixer.Sound("sounds/pikapika.wav")

keyword_detected_event = threading.Event()
wake_word_thread = threading.Thread(target=listen_for_keyword, args=(keyword_detected_event,))
wake_word_thread.start()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    screen.blit(pikachu.image, pikachu.rect)

    if keyword_detected_event.is_set():
        pika_sound.play()
        keyword_detected_event.clear()

    pygame.display.flip()
    clock.tick(60)

wake_word_thread.join()
pygame.quit()

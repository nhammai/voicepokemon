import os
import pygame

# Path to the folder containing the PNG images
image_folder = r"C:/Users/daso/Desktop/material/image_process"

# Initialize Pygame
pygame.init()

# Set up the display window
screen = pygame.display.set_mode((800, 600))

# Get a list of PNG image files in the folder
image_files = [f for f in os.listdir(image_folder) if f.endswith(".png")]

# Load the images into a list
images = [pygame.image.load(os.path.join(image_folder, f)) for f in image_files]

# Set the initial image index and frame rate
current_image = 0
frame_rate = 10  # Number of frames per second

clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Display the current image on the screen
    screen.blit(images[current_image], (0, 0))

    # Update the current image index
    current_image = (current_image + 1) % len(images)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(frame_rate)

# Quit the game
pygame.quit()

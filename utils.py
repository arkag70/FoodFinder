import pygame
import threading
from settings import MUSICFILE, VOLUME, WIDTH, HEIGHT, DELAY

def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load(MUSICFILE)  # Replace with your music file
    pygame.mixer.music.set_volume(VOLUME)  # Adjust the volume as needed
    pygame.mixer.music.play(-1)  # -1 indicates infinite loop

def start_music():
    music_thread = threading.Thread(target=play_music)
    music_thread.daemon = True  # This will allow the program to exit even if the thread is running
    music_thread.start()

def display_init():
    # Create a Pygame window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 24)
    # Set the window title
    pygame.display.set_caption("Pygame Canvas")

    return screen, font

# Function to display text on the screen
def display_text(text, x, y, color, font, screen):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def refresh():
    pygame.time.delay(DELAY)
    # Update the display
    pygame.display.update()
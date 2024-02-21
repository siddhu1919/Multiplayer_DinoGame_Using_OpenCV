import socket
import subprocess
import pyautogui
import pygame
import sys


#importing the hand_gesture file


# Initialize pygame
pygame.init()
width, height = 400, 300
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client Waiting for Server")

# Function to show status screen
def show_status_screen(message):
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 24)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(width/2, height/2))
    screen.blit(text, text_rect)
    pygame.display.flip()

# Function to launch Dino Game
def launch_dino_game():
    from main2 import gesture_control
    print("Dino Game Launched")
    gesture_control()
    dino_game_url = "https://offline-dino-game.firebaseapp.com/"
    # Depending on your system configuration, you might need to adjust the way to open a URL in Chrome
    subprocess.Popen(['start', 'chrome', '--new-window', dino_game_url], shell=True)
    pyautogui.press('f11')  # Press F11 to enter fullscreen mode
    
# Setup socket
host = 'localhost'  # Replace with server's IP address
port = 12345
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Display initial waiting screen
show_status_screen("Connecting to server...")

try:
    client_socket.connect((host, port))
    # Display connected status
    show_status_screen(f"Connected to {host}")
    pygame.time.wait(2000)  # Wait for 2 seconds to show the message

    # Launch Dino Game upon successful connection
    launch_dino_game()

except Exception as e:
    show_status_screen(f"Failed to connect: {e}")
    pygame.time.wait(2000)  # Wait for 2 seconds to show the message
    pygame.quit()
    sys.exit()

client_socket.close()
pygame.quit()

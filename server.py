import pygame
import sys
import socket
import threading
import pyautogui
import subprocess


# Initialize Pygame
pygame.init()

# Screen Setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Server Control Panel")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Button Dimensions
button_width, button_height = 200, 60
start_button = pygame.Rect(
    screen_width / 2 - button_width - 10,
    screen_height / 2 - button_height / 2,
    button_width,
    button_height,
)
stop_button = pygame.Rect(
    screen_width / 2 + 10,
    screen_height / 2 - button_height / 2,
    button_width,
    button_height,
)
reset_button = pygame.Rect(
    screen_width / 2 - button_width / 2,
    screen_height / 2 + button_height + 10,
    button_width,
    button_height,
)

# Server Setup
server_socket = None
listening_thread = None


# Start Server Function
def start_server():
    global server_socket, message
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))  # Change port as needed
    server_socket.listen()
    print("Server is now listening...")
    client_socket, address = server_socket.accept()
    message = f"Connected to {address}"
    launch_dino_game()


# Dino Game
def launch_dino_game():
    try:
        print("Dino Game Launched")

        # importing the hand_gesture file
        from main2 import gesture_control

        gesture_control()

        dino_game_url = "https://offline-dino-game.firebaseapp.com/"
        subprocess.Popen(["start", "chrome", "--new-window", dino_game_url], shell=True)
        pyautogui.press("f11")  # Press F11 to enter fullscreen mode
    except Exception as e:
        print(f"Error launching Dino game: {e}")


# Stop Server Function
def stop_server():
    global server_socket
    if server_socket:
        server_socket.close()


# Reset Server Function
def reset_server():
    global listening_thread
    stop_server()
    if listening_thread:
        listening_thread.join()
    listening_thread = None


# Thread Starter
def start_listening_thread():
    global listening_thread
    listening_thread = threading.Thread(target=start_server, daemon=True)
    listening_thread.start()


# Text Setup
def draw_text(text, font, color, surface, rect):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=rect.center)
    surface.blit(textobj, textrect)


def draw_screen(message):
    screen.fill(black)

    # Buttons
    pygame.draw.rect(screen, green, start_button)
    draw_text("Start Search", font, black, screen, start_button)

    pygame.draw.rect(screen, red, stop_button)
    draw_text("Stop Search", font, black, screen, stop_button)

    pygame.draw.rect(screen, blue, reset_button)
    draw_text("Reset", font, white, screen, reset_button)

    # Message Display Area
    message_area = pygame.Rect(100, 50, screen_width - 200, 40)
    pygame.draw.rect(screen, white, message_area)
    draw_text(message, font, black, screen, message_area)

    # Update the display
    pygame.display.flip()


message = "Press 'Start Search' to begin."

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            reset_server()  # Ensure the server is properly shut down
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_button.collidepoint(event.pos):
                message = "Waiting for client..."
                start_listening_thread()
            elif stop_button.collidepoint(event.pos):
                message = "Stopped searching."
                stop_server()
            elif reset_button.collidepoint(event.pos):
                message = "Connection reset."
                reset_server()

    draw_screen(message)

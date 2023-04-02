import pygame
import sys
import serial

# Initialize Arduino connection
arduino = serial.Serial('COM3', 115200)  # Replace 'COM3' with the appropriate port for your system

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Define game objects
paddle_width, paddle_height = 25, 100
ball_radius = 15

# Initialize paddles and ball
player_paddle = pygame.Rect(0, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(WIDTH // 2 - ball_radius // 2, HEIGHT // 2 - ball_radius // 2, ball_radius, ball_radius)
ball_speed = [3, 3]

font = pygame.font.Font(None, 36)

game_over = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Read accelerometer data from Arduino
        try:
            y_accel = int(arduino.readline().decode().strip())
        except ValueError:
            continue

        # Calculate paddle speed
        paddle_speed = y_accel * 0.01  # Adjust the scaling factor as needed

        # Update paddle position based on accelerometer data
        player_paddle.y += paddle_speed
        player_paddle.y = min(max(0, player_paddle.y), HEIGHT - paddle_height)

        # Update ball position
        ball.x += ball_speed[0]
        ball.y += ball_speed[1]

        # Check for ball collisions with edges
        if ball.y <= 0 or ball.y + ball_radius >= HEIGHT:
            ball_speed[1] = -ball_speed[1]
        if ball.x + ball_radius >= WIDTH:
            ball_speed[0] = -ball_speed[0]

        # Check for ball collision with paddle
        if ball.colliderect(player_paddle):
            ball_speed[0] = -ball_speed[0]

        # Check for ball out of bounds (game over)
        if ball.x <= 0:
            game_over = True

        # Render the game objects
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, player_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    else:
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.fill(BLACK)
        screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(10)
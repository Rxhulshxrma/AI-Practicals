import pygame 
import random 
# Initialize Pygame 
pygame.init() 
# Define constants 
WIDTH, HEIGHT = 800, 600 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 
BALL_SPEED = 5 
PADDLE_SPEED = 10 
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100 
BALL_SIZE = 20 
FONT_SIZE = 36 
# Set up the display 
screen = pygame.display.set_mode((WIDTH, HEIGHT)) 
pygame.display.set_caption("Pong with AI") 
# Set up the font 
font = pygame.font.Font(None, FONT_SIZE) 
 
# Button colors 
BUTTON_COLOR = (0, 128, 255) 
HOVER_COLOR = (0, 180, 255) 
BUTTON_BORDER_COLOR = (0, 0, 0)  # Border color for buttons 
BUTTON_RADIUS = 10  # Radius for rounded corners 
 
# Define the Ball class 
class Ball: 
    def __init__(self): 
        self.x = WIDTH // 2 
        self.y = HEIGHT // 2 
        self.dx = BALL_SPEED * random.choice((1, -1)) 
        self.dy = BALL_SPEED * random.choice((1, -1)) 
        self.size = BALL_SIZE 
     
    def draw(self): 
        pygame.draw.ellipse(screen, WHITE, (self.x, self.y, self.size, self.size)) 
     
    def move(self): 
        self.x += self.dx 
        self.y += self.dy 
        if self.y <= 0 or self.y >= HEIGHT - self.size: 
            self.dy = -self.dy 
        if self.x <= 0 or self.x >= WIDTH - self.size: 
            self.dx = -self.dx 
 
# Define the Paddle class 
class Paddle: 
    def __init__(self, x): 
        self.x = x 
        self.y = HEIGHT // 2 - PADDLE_HEIGHT // 2 
        self.width = PADDLE_WIDTH 
        self.height = PADDLE_HEIGHT 
        self.speed = PADDLE_SPEED 
     
    def draw(self): 
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height)) 
     
    def move(self, up=True): 
        if up: 
            self.y -= self.speed 
        else: 
            self.y += self.speed 
        self.y = max(0, min(HEIGHT - self.height, self.y)) 
 
ball = Ball() 
player_paddle = Paddle(WIDTH - PADDLE_WIDTH - 10) 
ai_paddle = Paddle(10) 
player_score = 0 
ai_score = 0 
score_limit = 5 
running = True 
game_over = False 
in_menu = True 
how_to_play = False  # Track the "How to Play" screen state 
clock = pygame.time.Clock() 
 
def draw_button(text, x, y, width, height, hover=False): 
    color = HOVER_COLOR if hover else BUTTON_COLOR 
    # Draw button background with rounded corners 
    pygame.draw.rect(screen, color, (x, y, width, height), 
border_radius=BUTTON_RADIUS) 
    # Draw button border 
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x, y, width, height), 2, 
border_radius=BUTTON_RADIUS) 
    button_text = font.render(text, True, WHITE) 
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + 
(height - button_text.get_height()) // 2)) 
 
def show_menu(): 
    screen.fill(BLACK) 
    # Draw the game title at the top 
    title_text = font.render("Pong with AI", True, WHITE) 
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50)) 
    mouse_pos = pygame.mouse.get_pos() 
    start_hover = 300 <= mouse_pos[0] <= 500 and 200 <= mouse_pos[1] <= 260 
    how_to_play_hover = 300 <= mouse_pos[0] <= 500 and 300 <= 
mouse_pos[1] <= 360 
    quit_hover = 300 <= mouse_pos[0] <= 500 and 400 <= mouse_pos[1] <= 460 
    draw_button("Start Game", 300, 200, 200, 60, start_hover) 
    draw_button("How to Play", 300, 300, 200, 60, how_to_play_hover) 
    draw_button("Quit", 300, 400, 200, 60, quit_hover) 
    pygame.display.flip() 
 
def show_how_to_play(): 
    screen.fill(BLACK) 
    instructions = [ 
        "How to play.", 
        "Use the UP and DOWN arrow keys to move your paddle.", 
        "The AI paddle will move automatically.", 
        "Score by getting the ball past the AI paddle.", 
        "The first to reach 5 points wins the game!" 
    ] 
    y_offset = 150 
    for line in instructions: 
        text = font.render(line, True, WHITE) 
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y_offset)) 
        y_offset += 50 
    back_text = font.render("Press ESC to go back", True, WHITE) 
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 
200)) 
    pygame.display.flip() 
 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        if in_menu: 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if 300 <= event.pos[0] <= 500: 
                    if 200 <= event.pos[1] <= 260: 
                        in_menu = False  # Start game 
                    elif 300 <= event.pos[1] <= 360: 
                        how_to_play = True  # Show "How to Play" 
                        in_menu = False 
                    elif 400 <= event.pos[1] <= 460: 
                        running = False  # Quit 
        elif how_to_play: 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
                how_to_play = False 
                in_menu = True  # Return to menu 
        elif game_over: 
            # Display the final score when the game ends 
            screen.fill(BLACK) 
            game_over_text = font.render("Game Over!", True, WHITE) 
            final_score_text = font.render(f"Final Score - Player: {player_score}  AI: 
{ai_score}", True, WHITE) 
            instruction_text = font.render("Press ESC to return to the menu", True, 
WHITE) 
            # Center the texts on the screen 
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() 
// 2, HEIGHT // 3 - 50)) 
            screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() 
// 2, HEIGHT // 2 - 50)) 
            screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() 
// 2, HEIGHT // 2 + 10)) 
            pygame.display.flip() 
            # Check for events in the game-over state 
            while game_over: 
                for event in pygame.event.get(): 
                    if event.type == pygame.QUIT: 
                        running = False 
                        game_over = False 
                    if event.type == pygame.KEYDOWN and event.key == 
pygame.K_ESCAPE: 
                        in_menu = True 
                        game_over = False 
                        player_score = ai_score = 0  # Reset scores 
 
    if in_menu: 
        show_menu() 
    elif how_to_play: 
        show_how_to_play() 
    elif not game_over: 
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_UP]: 
            player_paddle.move(up=True) 
        if keys[pygame.K_DOWN]: 
            player_paddle.move(up=False) 
        # Randomized AI Movement 
        if random.random() < 0.5:  # 50% chance to move towards the ball 
            if ai_paddle.y + PADDLE_HEIGHT / 2 < ball.y + BALL_SIZE / 2: 
                ai_paddle.move(up=False) 
            elif ai_paddle.y + PADDLE_HEIGHT / 2 > ball.y + BALL_SIZE / 2: 
                ai_paddle.move(up=True) 
        ball.move() 
        if (ball.x <= ai_paddle.x + ai_paddle.width and 
            ai_paddle.y < ball.y + BALL_SIZE and 
            ai_paddle.y + ai_paddle.height > ball.y): 
            ball.dx = -ball.dx 
        if (ball.x + BALL_SIZE >= player_paddle.x and 
            player_paddle.y < ball.y + BALL_SIZE and 
            player_paddle.y + player_paddle.height > ball.y): 
            ball.dx = -ball.dx 
        if ball.x <= 0: 
            player_score += 1 
            ball = Ball() 
            if player_score >= score_limit: 
                game_over = True 
        if ball.x >= WIDTH - BALL_SIZE: 
            ai_score += 1 
            ball = Ball() 
            if ai_score >= score_limit: 
                game_over = True 
        screen.fill(BLACK) 
        ball.draw() 
player_paddle.draw() 
ai_paddle.draw() 
score_text = font.render(f"Player: {player_score}  AI: {ai_score}", True, 
WHITE) 
screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20)) 
pygame.display.flip() 
clock.tick(60) 
pygame.quit()  
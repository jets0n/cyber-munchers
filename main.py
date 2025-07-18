
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 900  # Increased height for top status area
GRID_SIZE = 5
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
PLAYER_SIZE = CELL_SIZE - 20
TOP_MARGIN = 100  # Space at the top for lives and status

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_RED = (255, 200, 200)

# Create window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Cyber Munchers")

# Word lists
pii_words = ["Full Name", "First Name", "Last Name", "Date of Birth", "Address", 
           "Home Address", "Mailing Address", "Phone Number", "Email Address", 
           "Social Security Number", "SSN", "Driver's License Number"]

non_pii_words = ["Apple", "Book", "Parrot", "Mountain", "Cloud", 
                "Code", "Pencil", "Puppy", "Dance", "Waterfall"]

# Game grid - randomly place PII and non-PII words
grid = [[""] * GRID_SIZE for _ in range(GRID_SIZE)]

# Track PII words for win condition
total_pii_words = 0
remaining_pii_words = 0

# Fill grid with approximately 30-40% PII words and the rest non-PII
def initialize_grid():
    global total_pii_words, remaining_pii_words
    total_cells = GRID_SIZE * GRID_SIZE
    pii_count = int(total_cells * random.uniform(0.3, 0.4))  # 30-40% PII words
    total_pii_words = pii_count
    remaining_pii_words = pii_count
    
    # Create a flat list of positions
    positions = [(row, col) for row in range(GRID_SIZE) for col in range(GRID_SIZE)]
    random.shuffle(positions)
    
    # Place PII words
    for i in range(pii_count):
        row, col = positions[i]
        grid[row][col] = random.choice(pii_words)
    
    # Place non-PII words
    for i in range(pii_count, total_cells):
        row, col = positions[i]
        grid[row][col] = random.choice(non_pii_words)

# Initialize the grid
initialize_grid()

# Player position and lives
player_pos = [0, 0]
player_lives = 3

# Fonts
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
message_font = pygame.font.Font(None, 48)

def draw_grid():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            # Draw cell - all cells are white (no visual distinction between PII and non-PII)
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE + TOP_MARGIN, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 2)
            
            # Draw word if not empty
            if grid[row][col]:
                # Split multi-word terms into lines
                words = grid[row][col].split()
                if len(words) > 1:
                    # Multi-word term - render on multiple lines
                    line_height = font.get_height()
                    y_offset = -(line_height * (len(words) - 1)) / 2
                    
                    for word in words:
                        text = font.render(word, True, BLACK)
                        text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE/2,
                                                    row * CELL_SIZE + TOP_MARGIN + CELL_SIZE/2 + y_offset))
                        screen.blit(text, text_rect)
                        y_offset += line_height
                else:
                    # Single word - render normally
                    text = font.render(grid[row][col], True, BLACK)
                    text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE/2,
                                                    row * CELL_SIZE + TOP_MARGIN + CELL_SIZE/2))
                    screen.blit(text, text_rect)

def draw_player():
    player_x = player_pos[1] * CELL_SIZE + CELL_SIZE/2 - PLAYER_SIZE/2
    player_y = player_pos[0] * CELL_SIZE + TOP_MARGIN + CELL_SIZE/2 - PLAYER_SIZE/2
    pygame.draw.rect(screen, BLUE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

def eat_word():
    global remaining_pii_words, player_lives
    row, col = player_pos
    current_word = grid[row][col]
    
    if not current_word:  # Empty cell
        return
    
    if current_word in pii_words:
        # Correct - ate a PII word
        remaining_pii_words -= 1
        grid[row][col] = ""  # Clear the cell
    else:
        # Incorrect - ate a non-PII word
        player_lives -= 1  # Lose a life
        grid[row][col] = ""  # Clear the cell

def draw_lives():
    # Draw life indicators at the top
    life_size = 40
    spacing = 15
    for i in range(3):
        x = 20 + i * (life_size + spacing)
        y = 30
        color = BLUE if i < player_lives else GRAY
        pygame.draw.rect(screen, color, (x, y, life_size, life_size))

def draw_controls_button():
    # Draw controls button
    button_width = 120
    button_height = 40
    button_x = WINDOW_WIDTH - button_width - 20
    button_y = 10
    
    pygame.draw.rect(screen, GRAY, (button_x, button_y, button_width, button_height))
    pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height), 2)
    
    text = font.render("Controls", True, WHITE)
    text_rect = text.get_rect(center=(button_x + button_width/2, button_y + button_height/2))
    screen.blit(text, text_rect)
    
    return pygame.Rect(button_x, button_y, button_width, button_height)

def draw_controls_popup():
    # Draw controls popup
    popup_width = 400
    popup_height = 300
    popup_x = WINDOW_WIDTH//2 - popup_width//2
    popup_y = WINDOW_HEIGHT//2 - popup_height//2
    
    pygame.draw.rect(screen, BLACK, (popup_x, popup_y, popup_width, popup_height))
    pygame.draw.rect(screen, WHITE, (popup_x, popup_y, popup_width, popup_height), 3)
    
    # Title
    title_text = message_font.render("Game Controls", True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, popup_y + 40))
    screen.blit(title_text, title_rect)
    
    # Controls info
    controls = [
        "Arrow Keys: Move player",
        "Spacebar: Eat word",
        "R: Restart game",
        "",
        "Goal: Eat all PII words and avoid non-PII words"
    ]
    
    y_pos = popup_y + 100
    for line in controls:
        text = font.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, y_pos))
        screen.blit(text, text_rect)
        y_pos += 40
    
    # Close button
    close_text = font.render("Close", True, WHITE)
    close_rect = close_text.get_rect(center=(WINDOW_WIDTH//2, popup_y + popup_height - 40))
    pygame.draw.rect(screen, GRAY, (close_rect.x - 20, close_rect.y - 10, close_rect.width + 40, close_rect.height + 20))
    pygame.draw.rect(screen, WHITE, (close_rect.x - 20, close_rect.y - 10, close_rect.width + 40, close_rect.height + 20), 2)
    screen.blit(close_text, close_rect)
    
    return pygame.Rect(close_rect.x - 20, close_rect.y - 10, close_rect.width + 40, close_rect.height + 20)

def draw_status():
    # Draw top status bar background
    pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, TOP_MARGIN))
    pygame.draw.line(screen, WHITE, (0, TOP_MARGIN-1), (WINDOW_WIDTH, TOP_MARGIN-1), 2)
    
    # Draw remaining PII count
    status_text = f"PII Words: {remaining_pii_words}/{total_pii_words}"
    text = font.render(status_text, True, WHITE)
    screen.blit(text, (WINDOW_WIDTH//2 - 80, 40))
    
    # Draw lives
    lives_text = "Lives:"
    text = font.render(lives_text, True, WHITE)
    screen.blit(text, (20, 10))
    draw_lives()
    
    # Draw controls button
    controls_button = draw_controls_button()
    
    # Draw restart instructions
    if game_won or game_over:
        restart_text = "Press 'R' to restart"
        text = font.render(restart_text, True, WHITE)
        screen.blit(text, (WINDOW_WIDTH//2 - 100, TOP_MARGIN - 30))
    
    return controls_button

# Initialize variables for controls
controls_button = None
close_button = None

# Game loop
running = True
game_won = False
game_over = False
show_controls = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            if not game_won and not game_over and not show_controls:  # Only allow movement if game is active
                if event.key == pygame.K_LEFT and player_pos[1] > 0:
                    player_pos[1] -= 1
                if event.key == pygame.K_RIGHT and player_pos[1] < GRID_SIZE - 1:
                    player_pos[1] += 1
                if event.key == pygame.K_UP and player_pos[0] > 0:
                    player_pos[0] -= 1
                if event.key == pygame.K_DOWN and player_pos[0] < GRID_SIZE - 1:
                    player_pos[0] += 1
                if event.key == pygame.K_SPACE:
                    eat_word()
            
            # Allow restart with R key
            if event.key == pygame.K_r:
                initialize_grid()
                player_pos = [0, 0]
                player_lives = 3
                game_won = False
                game_over = False
                show_controls = False
                
            # Close controls with Escape key
            if event.key == pygame.K_ESCAPE and show_controls:
                show_controls = False
                
        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if controls button was clicked
            if controls_button and controls_button.collidepoint(mouse_pos) and not show_controls:
                show_controls = True
                
            # Check if close button in controls popup was clicked
            if show_controls and close_button and close_button.collidepoint(mouse_pos):
                show_controls = False

    # Check win condition
    if remaining_pii_words == 0:
        game_won = True
        
    # Check game over condition
    if player_lives <= 0:
        game_over = True

    # Draw
    screen.fill(BLACK)
    controls_button = draw_status()  # Draw status first (includes top bar)
    draw_grid()
    draw_player()
    
    # Draw win/game over messages
    if game_won:
        win_text = "YOU WIN! All PII data eaten!"
        text = message_font.render(win_text, True, GREEN)
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(text, text_rect)
    
    if game_over:
        game_over_text = "GAME OVER! You lost all lives!"
        text = message_font.render(game_over_text, True, RED)
        text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(text, text_rect)
    
    # Draw controls popup if active
    if show_controls:
        close_button = draw_controls_popup()
    else:
        close_button = None
        
    pygame.display.flip()

pygame.quit()
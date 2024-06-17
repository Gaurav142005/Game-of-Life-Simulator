import pygame # type: ignore
from Board import *
from preDefined import *

# Defining Colours
WHITE = (255, 255, 255)
LIGHT_GREY = (211, 211, 211)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)
BG_COLOR = (150, 150, 150)

SCALE = 8
rows = 5*SCALE #int(input("Enter the number of rows: "))
cols = 4*SCALE #int(input("Enter the number of columns: "))
N = int(0.15 * rows * cols)

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
BORDER = 1
# Grid Area -> (800, 640)
RSIZE = 800 / rows
CSIZE = 640 / cols

# Initialize Pygame
pygame.init()

timer = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))    # Creating the screen
pygame.display.set_caption("The Game of Life")

# Simulate event
SIMULATE = pygame.USEREVENT + 1
pygame.time.set_timer(SIMULATE, 600)

# Defining a font
smallfont = pygame.font.SysFont('Corbel',35)
random = smallfont.render('Randomise' , True , WHITE)
sim = smallfont.render('Simulate' , True , WHITE)
clear = smallfont.render('X Clear', True, WHITE)
    

def draw_grid():
    # Looping through the board and displaying the live cells
    rows = 5*SCALE #int(input("Enter the number of rows: "))
    cols = 4*SCALE #int(input("Enter the number of columns: "))
    RSIZE = 800 / rows
    CSIZE = 640 / cols
    for i in range(rows+1):   # Rows
        pygame.draw.rect(screen, (0, 0, 0), (100+i*RSIZE, 60, BORDER, 641)) # Row Grid Lines
    for i in range(cols+1): # Columns
        pygame.draw.rect(screen, (0, 0, 0), (100, 60 + i*CSIZE, 801, BORDER))   # Column Grid Lines
    
    for i in range(rows):
        for j in range(cols):
            if(board.board[i][j] == 1):
                pygame.draw.rect(screen, YELLOW, (100+i*RSIZE+BORDER, 60+j*CSIZE+BORDER, RSIZE-BORDER, CSIZE-BORDER))


# Game Loop
running = True
simulate = False

board = Board(rows, cols, N)
board.createRandomBoard()
board.displayBoard()
while running:
    screen.fill(BG_COLOR)
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 4 - 110, 720, 170, 50))  # Randomise Button
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 2 - 80, 720, 170, 50))  # Simulate Button
    pygame.draw.rect(screen, BLUE, (3 * SCREEN_WIDTH // 4 - 60, 720, 170, 50))  # Clear Button
    
    pygame.draw.rect(screen, LIGHT_GREY, (100, 60, 801, 641))  # Shade over baord area
    
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse Click for Simulator
            if SCREEN_WIDTH // 2 - 80 <= mouse[0] <= SCREEN_WIDTH // 2 + 90 and 720 <= mouse[1] <= 770:
                simulate = True
            
            # Selecting cells manaully within the grid
            if 100 <= mouse[0] <= 900 and 60 <= mouse[1] <= 700:    # Within grid
                x, y = mouse[0] - 100, mouse[1] - 60
                i, j = int(x // RSIZE), int(y // CSIZE)
                board.board[i][j] = 1
            
            # Clear board button
            if 3 * SCREEN_WIDTH // 4 - 60 <= mouse[0] <= 3 * SCREEN_WIDTH // 4 + 110 and 720 <= mouse[1] <= 770:    # Clear
                board.board = np.zeros((rows, cols))
                simulate = False
                board.gen = 1
            
            if SCREEN_WIDTH // 4 - 110 <= mouse[0] <= SCREEN_WIDTH // 4 + 60 and 720 <= mouse[1] <= 770:    # Clear
                board = Board(rows, cols, N)
                board.createRandomBoard()
                board.gen = 1
                board.displayBoard()
                simulate = False
                
        # Simulate Control on its own
        if event.type == SIMULATE and simulate:
            board.survival()
            board.displayBoard()
        
        if event.type == pygame.KEYDOWN:

            # Manually see each generation
            if event.key == pygame.K_SPACE:
                simulate = False
                board.survival()
                board.displayBoard()

            # 101 pattern
            if event.key == pygame.K_a:
                simulate = False
                board = Board(rows, cols, N)
                board.board = p101
                board.displayBoard()
            
            if event.key == pygame.K_p:
                simulate = False
            
            if event.key == pygame.K_UP:
                if SCALE > 1:
                    SCALE -= 1
            if event.key == pygame.K_DOWN:
                if SCALE < 8:
                    SCALE += 1 

        # Quit Event
        if event.type == pygame.QUIT:
            running = False
        

    draw_grid() # Drawing the grid
    # Displaying the text onto our button
    screen.blit(sim , (SCREEN_WIDTH // 2 - 45, 732))
    screen.blit(clear , (3 * SCREEN_WIDTH // 4  - 15, 732))
    screen.blit(random , (SCREEN_WIDTH // 4 - 90, 732))
    
    gen = smallfont.render(f'Generation: {board.gen}', True, BLACK)
    screen.blit(gen , (100, 30))
    pygame.display.flip()
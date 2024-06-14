import pygame # type: ignore
from Board import *
from preDefined import *

# Defining Colours
WHITE = (255, 255, 255)
LIGHT_GREY = (211, 211, 211)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 215, 0)

rows = 40
cols = 32
N = 200

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
sim = smallfont.render('Simulate' , True , WHITE)
clear = smallfont.render('X Clear', True, WHITE)
    

board = Board(rows, cols, N)
board.createRandomBoard()
board.displayBoard()


def draw_grid():
    # Looping through the board and displaying the live cells
    for i in range(rows):
        for j in range(cols):
            if(board.board[i][j] == 1):
                pygame.draw.rect(screen, YELLOW, (100+i*RSIZE+BORDER, 60+j*CSIZE+BORDER, RSIZE-BORDER, CSIZE-BORDER))


# Game Loop
running = True
simulate = False
while running:
    screen.fill((150, 150, 150))
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH // 4, 720, 145, 50))  # Simulate Button
    pygame.draw.rect(screen, BLUE, (3 * SCREEN_WIDTH // 4 - 100, 720, 145, 50))  # Simulate Button
    
    pygame.draw.rect(screen, LIGHT_GREY, (100, 60, 801, 641))  # Shade
    for i in range(rows+1):   # Rows
        pygame.draw.rect(screen, (0, 0, 0), (100+i*RSIZE, 60, BORDER, 641)) # Row Grid Lines
    for i in range(cols+1): # Columns
        pygame.draw.rect(screen, (0, 0, 0), (100, 60 + i*CSIZE, 801, BORDER))   # Column Grid Lines
    
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Mouse Click for Simulator
            if SCREEN_WIDTH // 4 <= mouse[0] <= SCREEN_WIDTH // 4 + 140 and 720 <= mouse[1] <= 770:
                simulate = True
            
            # Selecting cells within the grid
            if 100 <= mouse[0] <= 900 and 60 <= mouse[1] <= 700:    # Within grid
                x, y = mouse[0] - 100, mouse[1] - 60
                i, j = int(x // RSIZE), int(y // CSIZE)
                board.board[i][j] = 1
            
            # Clear board button
            if 3 * SCREEN_WIDTH // 4 - 100 <= mouse[0] <= 3 * SCREEN_WIDTH // 4 + 45 and 720 <= mouse[1] <= 770:    # Clear
                board.board = np.zeros((rows, cols))
                simulate = False
                board.gen = 1
                
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

            if event.key == pygame.K_r:
                board = Board(rows, cols, N)
                board.createRandomBoard()
                board.gen = 1
                board.displayBoard()
                simulate = False


        # Quit Event
        if event.type == pygame.QUIT:
            running = False
        

    draw_grid()
    # Displaying the text onto our button
    screen.blit(sim , (SCREEN_WIDTH // 4 + 20, 732))
    screen.blit(clear , (3 * SCREEN_WIDTH // 4  - 70, 732))
    gen = smallfont.render(f'Generation: {board.gen}', True, BLACK)
    screen.blit(gen , (100, 30))
    pygame.display.flip()
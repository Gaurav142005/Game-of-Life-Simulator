import numpy as np # type: ignore

class Board:
    def __init__(self, row, col, n):
        self.row = row
        self.col = col
        self.n = n
        self.board = np.zeros((self.row, self.col), dtype=int)
        self.flag = 0
        self.endgame = False
        self.gen = 1

    # To display the board at any time
    def displayBoard(self):
        print("The Board state is: \n")
        for i in range(self.row):
            for j in range(self.col):
                if(self.board[i][j] == 2):
                    self.board[i][j] = 1
                if(self.board[i][j] == 3):
                    self.board[i][j] = 0
                if(self.board[i][j] == 0):
                    print(" 0 ", end="")
                else:
                    print(" " + str(self.board[i][j]) + " ", end="")
            print()
        print()
    
    # Create a randomized board state
    def createRandomBoard(self):
        self.randX = np.random.randint(0, self.row, size=self.n)
        self.randY = np.random.randint(0, self.col, size=self.n)
        for i in range(self.n):
            self.board[self.randX[i]][self.randY[i]] = 1
    
    # Counts number of neighbours (alive)
    def neighbours(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Coordinates of neighbouring cells
                nx = x + i
                ny = y + j

                if(nx >= 0 and nx < self.row and ny >= 0 and ny < self.col and not(i == 0 and j == 0)):
                    if(self.board[nx][ny] == 1 or self.board[nx][ny] == 3): # Current alive neighbour count
                        count += 1
        return count

    # Simulates one generation 
    def survival(self):
        if not self.endgame:
            self.gen += 1
            for i in range(self.row):
                for j in range(self.col):
                    state = self.board[i][j]    # Current State
                    if(state == 0):     # Dead Cell
                        if(self.neighbours(i, j) == 3): # Reproduction
                            self.board[i][j] = 2 # (Dead now, alive later)
                            self.flag = 1
                    
                    if(state == 1): # Alive cell
                        if(self.neighbours(i, j) < 2): # Underpopulation
                            self.board[i][j] = 3    # (Alive now, dead later)
                            self.flag = 1    
                        
                        if(self.neighbours(i, j) > 3):  # Overpopulation
                            self.board[i][j] = 3    # (Alive now, dead later)
                            self.flag = 1
        
        if(self.flag == 1):
            self.flag = 0
        else:
            self.endgame = True
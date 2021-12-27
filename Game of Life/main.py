import pygame
from pygame.display import update
import time


import numpy as np

def generate_board():
    board = np.zeros(100).reshape(10,10)

    # blinker
    # board[3,3] = 1
    # board[3,4] = 1
    # board[3,5] = 1

    # R-pentomino
    # board[2,3] = 1
    # board[2,4] = 1
    # board[3,2] = 1
    # board[3,3] = 1
    # board[4,3] = 1 

    board[5,2] = 1
    board[6,3] = 1
    board[4,4] = 1
    board[5,4] = 1
    board[6,4] = 1

    return board


def update_board(matrix):
    rows, cols = matrix.shape
    matrix_new = np.zeros(rows*cols).reshape(rows,cols)
    for row in range(rows):
        for col in range(cols):
            neighbours = (
                matrix[row - 1][col - 1] 
                + matrix[row - 1][col   ] 
                + matrix[row - 1][col +1 if col < cols -1 else 0]
                + matrix[row    ][col +1 if col < cols -1 else 0]
                + matrix[row + 1 if row < rows -1 else 0][col +1 if col < cols -1 else 0]
                + matrix[row + 1 if row < rows -1 else 0][col   ] 
                + matrix[row + 1 if row < rows -1 else 0][col -1]
                + matrix[row    ][col -1])
            if matrix[row][col] == 0:
                matrix_new[row][col] = 1 if neighbours == 3 else 0
            else:
                matrix_new[row][col] = 1 if neighbours in [2, 3] else 0


    return matrix_new

def createSquare(gridDisplay, x, y, color):
    pass
    # pygame.draw.rect(gridDisplay, color, [x, y, grid_node_width, grid_node_height ])

def createCircle(gridDisplay, x, y, r, color):
    pygame.draw.circle(gridDisplay, color, (x + r, y + r), r, 0)



def visualizeGrid(gridDisplay, matrix, pixel_size, offset_x, offset_y):
    cleanGrid(offset_x, offset_y, 20, 20, pixel_size)
    y = offset_y  # we start at the top of the screen
    for row in matrix:
        x = offset_x # for every row we start at the left of the screen again
        for item in row:
            if item == 1:
                createCircle(gridDisplay, x, y, 5, (0, 40, 0))
            x += pixel_size
        y += pixel_size
    pygame.display.update()

def cleanGrid(offset_x, offset_y, pixel_x, pixel_y, pixel_size):
    pygame.display.get_surface().fill((220, 220, 220))
    for x in range(pixel_x+1):
        for y in range(pixel_y+1):
            pygame.draw.line(pygame.display.get_surface(), (150, 150, 150), (offset_x + x * pixel_size,offset_y), (offset_x + x * pixel_size,offset_y+100), 1 )

def start_game():
    window_x , window_y = 300 , 300
    pixel_x , pixel_y = 20 , 20
    pixel_size = 10

    offset_x, offset_y = (window_x - pixel_x * pixel_size) / 2 , (window_y - pixel_y * pixel_size) / 2

    gridDisplay = pygame.display.set_mode((window_x , window_y))
    cleanGrid(offset_x, offset_y, pixel_x , pixel_y, pixel_size)

    matrix = generate_board()

    # visualizeGrid(matrix)

    # waint until user quits
    running, i = True, 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if i%100 == 0:
            print("iteration: ",i)
        i += 1
        
        visualizeGrid(gridDisplay, matrix, pixel_size, offset_x, offset_y)
        time.sleep(0.02)
        matrix = update_board(matrix)
    pygame.quit()


start_game()
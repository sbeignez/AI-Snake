import pygame
import time
import random
import sys

SPEED = 40
BOARD_ROWS = 20
BOARD_COLS = 20
SCALE = 30
COLOR_BOARD = (20, 20, 20)
COLOR_APPLE = (200, 0, 0)
COLOR_CELL = (40, 40, 40)
COLOR_SNAKE = (200, 200, 0)
COLOR_SNAKE_2 = (150, 150, 0)
COLOR_SNAKE_SPINE = (40, 40, 0)
COLOR_PAUSE = (200, 200, 200)
COLOR_SCORE = (200, 200, 200)

COLOR_MOVE_BEST = (30, 30, 200)
COLOR_MOVES = (30, 30, 100)


def display_board(window, board):

    pygame.display.get_surface().fill(COLOR_BOARD)
    snake = board["snake"]
    apple = board["apple"]
    pause = board["pause"]
    font = pygame.font.SysFont('Courier', int(SCALE / 2), bold=True)
    # print(pygame.font.get_fonts())
    score = "SCORE: " + ("0000" + str(board["score"]))[-4:] + " - MOVES: " + ("0000000" + str(board["steps"]))[-7:]

    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            draw_cell(window, r, c, COLOR_CELL)

    draw_snake(window, snake)
    draw_apple(window, apple[0], apple[1], COLOR_APPLE)
    if pause:
        draw_pause(window)

    draw_score(window, font, score)
    draw_moves(window, board["moves"], board["move"])

    pygame.display.update()

def draw_cell(window, x, y, color):
    pygame.draw.rect(window, color, pygame.Rect(x * SCALE, y * SCALE, SCALE, SCALE), 1)

def draw_apple(window, x, y, color):
    pygame.draw.circle(window, color, ((y+.5) * SCALE, (x+.5) * SCALE, ), (SCALE * .75)/2, 0)

def draw_pause(window):
    pygame.draw.rect(window, COLOR_PAUSE, pygame.Rect(BOARD_COLS * SCALE / 3, BOARD_ROWS * SCALE / 3, BOARD_COLS * SCALE / 9, BOARD_ROWS * SCALE / 3))
    pygame.draw.rect(window, COLOR_PAUSE, pygame.Rect(BOARD_COLS * SCALE * 5 / 9, BOARD_ROWS * SCALE / 3, BOARD_COLS * SCALE / 9, BOARD_ROWS * SCALE / 3))

def draw_snake(window, snake, color = COLOR_SNAKE):
    x_0, y_0 = None, None
    body = snake["body"]
    L = len(body)
    for i, s in enumerate(body):
        x, y = s[0], s[1]
        R = SCALE/2 * ( - 1 / (2* L) * i + 0.8)
        # pygame.draw.circle(window, color, ((y+.5) * SCALE, (x+.5) * SCALE ), R, 0)
        pygame.draw.rect(window, color if i==L-1 else COLOR_SNAKE_2, pygame.Rect(y * SCALE + 1, x * SCALE + 1, SCALE - 2, SCALE - 2), 0, border_radius= 1)
        if x_0 is not None:
            pass
            pygame.draw.line(window, COLOR_SNAKE_SPINE, ((y_0+.5)*SCALE,(x_0+.5)*SCALE), ((y+.5)*SCALE,(x+.5)*SCALE), 4)
            steps = 4
            for j in range(steps):
                pass
                # pygame.draw.rect(window, color, pygame.Rect((y + (1-SIZE) / 2) * SCALE, (x + (1-SIZE) / 2) * SCALE, SCALE * SIZE, SCALE * SIZE), 0, border_radius= 2)
                # pygame.draw.circle(window, COLOR_SNAKE_2, (((y_0*(steps-j)+y*j)/steps+.5) * SCALE, ((x_0*(steps-j)+x*j)/steps+.5) * SCALE, ), R, 0)
        x_0, y_0 = x, y

def draw_moves(window, moves, move):
    for m in moves:
        x, y = m[0], m[1]
        pygame.draw.rect(window, COLOR_MOVE_BEST if m==move else COLOR_MOVES, pygame.Rect(y * SCALE + 1, x * SCALE + 1, SCALE - 2, SCALE - 2), 0, border_radius= 1)

def draw_score(window, font, score):
    window.blit(font.render(score, True, COLOR_SCORE), (0, (SCALE+.5) * BOARD_ROWS))

def is_game_over(board):
    return False


def create_apple(snake):
    if len(snake["body"]) == BOARD_ROWS * BOARD_COLS:
        return None
    cells = { (r,c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) } - set(snake["body"]) 
    apple = random.choice(tuple(cells))
    print("APPLE:", apple)
    return apple

def init_board():
    snake = {
        "body" : [(0,0)],
        "lenght" : 3,
    }
    apple = create_apple(snake)
    board = {
        "apple" : apple,
        "snake" : snake,
        "pause" : False,
        "score" : 0,
        "steps" : 0,
    }
    return board

def move(board):
    apple = board["apple"]
    moves = set()
    body = board["snake"]["body"]
    head = body[-1]
    # UP
    if head[0] > 0 and (head[0]-1, head[1]) not in body:
        moves.add((head[0]-1, head[1]))
    # DOWN
    if head[0] < BOARD_ROWS - 1 and (head[0]+1, head[1]) not in body:
        moves.add((head[0]+1, head[1]))
    # RIGHT
    if head[1] < BOARD_COLS - 1 and (head[0], head[1]+1) not in body:
        moves.add((head[0], head[1]+1))
    # LEFT
    if head[1] > 0 and (head[0], head[1]-1) not in body:
        moves.add((head[0], head[1]-1))

    print("BODY:", body)
    print("MOVES:", moves)
    move = None
    if moves:
        move = min(moves, key = lambda x : abs(x[0] - apple[0]) + abs(x[1] - apple[1]))
    print("MOVE:", move)

    return moves, move

def start_game():
    window_x_px , window_y_px = BOARD_COLS * SCALE, BOARD_ROWS * SCALE + SCALE

    pygame.init()
    pygame.display.set_caption('Snake A.I. 2022')
    window = pygame.display.set_mode( (window_x_px , window_y_px) )
    
    board = init_board()
    snake = board["snake"]
    direction = (0,0)

    # waint until user quits
    running, game_over, board["steps"] = True, False, 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    start_game()
                if event.key == pygame.K_SPACE:
                    board["pause"] = not board["pause"]
                if event.key == pygame.K_LEFT:
                    if direction != (0,1):
                        direction = (0,-1)
                    board["pause"] = False
                if event.key == pygame.K_RIGHT:
                    if direction != (0, -1):
                        direction = (0,1)
                    board["pause"] = False
                if event.key == pygame.K_UP:
                    direction = (-1,0)
                    board["pause"] = False
                if event.key == pygame.K_DOWN:
                    direction = (1,0)
                    board["pause"] = False
                print(">> ", direction)

        
        # MOVE
        if not board["pause"]:

            board["moves"], board["move"] = move(board)
            if board["move"]:
                direction = ( board["move"][0] - snake["body"][-1][0], board["move"][1] - snake["body"][-1][1])
            else:
                game_over = True

            new_head = (snake["body"][-1][0] + direction[0], snake["body"][-1][1] + direction[1])
            if new_head[0] < 0 or new_head[0] >= BOARD_COLS or new_head[1] < 0 or new_head[1] >= BOARD_ROWS:
                board["pause"] = True
            elif new_head == board["apple"]:
                if len(snake["body"]) == BOARD_ROWS * BOARD_COLS:
                    print("VICTORY")
                board["apple"] = create_apple(snake)

                snake["lenght"] += 1
                board["score"] += 1

            elif new_head in snake["body"]:
                game_over = True
                print("GAME OVER")
                board["pause"] = True
            else:
                snake["body"].append(new_head)
                snake["body"] = snake["body"][- snake["lenght"]:]

            # print(board["snake"], board["apple"]) 
            board["steps"] += 1

        display_board(window, board)
        time.sleep( 1/ SPEED )



    pygame.quit()



start_game()
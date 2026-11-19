import pygame as pg
import sys
import copy

# ==== CONTROLS ====
# [E] - makes next step when paused;
# [R] - clears the field;
# [SPACE] - pause/unpause;
# [Left Click] - place/remove cell when paused;
# [Q] - change simulation speed;


# ==== RULES ====
# Each cell looks at it's 8 neighbors
# 1) if a living cell has less than 2 alive cells - death
# 2) if a living cell has 2-3 alive cells - nothing changes
# 3) if a living cell has more than 3 alive cells - death
# 4) if a dead cell has exactly 3 alive cells - life


# ==== PARAMETERS ====
pg.init()

SQUARE_SIDE = 30
# [W]idth or [H]eight = (amount of cells inside of red area in [W]idth/[H]eight) * SQUARE_SIDE + (border compensation)
W = 30*SQUARE_SIDE + 2*SQUARE_SIDE 
H = 30*SQUARE_SIDE + 2*SQUARE_SIDE

ROWS = H//SQUARE_SIDE
COLS = W//SQUARE_SIDE

GREY = (32, 32, 32)
ORANGE = (255, 150, 0)
BLUE = (0, 150, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0,0,0)
WHITE = (255,255,255)

SPEED_MODIFIER = 1000

SPEED_TEXT = f"Speed: x{SPEED_MODIFIER/1000}"

# ==== FUNCTIONS ====
def update_field(field_current: list, field_buffer: list):
    """Updates cells on the field"""
    counter = 0
    for row in range(1, ROWS-1):
        for col in range(1, COLS-1):
            if field_current[row-1][col]: counter += 1
            if field_current[row+1][col]: counter += 1
            if field_current[row][col-1]: counter += 1
            if field_current[row][col+1]: counter += 1
            if field_current[row-1][col-1]: counter += 1
            if field_current[row-1][col+1]: counter += 1
            if field_current[row+1][col-1]: counter += 1
            if field_current[row+1][col+1]: counter += 1

            if field_current[row][col]:
                if counter < 2: field_buffer[row][col] = 0
                elif counter > 3: field_buffer[row][col] = 0
                else: field_buffer[row][col] = field_current[row][col]
            else:
                if counter == 3: field_buffer[row][col] = 1
            counter = 0
            

def draw_grid():
    """Draws a grid and a boundary over field."""
    # Draws horizontal lines
    for i in range(2, H//SQUARE_SIDE - 1):
        pg.draw.line(screen, GREY, (SQUARE_SIDE, i*SQUARE_SIDE), (W-SQUARE_SIDE, i*SQUARE_SIDE))
    
    # Draws vertical lines
    for i in range(2, W//SQUARE_SIDE - 1):
        pg.draw.line(screen, GREY, (i*SQUARE_SIDE, SQUARE_SIDE), (i*SQUARE_SIDE, H-SQUARE_SIDE))
    
    # Draws red borders
    pg.draw.line(screen, RED, (SQUARE_SIDE, SQUARE_SIDE), (W - SQUARE_SIDE, SQUARE_SIDE))
    pg.draw.line(screen, RED, (SQUARE_SIDE, SQUARE_SIDE), (SQUARE_SIDE, H - SQUARE_SIDE))
    pg.draw.line(screen, RED, (SQUARE_SIDE, H - SQUARE_SIDE), (W - SQUARE_SIDE, H - SQUARE_SIDE))
    pg.draw.line(screen, RED, (W - SQUARE_SIDE, SQUARE_SIDE), (W - SQUARE_SIDE, H - SQUARE_SIDE))

def matrix_visualizer(matrix: list):
    """Converts 1's in a matrix into colored squares"""
    for row in range(0, ROWS):
        for col in range(0, COLS):
            if matrix[row][col]:
                r = pg.Rect(col*SQUARE_SIDE, row*SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE)
                pg.draw.rect(screen, BLUE, r)

def put_cell(pos: tuple, matrix: list):
    """Puts a cell on the screen upon mouse click"""
    row = pos[1]//SQUARE_SIDE
    col = pos[0]//SQUARE_SIDE
    if (row >= 1 and row <= H//SQUARE_SIDE - 2) and (col >= 1 and col <= W//SQUARE_SIDE - 2):
        if matrix[row][col] == 0: matrix[row][col] = 1
        else: matrix[row][col] = 0

def GUI_pause(pause: bool):
    """Displays GUI Pause indicator"""
    if pause:
        r = pg.Rect(0, 0, SQUARE_SIDE, SQUARE_SIDE)
        pg.draw.rect(screen, RED, r)
    else:
        r = pg.Rect(0, 0, SQUARE_SIDE, SQUARE_SIDE)
        pg.draw.rect(screen, GREEN, r)

text_font = pg.font.SysFont("Arial", 15)
def draw_text(text, font, color, x=W-(SQUARE_SIDE*3), y=0):
    """Displays current simulation speed as text"""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


# ==== MAIN CODE ====
pg.init()
screen = pg.display.set_mode((W, H))
field_clear = [[0 for _ in range(COLS+1)] for _ in range(ROWS+1)]
field_current = [[0 for _ in range(COLS+1)] for _ in range(ROWS+1)]
field_buffer = [[0 for _ in range(COLS+1)] for _ in range(ROWS+1)]

pause = True

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        
        if event.type == pg.MOUSEBUTTONDOWN and pause:
            # (x,y) = (col, row)
            put_cell(event.pos, field_current)
            matrix_visualizer(field_current)
        
        if event.type == pg.KEYDOWN:
            # pause handler
            if event.key == pg.K_SPACE: 
                pause = False if pause else True
            # field cleaner  
            elif event.key == pg.K_r:
                field_current = copy.deepcopy(field_clear)
            # makes next simulation step when paused
            elif event.key == pg.K_e and pause:
                update_field(field_current, field_buffer)
                field_current = copy.deepcopy(field_buffer)
                field_buffer = copy.deepcopy(field_clear)
                matrix_visualizer(field_current)
                draw_grid()
                pg.display.flip()
            elif event.key == pg.K_q:
                SPEED_MODIFIER *= 0.5
                if (SPEED_MODIFIER < 125): SPEED_MODIFIER = 1000
                SPEED_TEXT = f"Speed: x{SPEED_MODIFIER/1000}"
                

    if pause:
        screen.fill(BLACK)
        draw_text(SPEED_TEXT, text_font, WHITE)
        GUI_pause(pause)
        matrix_visualizer(field_current)
        draw_grid()
        pg.display.flip()
    else:
        update_field(field_current, field_buffer)
        screen.fill(BLACK)
        draw_text(SPEED_TEXT, text_font, WHITE)
        GUI_pause(pause)
        field_current = copy.deepcopy(field_buffer)
        field_buffer = copy.deepcopy(field_clear)
        matrix_visualizer(field_current)
        draw_grid()
        pg.display.flip()
        pg.time.delay(int(SPEED_MODIFIER))
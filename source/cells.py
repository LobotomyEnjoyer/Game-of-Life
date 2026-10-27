import pygame as pg
import sys
import time

W = 1024
H = 1024

pg.init()
screen = pg.display.set_mode((W, H))

SQUARE_SIDE = 15
GREY = (32, 32, 32)
ORANGE = (255, 150, 0)
BLUE = (0, 150, 255)
BLACK = (0,0,0)
r = pg.Rect(0, 0, SQUARE_SIDE, SQUARE_SIDE)

def draw_grid():
    for i in range(0, H//SQUARE_SIDE+1):
        pg.draw.line(screen, GREY, (0, i*SQUARE_SIDE), (W, i*SQUARE_SIDE))
        pg.draw.line(screen, GREY, (i*SQUARE_SIDE, 0), (i*SQUARE_SIDE, W))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    screen.fill(BLACK)
    draw_grid()
    r.move_ip(15,0)
    pg.draw.rect(screen, ORANGE, r)
    pg.display.flip()
    time.sleep(0.5)
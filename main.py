#!/usr/bin/env python3

import pygame as pg

pg.init()
global scale
scale = 2
board_size = (10, 10)
screen = pg.display.set_mode([board_size[0]*16 * scale, board_size[1]*16 * scale])

import typing
from cell import Cell


clock = pg.time.Clock()


def main():
    cells = []
    for width in range(board_size[0]):
        cells.append([])
        for height in range(board_size[1]):
            cells[width].append(Cell((width, height), scale=scale))

    running = True
    while running:
        # x, y = pg.mouse.get_pos()
        # screen.fill([x/1920 * 255, y/1080 * 255, (x*y) % 255])

        for width in range(board_size[0]):
            for height in range(board_size[1]):
                cells[width][height].draw(screen)

        pg.display.flip()

        print(clock.tick())

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            print(pg.time.get_ticks(), event)


if __name__ == "__main__":
    main()

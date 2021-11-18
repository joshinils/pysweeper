#!/usr/bin/env python3

import pygame as pg
from pygame import mouse

from config import Conf

import typing
from cell import Cell

from scipy.ndimage import convolve
import numpy as np


def set_neighbors(cell_matrix: typing.List[typing.List[Cell]]):
    a = np.zeros((len(cell_matrix), len(cell_matrix[0])))

    for width in range(Conf.board_size[0]):
        for height in range(Conf.board_size[1]):
            a[width][height] = cell_matrix[width][height].has_bomb
    conv = convolve(a, [[1, 1, 1], [1, 1, 1], [1, 1, 1]], mode='constant')

    for width in range(Conf.board_size[0]):
        for height in range(Conf.board_size[1]):
            cell_matrix[width][height].set_neighbors(conv[width][height])


def convert_mouse_pos_to_cell(pos):
    return (int(pos[0] / Conf.scale / Conf.tile_size), int(pos[1] / Conf.scale / Conf.tile_size))


def get_offsets_list() -> typing.List[typing.Tuple[int, int]]:
    return [
        (+1, +1),
        (+1,  0),
        (+1, -1),
        (+0, +1),
        (+0,  0),
        (+0, -1),
        (-1, +1),
        (-1,  0),
        (-1, -1),
    ]


def reveal_around(pos, cells):
    for offset in get_offsets_list():
        p = (pos[0] + offset[0], pos[1] + offset[1])
        if p[0] < 0 or p[1] < 0:
            continue
        try:
            if cells[p[0]][p[1]].left_click():
                reveal_around((p[0], p[1]), cells)
        except:
            pass


def handle_both_mouse_down(pos, cells):
    if not cells[pos[0]][pos[1]].is_revealed:
        return

    sum_flags = 0

    for offset in get_offsets_list():
        p = (pos[0] + offset[0], pos[1] + offset[1])
        if p[0] < 0 or p[1] < 0:
            continue
        try:
            sum_flags += cells[p[0]][p[1]].has_flag
            sum_flags += cells[p[0]][p[1]].has_bomb and cells[p[0]][p[1]].is_revealed
        except:
            pass

    # print(sum_flags)

    if sum_flags == cells[pos[0]][pos[1]].neighbors:
        # reveal neighbors without flag
        for offset in get_offsets_list():
            p = (pos[0] + offset[0], pos[1] + offset[1])
            if p[0] < 0 or p[1] < 0:
                continue
            try:
                if (
                    cells[p[0]][p[1]].has_flag
                    or (
                        cells[p[0]][p[1]].has_bomb
                        and
                        cells[p[0]][p[1]].is_revealed
                    )
                ):
                    continue
                else:
                    if cells[p[0]][p[1]].left_click():
                        reveal_around((p[0], p[1]), cells)
            except:
                pass


def depress(pos, cells):
    for offset in get_offsets_list():
        p = (pos[0] + offset[0], pos[1] + offset[1])
        if p[0] < 0 or p[1] < 0:
            continue
        try:
            cells[p[0]][p[1]].depress()
        except:
            pass


def undepress_all(cells):
    for width in range(Conf.board_size[0]):
        for height in range(Conf.board_size[1]):
            cells[width][height].undepress()


def middle_click_all(cells):
    for width in range(Conf.board_size[0]):
        for height in range(Conf.board_size[1]):
            handle_both_mouse_down([width, height], cells)


def dirty_all_cells(cells):
    for width in range(Conf.board_size[0]):
        for height in range(Conf.board_size[1]):
            cells[width][height].state_changed = True


def main():
    cells = []
    #    global Conf.scale # but why say this here?
    for width in range(Conf.board_size[0]):
        cells.append([])
        for height in range(Conf.board_size[1]):
            cells[width].append(Cell((width, height), scale=Conf.scale))

    set_neighbors(cells)

    mouse_left_down = False
    mouse_right_down = False
    mouse_both_down = False

    running = True
    while running:
        # x, y = pg.mouse.get_pos()
        # screen.fill([x/1920 * 255, y/1080 * 255, (x*y) % 255])

        for width in range(Conf.board_size[0]):
            for height in range(Conf.board_size[1]):
                cells[width][height].draw(Conf.screen)

        pg.display.flip()

        if mouse_both_down and (not mouse_left_down or not mouse_right_down):
            mouse_both_down = False
            undepress_all(cells)

        mouse_both_down = mouse_left_down and mouse_right_down

        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    mouse_left_down = True
                if event.button == pg.BUTTON_RIGHT:
                    mouse_right_down = True
                if mouse_left_down and mouse_right_down:
                    depress(pos, cells)
            elif event.type == pg.MOUSEMOTION:
                pos = convert_mouse_pos_to_cell(event.pos)
                undepress_all(cells)
                if mouse_both_down:
                    depress(pos, cells)

            elif event.type == pg.QUIT:
                running = False
            elif event.type == pg.WINDOWRESIZED:
                print(event, event.x, event.y)
                dirty_all_cells(cells)
            elif event.type == pg.MOUSEBUTTONUP:
                pos = convert_mouse_pos_to_cell(event.pos)
                print(pos)
                if event.button == pg.BUTTON_LEFT:
                    # left-click release
                    mouse_left_down = False
                    if mouse_right_down:
                        handle_both_mouse_down(pos, cells)
                    else:
                        empty_revealed = cells[pos[0]][pos[1]].left_click()
                        if empty_revealed:
                            reveal_around(pos, cells)
                elif event.button == pg.BUTTON_RIGHT:
                    # right-click release
                    mouse_right_down = False
                    if mouse_left_down:
                        handle_both_mouse_down(pos, cells)
                    else:
                        cells[pos[0]][pos[1]].right_click()
            elif event.type == pg.KEYUP:
                # example event:
                # 14496 <Event(769-KeyUp {'unicode': '-', 'key': 1073741910, 'mod': 4096, 'scancode': 86, 'window': None})> 769
                if event.key == pg.K_KP_MINUS:  # key keypad minuscule
                    Conf.scale -= 1
                    print(Conf.scale)
                    dirty_all_cells(cells)
                if event.key == pg.K_KP_PLUS:
                    Conf.scale += 1
                    print(Conf.scale)
                    dirty_all_cells(cells)
            elif event.type == pg.MOUSEWHEEL:
                # example event:
                # 19212 <Event(1027-MouseWheel {'flipped': False, 'y': -1, 'x': 0, 'which': 0, 'window': None})> 1027
                Conf.set_scale(Conf.scale * (1 + event.y / 15 * (-event.flipped * 2 +1)))
                print(Conf.scale)
                dirty_all_cells(cells)
            else:
                print(pg.time.get_ticks(), event, event.type)


if __name__ == "__main__":
    main()

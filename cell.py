from config import *
from enum import Enum
from spritesheet import SpriteSheet
import typing
import pygame as pg

import random


class CellStateEnum(Enum):
    HIDDEN = -1
    REVEALED = 0
    NEIGHBORS_1 = 1
    NEIGHBORS_2 = 2
    NEIGHBORS_3 = 3
    NEIGHBORS_4 = 4
    NEIGHBORS_5 = 5
    NEIGHBORS_6 = 6
    NEIGHBORS_7 = 7
    NEIGHBORS_8 = 8
    NEIGHBORS_9 = 9

    FLAG_REVEALED = 10
    FLAG_HIDDEN = 11

    QUESTION_REVEALED = 20
    QUESTION_HIDDEN = 21

    BOMB_REVEALED = 30
    BOMB_BLOWN = 31
    BOMB_WRONG = 32


class Cell:
    position: typing.Tuple[int, int]
    state: CellStateEnum
    state_changed: bool
    has_bomb: bool
    neighbors: int
    is_revealed: bool
    has_flag: bool
    is_depressed: bool

    sprites = SpriteSheet("sprite.png")
    global scale
    sprite_hidden_cell = sprites.image_at((0, 47, 16, 16), scale=scale)
    sprite_flag = sprites.image_at((16, 47, 16, 16), scale=scale)
    sprite_question_hidden = sprites.image_at((16*2, 47, 16, 16), scale=scale)
    sprite_question_revealed = sprites.image_at((16*3, 47, 16, 16), scale=scale)
    sprite_bomb_revealed = sprites.image_at((16*4, 47, 16, 16), scale=scale)
    sprite_bomb_exploded = sprites.image_at((16*5, 47, 16, 16), scale=scale)
    sprite_bomb_wrong = sprites.image_at((16*6, 47, 16, 16), scale=scale)
    sprite_revealed_cell = sprites.image_at((0, 63, 16, 16), scale=scale)

    sprite_numbers = [sprite_hidden_cell]
    for i in range(1, 9):
        sprite_numbers.append(sprites.image_at((i * 16, 63, 16, 16), scale=scale))

    def __init__(self: 'Cell', location: typing.Tuple[int, int], scale: float = 1) -> 'Cell':
        self.position = (location[0] * 16 * scale, location[1] * 16 * scale)
        self.has_bomb = random.random() > 0.9

        self.state = CellStateEnum.HIDDEN  # CellStateEnum(random.randint(-1, 0))

        self.state_changed = True
        self.neighbors = 0
        self.is_revealed = False
        self.has_flag = False
        self.is_depressed = False

    def set_neighbors(self, n: int = 0) -> None:
        if self.neighbors == n:
            return

        self.neighbors = int(n)
        self.state_changed = True
        if self.is_revealed:
            self.state = CellStateEnum(self.neighbors)

    def add_neighbors(self) -> None:
        self.set_neighbors(self.neighbors + 1)

    def draw(self: 'Cell', screen) -> None:
        if self.state_changed:
            self.state_changed = False

            if self.has_bomb and self.is_revealed:
                screen.blit(Cell.sprite_bomb_exploded, self.position)
            elif self.has_flag:
                screen.blit(Cell.sprite_flag, self.position)
            elif self.state == CellStateEnum.REVEALED or (self.is_depressed):
                screen.blit(Cell.sprite_revealed_cell, self.position)
            elif self.state == CellStateEnum.HIDDEN:
                screen.blit(Cell.sprite_hidden_cell, self.position)
            elif self.state == CellStateEnum.NEIGHBORS_1:
                screen.blit(Cell.sprite_numbers[1], self.position)
            elif self.state == CellStateEnum.NEIGHBORS_2:
                screen.blit(Cell.sprite_numbers[2], self.position)
            elif self.state == CellStateEnum.NEIGHBORS_3:
                screen.blit(Cell.sprite_numbers[3], self.position)
            elif self.state == CellStateEnum.NEIGHBORS_4:
                screen.blit(Cell.sprite_numbers[4], self.position)
            elif self.state == CellStateEnum.NEIGHBORS_5:
                screen.blit(Cell.sprite_numbers[5], self.position)
            elif self.state == CellStateEnum.NEIGHBORS_6:
                screen.blit(Cell.sprite_numbers[6], self.position)
            elif self.state == CellStateEnum.NEIGHBORS_7:
                screen.blit(Cell.sprite_numbers[7], self.position)
            elif self.state == CellStateEnum.NEIGHBORS_8:
                screen.blit(Cell.sprite_numbers[8], self.position)
            else:
                print("state:", self.state)

    def right_click(self):
        if not self.is_revealed:
            self.has_flag = not self.has_flag
            self.state_changed = True

    # returns if cell was revealed and empty
    def left_click(self) -> bool:
        if self.has_flag:
            return

        self.has_flag = False
        if not self.is_revealed:
            self.is_revealed = True
            self.state = CellStateEnum(self.neighbors)
            self.state_changed = True

            return self.neighbors == 0
        return False

    def depress(self):
        if not self.is_depressed and not self.is_revealed:
            self.is_depressed = True
            self.state_changed = True

    def undepress(self):
        if self.is_depressed:
            self.is_depressed = False
            self.state_changed = True

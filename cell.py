from enum import Enum
from spritesheet import SpriteSheet
import typing
import pygame as pg


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

    FLAG_REVEALED = 10
    FLAG_HIDDEN = 11

    QUESTION_REVEALED = 20
    QUESTION_HIDDEN = 21

    BOMB_REVEALED = 30
    BOMB_BLOWN = 31
    BOMB_WRONG = 32

global scale
class Cell:
    position: typing.Tuple[int, int]
    state: CellStateEnum
    state_changed: bool

    sprites = SpriteSheet("sprite.png")
    global scale
    sprite_hidden_cell   = sprites.image_at((0, 47, 16, 16), scale=scale)
    sprite_revealed_cell = sprites.image_at((0, 63, 16, 16))

    def __init__(self: 'Cell', location: typing.Tuple[int, int], scale: float = 1) -> 'Cell':
        self.position = (location[0] * 16 * scale, location[1] * 16 * scale)
        self.state = CellStateEnum.HIDDEN
        self.state_changed = True

    def draw(self: 'Cell', screen) -> None:
        if self.state_changed:
            self.state_changed = False
            if self.state == CellStateEnum.HIDDEN:
                print("hidden")
                screen.blit(Cell.sprite_hidden_cell, self.position)
            elif self.state == CellStateEnum.REVEALED:
                print("revealed")
                screen.blit(Cell.sprite_revealed_cell, self.position)
            else:
                print("state:", self.state)

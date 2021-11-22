from config import *
from enum import IntEnum
from spritesheet import SpriteSheet
from SpriteAtlas import *
import typing
import pygame as pg

import random


class CellStateEnum(IntEnum):
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
    location: typing.Tuple[int, int] # logical position, int into array
    position: typing.Tuple[int, int] # visual position, scaled, on screen space
    state: CellStateEnum
    state_changed: bool
    has_bomb: bool
    neighbors: int
    is_revealed: bool
    has_flag: bool
    is_depressed: bool
    is_muted: bool

    sprites_created: bool = False
    sprite_scale: float = -1

    @staticmethod
    def create_sprites():
        if Cell.sprites_created == True:
            return
        Cell.sprites_created = True

        #global Conf.scale
        Cell.sprite_scale = Conf.scale
        print("creating sprites", "Conf.scale", Conf.scale, "Cell.sprite_scale", Cell.sprite_scale)

        Cell.sprite_atlas = SpriteAtlas("sprite.png")

        Cell.sprite_atlas.register("hidden_cell"      , (16*0, 47, 16, 16))
        Cell.sprite_atlas.register("flag"             , (16*1, 47, 16, 16))
        Cell.sprite_atlas.register("question_hidden"  , (16*2, 47, 16, 16))
        Cell.sprite_atlas.register("question_revealed", (16*3, 47, 16, 16))
        Cell.sprite_atlas.register("bomb_revealed"    , (16*4, 47, 16, 16))
        Cell.sprite_atlas.register("bomb_exploded"    , (16*5, 47, 16, 16))
        Cell.sprite_atlas.register("bomb_wrong"       , (16*6, 47, 16, 16))
        Cell.sprite_atlas.register("revealed_cell"    , (   0, 63, 16, 16))

        #Cell.sprite_numbers = [Cell.sprite_hidden_cell]
        for i in range(1, 9):
            Cell.sprite_atlas.register("number_" + str(i), (i * 16, 63, 16, 16))
            Cell.sprite_atlas.register("number_muted_" + str(i), (i * 16, 79, 16, 16))

    def __init__(self: 'Cell', location: typing.Tuple[int, int], scale: float = 1) -> 'Cell':
        Cell.create_sprites()

        self.location = location
        self.position = (location[0] * 16 * scale, location[1] * 16 * scale)
        self.has_bomb = random.random() > 0.9

        self.state = CellStateEnum.HIDDEN  # CellStateEnum(random.randint(-1, 0))

        self.state_changed = True
        self.neighbors = 0
        self.is_revealed = False
        self.has_flag = False
        self.is_depressed = False
        self.is_muted = False

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

            # if scale has changed outside, re-do sprites
            #print("Conf.scale", Conf.scale, "Cell.sprite_scale", Cell.sprite_scale)

            if Conf.scale != Cell.sprite_scale:
                Cell.sprites_created = False
                screen.fill([0,0,0])
                Cell.create_sprites()
            self.position = (self.location[0] * 16 * Conf.scale, self.location[1] * 16 * Conf.scale)


            if self.has_bomb and self.is_revealed:
                screen.blit(Cell.sprite_atlas.get("bomb_exploded"), self.position)
            elif self.has_flag:
                screen.blit(Cell.sprite_atlas.get("flag"), self.position)
            elif self.state == CellStateEnum.REVEALED or (self.is_depressed):
                screen.blit(Cell.sprite_atlas.get("revealed_cell"), self.position)
            elif self.state == CellStateEnum.HIDDEN:
                screen.blit(Cell.sprite_atlas.get("hidden_cell"), self.position)
            elif (
                    self.state >= int(CellStateEnum.NEIGHBORS_1) and 
                    self.state <= int(CellStateEnum.NEIGHBORS_8) 
                ):
                muted = ""
                if self.is_muted:
                    muted = "muted_"
                screen.blit(Cell.sprite_atlas.get("number_" + muted + str(int(self.state))), self.position)
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

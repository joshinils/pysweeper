from typing import Iterable
import typing
import pygame as pg
from pygame.transform import scale

class Conf:
    tile_size = 16
    scale = 2.5


    @staticmethod
    def set_scale(new_scale: float) -> None:
        print("old", Conf.scale, "to_be", new_scale)

        scale_to_be = int(Conf.tile_size * new_scale) / Conf.tile_size
        scale_to_be = max(0.75, min(scale_to_be, 10))

        Conf.scale = scale_to_be
        print("is", Conf.scale)
    
    board_size: typing.Tuple[int, int] = (20, 25)
    screen_size: typing.Tuple[int, int] = (
        int(board_size[0] * int(tile_size * scale)),
        int(board_size[1] * int(tile_size * scale))
    )

    print("       tile_size", tile_size)
    print("           scale", scale)
    print("      board_size", board_size)
    print("     screen_size", screen_size)

    pg.init()
    screen = pg.display.set_mode(screen_size, pg.RESIZABLE)
    clock = pg.time.Clock()

    color_default = pg.Color("#C0C0C0")
    color_shadow = pg.Color("#808080")
    color_lit = pg.Color("#FFFFFF")

    border = {
        "all":     3,
        "info":    2,
        "counter": 1,
    }

    gap = {
        "all": 6,
        "info": {"bottom": 6},
    }

    # everything has a big border on the outside
    # - gap of 6 \w default color around everything
    # the info at the top has a medium border
    # - gap of 6 \w default color between game and info at top
    # - counters have a small border
    #   - counter has a horizontal default gap of 5
    #   - counter has a vertical default gap of 4
    # - smiley is centered
    #   - smiley button border?
    #     - maybe small?

Conf.set_scale(Conf.scale)

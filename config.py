import pygame as pg

tile_size = 16

global scale

scale = 2.5
scaled_tile_size = int(tile_size * scale)
scaled_scale = scaled_tile_size / tile_size

board_size = (20, 25)
screen_size = (int(board_size[0] * scaled_tile_size), int(board_size[1] * scaled_tile_size))

print("       tile_size", tile_size)
print("scaled_tile_size", scaled_tile_size)
print("    scaled_scale", scaled_scale)
print("           scale", scale)
print("      board_size", board_size)
print("     screen_size", screen_size)

scale = scaled_scale

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

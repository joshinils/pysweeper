import pygame as pg

tile_size = 16

scale = 1
scaled_tile_size = int(tile_size * scale)
scaled_scale = scaled_tile_size / tile_size

board_size = (200, 200)
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

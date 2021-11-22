from typing import Tuple
from spritesheet import SpriteSheet
from config import *
import pygame as pg


class Sprite():
    is_dirty: bool
    coords: typing.Tuple
    surface: pg.Surface

    def __init__(self: 'Sprite', surface: pg.Surface):
        self.is_dirty: bool = False
        self.coords: typing.Tuple = None
        self.surface = surface


class SpriteAtlas(dict):
    sheet: SpriteSheet
    scale: float

    def __init__(self: 'SpriteAtlas', filename: str):
        self.scale = Conf.scale
        self.sheet = SpriteSheet(filename)

    def rescale(self: 'SpriteAtlas', name: str):
        self[name].surface = self.sheet.image_at(self[name].coords, scale=self.scale)

    def check_scale(self: 'SpriteAtlas'):
        if Conf.scale != self.scale:
            self.scale = Conf.scale
            for name, sprite in super().items():
                self[name].is_dirty = True

    def register(self: 'SpriteAtlas', name: str, coords: Tuple):
        new_sprite = Sprite(self.sheet.image_at(coords, scale=self.scale))
        new_sprite.coords = coords

        #super()[name] = new_sprite
        self[name] = new_sprite

    def get(self: 'SpriteAtlas', name: str):
        self.check_scale()
        sprite = self[name]
        if sprite.is_dirty:
            self.rescale(name)
        return self[name].surface

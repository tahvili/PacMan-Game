import pygame
from constants import *

class Spritesheet:

    def __init__(self):
        self.sheet = pygame.image.load("res/spritesheet.png").convert()
        self.sheet.set_colorkey(TRANSPARENT)

    def get_sprite(self, x, y, width, height):

        x *= width
        y *= height
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

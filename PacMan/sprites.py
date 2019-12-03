import pygame
from constants import *
from typing import *


class Spritesheet:
    """
    This class used to visually represent all the objects in the PacMan game.
    """

    def __init__(self) -> None:
        """
        Initializes the Spritesheet object.
        """
        self.sheet = pygame.image.load("res/spritesheet.png").convert()
        self.sheet.set_colorkey(TRANSPARENT)

    def get_sprite(self, x: int, y: int, width: int, height: int) -> Any:
        """
        This method gets the correct sprite from the sprite sheet at the given
        row and column.
        """

        x *= width
        y *= height
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip())

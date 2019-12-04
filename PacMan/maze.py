from constants import *
from typing import *
import pygame


class Maze:

    """
    Maze class that builds a visual representation of the board
    for the game board
    """
    def __init__(self, sprite: Any) -> None:

        """
        Initalizer for the the Maze class
        """

        self.sprite = sprite
        self.maze_info = None
        self.rotate_info  = None
        self.sprites = []
        self.s_row = 16
        self.get_maze_sprite()

    def get_maze_sprite(self) -> None:
        """
        gets all the board sprites from the sprite sheet
        """
        for i in range(10):
            self.sprites.append(self.sprite.get_sprite(i, self.s_row, WIDTH, HEIGHT))

    def rotate(self, sprite: Any, val: int) -> None:
        """
        Rotates a sprite passed into it be a specific degree
        """
        return pygame.transform.rotate(sprite, val*90)

    def read_maze_file(self, textfile: Any) -> List[Any]:

        """
        Get information from text files
        """
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]

    def get_maze(self, textfile: Any) -> None:

        """
        Reads the file for both the main and rotation
        maze files
        """
        self.maze_info = self.read_maze_file(textfile+".txt")
        self.rotate_info = self.read_maze_file(textfile+"_rot.txt")

    def combine_maze(self, background: Any) -> None:

        """
        This method is where we actually build the maze by taking each part
        from the sprite sheet and build an image of it based on the from both
        the maze and rotation maze files.
        """
        rows = len(self.maze_info)
        cols = len(self.maze_info[0])
        for row in range(rows):
            for col in range(cols):
                x = col * WIDTH
                y = row * HEIGHT
                try:
                    val = int(self.maze_info[row][col])
                except ValueError:
                    pass
                else:
                    if self.rotate_info is not None:
                        rotVal = self.rotate_info[row][col]
                        image = self.rotate(self.sprites[val], int(rotVal))
                        background.blit(image, (x, y))
                    else:
                        background.blit(self.sprites[val], (x, y))

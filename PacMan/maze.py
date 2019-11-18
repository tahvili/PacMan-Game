from constants import *
import pygame

class Maze:

    def __init__(self, sprite):

        self.sprite = sprite
        self.maze_info = None
        self.rotate_info  = None
        self.sprites = []
        self.s_row = 16
        self.get_maze_sprite()

    def get_maze_sprite(self):

        for i in range(10):
            self.sprites.append(self.sprite.get_sprite(i, self.s_row, WIDTH, HEIGHT))

    def rotate(self, sprite, val):
        return pygame.transform.rotate(sprite, val*90)

    def read_maze_file(self, textfile):
        """
        Get information from files
        """
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        return [line.split(' ') for line in lines]


    def get_maze(self, textfile):

        self.maze_info = self.read_maze_file(textfile+".txt")
        self.rotate_info = self.read_maze_file(textfile+"_rot.txt")

    def combine_maze(self, background):

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

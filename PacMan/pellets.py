import pygame
from typing import*
from vector import Vector2
from constants import *

class Pellets:

    def __init__(self, x, y):

        self.name = "pellets"
        self.color = YELLOW
        self.position = Vector2(x, y)
        self.radius = 4


    def render(self, screen):
        """
        draws pellets on screen,
        and also draws the pellets on screen
        """
        pos = self.position.to_tuple(True)
        pygame.draw.circle(screen, self.color, pos, self.radius)



class Power_Pellets(Pellets):

    def __init__(self, x, y):
        Pellets.__init__(self, x, y)
        self.name = "power pellets"
        self.color = YELLOW
        self.radius = 8



class Pellets_Group:

    def __init__(self, level):
        self.pellets_list = []
        self.pallets_symbols = ["p", "n"]
        self.power_pellets_symbols = ["N"]
        self.create_pellets_list(level)

    def read_maze_file(self, textfile):
        """
        Get information from files
        """
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        grid = [line.split(' ') for line in lines]
        return grid

    def create_pellets_list(self, textfile):
        """

        a list of pellets is created by adding the pellets and power pellets in
        bass on the position on the map

        """
        grid = self.read_maze_file(textfile)
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] in self.pallets_symbols:
                    self.pellets_list.append(Pellets(col * WIDTH, row * HEIGHT))
                if grid[row][col] in self.power_pellets_symbols:
                    self.pellets_list.append(Power_Pellets(col * WIDTH, row * HEIGHT))


    def render(self, screen):
        """
        the pellets are drawn 
        """
        for i in self.pellets_list:
            i.render(screen)















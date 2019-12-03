import pygame
from typing import*
from vector import Vector2
from constants import *

class Pellets:
    """
    This class represents the objects that PacMan collides with and score
    points.
    """
    def __init__(self, x: int, y: int) -> None:
        """
        Initialises the Pellets and sets its size, position, and points.
        """

        self.name = "pellets"
        self.color = WHITE
        self.position = Vector2(x, y)
        self.radius = 2
        self.points = 10

    def render(self, screen) -> None:
        """
        Draws pellets on screen.
        """
        pos = self.position.to_tuple(True)
        pos = (int(pos[0]+WIDTH/2), int(pos[1]+WIDTH/2))
        pygame.draw.circle(screen, self.color, pos, self.radius)



class Power_Pellets(Pellets):
    """
    This class inherits from Pellets and implements the special type of Pellet.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialises the Power_Pellets and sets its size, position, and points.
        """
        Pellets.__init__(self, x, y)
        self.name = "powerpellet"
        self.color = YELLOW
        self.radius = 8
        self.points = 50



class Pellets_Group:
    """
    This class defines a collection of pellet is form of a pellet group.
    """

    def __init__(self, level: int) -> None:
        """
        Initialises the Pellet Group and creates a pellet list.
        """
        self.pellets_list = []
        self.pallets_symbols = ["p", "n"]
        self.power_pellets_symbols = ["N", "P"]
        self.create_pellets_list(level)

    def read_maze_file(self, textfile: Any) -> Any:
        """
        Get information from the text file.
        """
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        grid = [line.split(' ') for line in lines]
        return grid

    def create_pellets_list(self, textfile: Any) -> None:
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

    def is_empty(self) -> bool:
        """
        Checks if the pellet list is empty.
        """
        return self.pellets_list == []

    def render(self, screen) -> None:
        """
        the pellets are drawn on the screen.
        """
        for i in self.pellets_list:
            i.render(screen)















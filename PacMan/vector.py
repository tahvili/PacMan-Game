from math import *
from typing import *


class Vector2:
    """
    Vectors are a data structure that's useful for storing information like position
    and velocity. A vector is something that describes both magnitude and direction.
    Both of those are necessary in describing a vector.

    """

    def __init__(self, x: int, y: int) -> None:
        """
        Intializer: we have an x and y which are the positions.
        """
        self.x, self.y = x, y

    def __str__(self) -> str:
        """
        This method just creates a printable version of our vector. It is very
         useful for debugging purposes.
        """
        return "<" + str(self.x) + ", " + str(self.y) + ">"

    def set(self, x: int) -> None:
        """

        It takes in x value of a position and updates it.
        """

        self.x += x

    def to_tuple(self, asints=False) -> Tuple[int, int]:

        """
        This method just converts our vector into a tuple.
        It becomes useful later on.
        This is really just a convenience method.
        We can force the x and y values to be ints if we set the asints variable to True.
        """
        if asints:
            return int(self.x), int(self.y)
        return self.x, self.y

    def magnitude(self) -> float:
        """
        gets the actual length of a vector, which requires a square root
        function.
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def magnitude_squared(self) -> int:
        """
        This is the same as magnitude, except it does not take the square root.
        This one is safer to use than the other magnitude method.

        """
        return self.x ** 2 + self.y ** 2

    """
    Magic methods, they are just good to have
    """
    def __add__(self, other) -> object:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> object:
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self) -> object:
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar) -> object:
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar) -> object:
        return Vector2(self.x / float(scalar), self.y / float(scalar))

    def __div__(self, scalar) -> object:
        return Vector2(self.x / float(scalar), self.y / float(scalar))

    def __eq__(self, other) -> object:
        if self.x == other.x and self.y == other.y:
            return True

        return False

    def __hash__(self) -> object:
        return id(self)

    def dot(self, other) -> int:
        """
        gets the dot product of two vectors
        """
        return self.x * other.x + self.y * other.y

    def normalize(self) -> object:
        """
        Turns our vector to a unit vector, with the length of 1.

        """
        mag = self.magnitude()

        if mag != 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(self.x, self.y)

    def copy(self) -> object:
        """
        This method creates an instance of another vector, very
        important for getting potential directions for pacman movement
        """
        return Vector2(self.x, self.y)


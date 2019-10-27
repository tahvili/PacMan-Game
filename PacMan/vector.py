from math import *

"""
Vectors are a data structure that's useful for storing information like position 
and velocity. A vector is something that describes both magnitude and direction. 
Both of those are necessary in describing a vector.

"""
class Vector2(object):

    def __init__(self, x, y):
        """
        Intializer, we have an x and y
        """
        self.x, self.y = x, y

    def __str__(self):
        """
        This method just creates a printable version of our vector. It is very useful for debugging purposes.
        """
        return "<" + str(self.x) + ", " + str(self.y) + ">"

    def to_tuple(self, asints=False):

        """
        This method just converts our vector into a tuple.
        It becomes useful later on.
        This is really just a convenience method.
        We can force the x and y values to be ints if we set the asints variable to True.
        """
        if asints:
            return int(self.x), int(self.y)
        return self.x, self.y

    def magnitude(self):
        """
        gets the actual length of a vector, which requires a square root
        function
        :return:
        """
        return sqrt(self.x ** 2 + self.y ** 2)

    def magnitude_squared(self):
        """
        This is the same as magnitude, except it does nottake the square root.
        I find this one safer to use than the other magnitude method
        :return:
        """
        return self.x ** 2 + self.y ** 2

    """
    Magic methods, they are just good to have
    """
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x / float(scalar), self.y / float(scalar))

    def __div__(self, scalar):
        return Vector2(self.x / float(scalar), self.y / float(scalar))

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True

        return False

    def __hash__(self):
        return id(self)

    def dot(self, other):
        """
        gets the dot product of two vectors
        """
        return self.x * other.x + self.y * other.y

    def normalize(self):
        """
        Turns our vector to a unit vector, with the length of 1.

        """
        mag = self.magnitude()

        if mag != 0:
            return Vector2(self.x / mag, self.y / mag)
        return Vector2(self.x, self.y)

    def copy(self):
        """
        This method creates an instance of another vector, very
        important for getting potential directions for pacman movement
        """
        return Vector2(self.x, self.y)

    def get_type(self, values):
        """
        This method takes the inputs and figures out how to parse it into the x
        and y values. If it can't parse the values, then it just returns a zero vector.

        """
        x, y = (0.0, 0.0)

        if len(values) == 1:
            if type(values[0]) is tuple or type(values[0]) is list:
                if len(values[0]) == 2:
                    x, y = self.set_values(values[0][0], values[0][1])
            elif len(values) == 2:
                x, y = self.set_values(values[0], values[1])
        return x, y

    def set_values(self, v1, v2):
        """
        Helper method for get_type
        """
        x, y = (0, 0)

        if type(v1) is int or type(v1) is float:
            x = float(v1)
        if type(v2) is int or type(v2) is float:
            y = float(v2)
        return x, y

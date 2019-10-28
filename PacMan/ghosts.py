import pygame
from entity import MazeRunner
from constants import *
from vector import Vector2
from random import *
from stack import Stack


class Ghost(MazeRunner):

    def __init__(self, nodes):
        """
        Initialize the ghost as a mazerunner
        """
        MazeRunner.__init__(self, nodes)
        self.name = "ghost"
        self.goal = Vector2(0, 0)
        self.modeStack = self.setup_mode_stack()
        self.mode = self.modeStack.pop()
        self.modetimer = 0

    def update(self, dt, pacman):
        """
        Like pacman, we are assessing the Ghost movement in each
        frame.
        """
        displacement = self.speed * self.mode.multiplier
        self.position += self.direction * displacement * dt
        self.update_mode(dt)
        if self.mode.name == "CHASE":
            self.chase(pacman)
        elif self.mode.name == "SCATTER":
            self.scatter()
        self.motion()

    def valid_directions(self):
        """
        This method will build a list of valid directions that
        the ghost can move in.
        """
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if key != self.direction * -1:
                    validDirections.append(key)
        if len(validDirections) == 0:
            validDirections.append(self.backtrack())
        return validDirections

    def rand_move(self, valid_directions):
        """
        This method will get the list of directions the ghost can move in by
        calling the previous method we just created. Once it has that list of
        directions, it will just simply randomly choose one of those directions.
        """
        move = randint(0, len(valid_directions) - 1)
        return valid_directions[move]

    def closest_direction(self, valid_directions):
        """
        What this method does is take the list of valid directions, and for each
        of the directions in the list it will calculate which direction will bring
        the ghost closer to its goal. That direction will be chosen instead of
        choosing a random direction. We find the best direction by calculating
        the line of sight distance from each direction and just choosing the
        direction with the shortest line of sight distance.
        """
        distances = []
        for direction in valid_directions:
            diffVec = self.node.position + direction * WIDTH - self.goal
            distances.append(diffVec.magnitude_squared())
        move = distances.index(min(distances))
        return valid_directions[move]

    def motion(self):
        """
        Similar to the motion method in the mazerunner class, except this \
        method except the ghost uses the valid moves method and randomly chooses
        a direction in the validdirections dictionary and moves in that directions
        """
        if self.overshot():
            self.node = self.target
            self.teleport()
            valid_directions = self.valid_directions()
            self.direction = self.closest_direction(valid_directions)
            self.target = self.node.neighbors[self.direction]
            self.set_position()

    def backtrack(self):
        """
        To make the Ghost go backwards in case of a dead end is reached
        this method is there to suppliment that movement
        """
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT

    def setup_mode_stack(self):
        """
        The Ghost has modes that randge for 20 seconds of chasing to
        5 seconsd og scattering from pacman to offere relief, this stack
        just sets all these modes up so when the game is ready we can run through
        them
        """
        modes = Stack()
        modes.push(Mode(name="CHASE"))
        modes.push(Mode(name="SCATTER", timer=5))
        modes.push(Mode(name="CHASE", timer=20))
        modes.push(Mode(name="SCATTER", timer=7))
        modes.push(Mode(name="CHASE", timer=20))
        modes.push(Mode(name="SCATTER", timer=7))
        modes.push(Mode(name="CHASE", timer=20))
        modes.push(Mode(name="SCATTER", timer=7))
        return modes

    def scatter(self):
        """
        This method tells the ghost what his goal is when he is in scatter mode.
        This should correspond to the top right of the screen.
        """
        self.goal = Vector2(SCREENSIZE[0], 0)

    def chase(self, pacman):
        """
        This method tells the ghost what his goal is when he is in chase mode.
        We are saying that his goal is Pacman's position.
        So wherever Pacman is, that's his goal he's trying to reach. This will
        make it look like the ghost is chasing Pacman.
        """
        self.goal = pacman.position

    def update_mode(self, dt):
        """
        This method  keeps track of the time that has passed, and
        then pop off the next Ghost mode when it needs to
        """
        self.modetimer += dt
        if self.mode.timer is not None:
            if self.modetimer >= self.mode.timer:
                self.mode = self.modeStack.pop()
                self.modetimer = 0

    def render(self, screen):
        """
        Draws the ghost the ghost on the screen
        """
        p = self.position.to_tuple(True)
        pygame.draw.circle(screen, self.color, p, self.radius)


class Mode:
    """
    This class takes care of the Ghost modes and, a timer for when they are
    active as well as their movement speed
    """
    def __init__(self, name="", timer=None, multiplier=1):
        self.name = name
        self.timer = timer
        self.multiplier = multiplier

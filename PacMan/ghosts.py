
import pygame
from entity import MazeRunner
from constants import *
from vector import Vector2
from random import *
from nodes import Node
from stack import Stack

class Ghost(MazeRunner):

    def __init__(self, nodes):
        MazeRunner.__init__(self, nodes)
        self.name = "ghost"
        self.goal = Vector2(0, 0)
        self.modeStack = self.setupModeStack()
        self.mode = self.modeStack.pop()
        self.modetimer = 0

    def update(self, dt, pacman):
        displacement  = self.speed * self.mode.multiplier
        self.position += self.direction*displacement*dt
        self.updateMode(dt)
        if self.mode.name == "CHASE":
            self.chase(pacman)
        elif self.mode.name == "SCATTER":
            self.scatter()
        self.motion()

    def validDirections(self):
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if key != self.direction * -1:
                    validDirections.append(key)
        if len(validDirections) == 0:
            validDirections.append(self.backtrack())
        return validDirections

    def randmove(self, validDirections):
        move = randint(0, len(validDirections) - 1)
        return validDirections[move]

    def closestDirection(self, validDirections):
        distances = []
        for direction in validDirections:
            diffVec = self.node.position + direction * WIDTH - self.goal
            distances.append(diffVec.magnitudeSquared())
        move = distances.index(min(distances))
        return validDirections[move]

    def motion(self):
        if self.overshot():
            self.node = self.target
            self.teleport()
            validDirections = self.validDirections()
            self.direction = self.closestDirection(validDirections)
            self.target = self.node.neighbors[self.direction]
            self.setPosition()

    def backtrack(self):
        if self.direction * -1 == UP:
            return UP
        if self.direction * -1 == DOWN:
            return DOWN
        if self.direction * -1 == LEFT:
            return LEFT
        if self.direction * -1 == RIGHT:
            return RIGHT

    def setupModeStack(self):
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
        self.goal = Vector2(SCREENSIZE[0], 0)

    def chase(self, pacman):
        self.goal = pacman.position

    def updateMode(self, dt):
        self.modetimer += dt
        if self.mode.timer is not None:
            if self.modetimer >= self.mode.timer:
                self.mode = self.modeStack.pop()
                self.modetimer = 0

    def render(self, screen):
        p = self.position.toTuple(True)
        pygame.draw.circle(screen, self.color, p, self.radius)


class Mode:

    def __init__(self, name="", timer=None, multiplier=1):
        self.name = name
        self.timer = timer
        self.multiplier = multiplier



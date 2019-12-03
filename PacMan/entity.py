
import pygame
from vector import Vector2
from constants import *
from random import *


class MazeRunner:
    def __init__(self, nodes, sprite):
        self.name = ""
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.collideRadius = 5
        self.color = WHITE
        self.nodes = nodes
        self.node = nodes.nodeList[0]
        self.target = self.node
        self.set_position()
        self.image = None
        self.sprite = sprite

    def set_position(self):
        """
        This method creates a node for pacman's position on screen
        for a simpler explanation, it just sets its position to a node
        wherever we decide.
        """
        self.position = self.node.position.copy()

    def update(self, dt):
        """
        Gets Pacman moving in a set direction, this method, is an overidden
        method per frame in the Game, so we always have the latest keypresses and
        checking if pacman can move in a direction or not.
        """
        self.position += self.direction * self.speed * dt
        self.motion()

    def motion(self):
        """
        Pacman largely moves by himself without any human intervention.
        This method is called when the user isn't pressing any keys
        telling him where to go. we check if pacman has stopped, if he hasn't
        then we check id he has overshot his target node, then we allow him to keep
        moving till he reaches his target that will make his stop, if he can still
        move in any direction, then we set his target to be the node that is in the
        direction that will make him stop, if this isn't the case then, pacman should
        top or have not movement, and set his postion on the nodegroup as such.
        """

        if self.direction is not STOP:
            if self.overshot():
                self.node = self.target
                self.teleport()
                if self.node.neighbors[self.direction] is not None:
                    self.target = self.node.neighbors[self.direction]
                else:
                    self.set_position()
                    self.direction = STOP

    def overshot(self):
        """
        This new method checks to see if Pacman has overshot the target node he is moving towards.
        If Pacman's distance is greater or equal to the distance between the two nodes,
        then we say that he has overshot the target node.
        returns true or false
        """
        if self.target is not None:
            postarget = self.target.position - self.node.position
            poscurrent = self.position - self.node.position
            # Use magnitude_squared because we are comparing distances, no need
            # for square root
            targetnode = postarget.magnitude_squared()
            currentnode = poscurrent.magnitude_squared()
            return currentnode >= targetnode
        return False

    def reverse(self):
        """
        Allows pacman to reverse his direction at anytime, if the direction
        pacman is reversing to is not a neighbor it wont allow it, though it is
        checked in this method.
        """
        if self.direction is UP:
            self.direction = DOWN
        elif self.direction is DOWN:
            self.direction = UP
        elif self.direction is LEFT:
            self.direction = RIGHT
        elif self.direction is RIGHT:
            self.direction = LEFT
        temp = self.node
        self.node = self.target
        self.target = temp


    def teleport(self):

        """
        If pacman reaches a portal, then it teleports to the other
        side of the screen(we set pacman's current node to the node on the
        other portal node on the screen)
        """
        if self.node.portals:
            self.node = self.node.portals
            self.set_position()

    def render(self, screen):
        if self.image is not None:
             pos = self.position.to_tuple()
             pos = (int(pos[0] - WIDTH / 2), int(pos[1] - WIDTH / 2))
             screen.blit(self.image, pos)


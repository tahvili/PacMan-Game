
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import MazeRunner


class Pacman(MazeRunner):
    """
    The Pacman Class, everything in the class pertains to the player character
    pacman. If you want to update something on pacman this is the class where you
    do it so that it affects the player character.
    """

    def __init__(self, nodes):

        MazeRunner.__init__(self, nodes)
        self.name = "pacman"
        self.color = YELLOW
        self.lives = 3
        self.startPosition()

    def decreaseLives(self):
        """
        This method check if the Pac-Mans lives are not 0, then it decreases it by 1, returning False and if its lives
        is 0, then it returns True.
        """
        if self.lives == 0:
            return True
        else:
            self.lives -= 1
            return False

    def start(self):
        """
        Sets the starting node for Pac-Man.
        """
        for node in self.nodes.nodeList:
            if node.start:
                return node

    def startPosition(self):
        """
        Sets Pac-Man start position in the beginning of the game.
        """
        pass

    def setPosition(self):
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
        direction = self.getKeyPressed()
        if direction:
            self.move(direction)
        else:
            self.motion()

    def getKeyPressed(self):
        """
        Look at the constants.py file

        We also check for key presses since we want to detect if the user is pressing the correct keys.
        If we detect that the user has pressed either the UP, DOWN, LEFT, or RIGHT keys
        then we call the move method and pass in the corresponding directions.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return None

    def teleport(self):
        """
        If pacman reaches a portal, then it teleports to the other
        side of the screen(we set pacman's current node to the node on the
        other portal node on the screen)
        """
        if self.node.portals:
            self.node = self.node.portals
            self.setPosition()

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
                    self.setPosition()
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
            # Use magnitudeSquared because we are comparing distances, no need
            # for square root
            targetnode = postarget.magnitudeSquared()
            currentnode = poscurrent.magnitudeSquared()
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

    def move(self, direction):
        """
        This is the movement method, there is a lot to be discussed here
        but I am not going to discuss it, as there is alot to explain, and nobody
        will need to use this hopefully.
        """
        if self.direction is STOP:
            if self.node.neighbors[direction] is not None:
                self.target = self.node.neighbors[direction]
                self.direction = direction
        else:
            if direction == self.direction * -1:
                self.reverse()
            if self.overshot():
                self.node = self.target
                self.teleport()
                if self.node.neighbors[direction] is not None:
                    self.target = self.node.neighbors[direction]
                    if self.direction != direction:
                        self.setPosition()
                        self.direction = direction
                else:
                    if self.node.neighbors[self.direction] is not STOP:
                        self.target = self.node.neighbors[self.direction]
                    else:
                        self.setPosition()
                        self.direction = STOP

    def render(self, screen):
        """
        draws pacman on screen, which at this point is just a yellow circle
        and also drws him based on his position on screen
        """
        pos = self.position.toTuple(True)
        pygame.draw.circle(screen, self.color, pos, self.radius)

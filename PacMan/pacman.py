
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import MazeRunner
from animation import Animation


class Pacman(MazeRunner):
    """
    The Pacman Class, everything in the class pertains to the player character
    pacman. If you want to update something on pacman this is the class where you
    do it so that it affects the player character.
    """

    def __init__(self, nodes, sprite):

        MazeRunner.__init__(self, nodes, sprite)
        self.name = "pacman"
        self.color = YELLOW
        self.lives = 3
        self.set_start_position()
        #self.image = sprite.get_sprite(0, 1, 32, 32)
        self.animation = None
        self.animations = {}
        self.define_animations()

    def decrease_lives(self):
        """
        This method check if the Pac-Mans lives are not 0, then it decreases it by 1, returning False and if its lives
        is 0, then it returns True.
        """
        if self.lives == 0:
            return True
        else:
            self.lives -= 1
            return False

    def set_start_position(self):
        """
        Sets the starting node for Pac-Man.
        """
        self.direction = LEFT
        self.node = self.get_start_node()
        self.target = self.node.neighbors[self.direction]
        self.set_position()
        #self.position.x -= (self.node.position.x - self.target.position.x) / 2

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
        direction = self.get_key_pressed()
        if direction:
            self.move(direction)
        else:
            self.motion()
        self.update_animation(dt)

    def get_key_pressed(self):
        """
        Look at the constants.py file

        We also check for key presses since we want to detect if the user is pressing the correct keys.
        If we detect that the user has pressed either the UP, DOWN, LEFT, or RIGHT keys
        then we call the move method and pass in the corresponding directions.
        """
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        elif key_pressed[K_DOWN]:
            return DOWN
        elif key_pressed[K_LEFT]:
            return LEFT
        elif key_pressed[K_RIGHT]:
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
            self.set_position()

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
                if self.direction != direction:
                    self.node = self.target
                self.node = self.target
                self.teleport()
                if self.node.neighbors[direction] is not None:
                    if self.node.restrict_entry:
                        if self.node.neighbors[self.direction] is not None:
                            self.target = self.node.neighbors[self.direction]
                        else:
                            self.set_position()
                            self.direction = STOP
                    else:
                        self.target = self.node.neighbors[direction]
                        if self.direction != direction:
                            self.set_position()
                            self.direction = direction
                else:
                    if self.node.neighbors[self.direction] is not STOP:
                        self.target = self.node.neighbors[self.direction]
                    else:
                        self.set_position()
                        self.direction = STOP

    # def render(self, screen):
    #     """
    #     draws pacman on screen, which at this point is just a yellow circle
    #     and also drws him based on his position on screen
    #     """
    #     pos = self.position.to_tuple(True)
    #     pygame.draw.circle(screen, self.color, pos, self.radius)

    def collide_pellets(self, pellet_list):
        """
        This methods search the whole board for all the  pellet and see if the
        pacman collided with any of them and then it returns that specific
        pellet.

        """
        for pellet in pellet_list:
            distance = self.position - pellet.position
            pac_distance = distance.magnitude_squared()
            pel_distance = (pellet.radius + self.collideRadius) ** 2
            if pac_distance <= pel_distance:
                return pellet
        return None

    def get_start_node(self):
        for node in self.nodes.nodeList:
            if node.pacman_start:
                return node
        return node

    def collide_ghost(self, ghosts):
        """
        This methods search the whole board for all the  pellet and see if the
        pacman collided with any of them and then it returns that specific
        pellet.

        """
        for ghost in ghosts:
            distance = self.position - ghost.position
            pac_distance = distance.magnitude_squared()
            ghost_distance = (ghost.collideRadius + ghost.collideRadius) ** 2
            if pac_distance <= ghost_distance:
                return ghost
        return None

    def update_animation(self, dt):
        if self.direction == UP:
            self.animation = self.animations["up"]
        elif self.direction == DOWN:
            self.animation = self.animations["down"]
        elif self.direction == LEFT:
            self.animation = self.animations["left"]
        elif self.direction == RIGHT:
            self.animation = self.animations["right"]
        elif self.direction == STOP:
            self.animation = self.animations["idle"]
        self.image = self.animation.get_frame(dt)

    def define_animations(self):
        anim = Animation("ping")

        anim.speed = 20
        anim.add_frame(self.sprite.get_sprite(4, 0, 32, 32))
        anim.add_frame(self.sprite.get_sprite(0, 0, 32, 32))
        anim.add_frame(self.sprite.get_sprite(0, 1, 32, 32))
        self.animations["left"] = anim

        anim = Animation("ping")
        anim.speed = 20
        anim.add_frame(self.sprite.get_sprite(4, 0, 32, 32))
        anim.add_frame(self.sprite.get_sprite(1, 0, 32, 32))
        anim.add_frame(self.sprite.get_sprite(1, 1, 32, 32))
        self.animations["right"] = anim

        anim = Animation("ping")
        anim.speed = 20
        anim.add_frame(self.sprite.get_sprite(4, 0, 32, 32))
        anim.add_frame(self.sprite.get_sprite(2, 0, 32, 32))
        anim.add_frame(self.sprite.get_sprite(2, 1, 32, 32))
        self.animations["down"] = anim

        anim = Animation("ping")
        anim.speed = 20
        anim.add_frame(self.sprite.get_sprite(4, 0, 32, 32))
        anim.add_frame(self.sprite.get_sprite(3, 0, 32, 32))
        anim.add_frame(self.sprite.get_sprite(3, 1, 32, 32))
        self.animations["up"] = anim

        anim = Animation("once")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(0, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(1, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(2, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(3, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(4, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(5, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(6, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(7, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(8, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(9, 7, 32, 32))
        anim.add_frame(self.sprite.get_sprite(10, 7, 32, 32))
        self.animations["death"] = anim

        anim = Animation("static")
        anim.add_frame(self.sprite.get_sprite(4, 0, 32, 32))
        self.animations["idle"] = anim

class LifeIcon:

    def __init__(self, spritesheet):
        self.width, self.height = 32, 32
        self.image = spritesheet.get_sprite(0, 1, self.width, self.height)
        self.gap = 10

    def render(self, screen, num):
        for i in range(num):
            x = self.gap + (self.width + self.gap) * i
            y = HEIGHT * ROWS - self.height
            screen.blit(self.image, (x, y))

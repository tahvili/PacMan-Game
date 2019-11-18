import pygame
from entity import MazeRunner
from constants import *
from vector import Vector2
from random import *
from stack import Stack
from animation import Animation


class Ghost(MazeRunner):

    def __init__(self, nodes, sprite):
        """
        Initialize the ghost as a mazerunner
        """
        MazeRunner.__init__(self, nodes, sprite)
        self.name = "ghost"
        self.goal = Vector2(0, 0)
        self.modeStack = self.setup_mode_stack()
        self.mode = self.modeStack.pop()
        self.modetimer = 0
        self.spawn = self.find_spawn()
        self.set_guide_stack()
        self.bad_direction = []
        self.set_start_position()
        self.escaped = True
        self.pellets_needed = 0
        self.animation  = None
        self.animations = {}

    def set_start_position(self):
        self.node = self.get_start_node()
        self.target = self.node
        self.set_position()

    def update(self, dt, pacman, blinky):
        """
        Like pacman, we are assessing the Ghost movement in each
        frame.
        """
        displacement = self.speed * self.mode.multiplier
        self.position += self.direction * displacement * dt
        self.update_mode(dt)
        if self.mode.name == "CHASE":
            self.chase(pacman, blinky)
        elif self.mode.name == "SCATTER":
            self.scatter()
        elif self.mode.name == "FEAR":
            self.flee()
        elif self.mode.name == "SPAWN":
            self.goto_spawn()
        self.motion()
        self.update_animation(dt)

    def valid_directions(self):
        """
        This method will build a list of valid directions that
        the ghost can move in.
        """
        validDirections = []
        for key in self.node.neighbors.keys():
            if self.node.neighbors[key] is not None:
                if key != self.direction * -1:
                    if not self.mode.name == "SPAWN":
                        if not self.node.homegrid:
                            if key not in self.bad_direction:
                                validDirections.append(key)
                        if not self.node.ghost_spawn:
                            validDirections.append(key)

                        else:
                            if key != DOWN:
                                validDirections.append(key)
                    else:
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

    def find_spawn(self):
        for node in self.nodes.homeList:
            if node.ghost_spawn:
                break
        return node

    def goto_spawn(self):
        self.goal = self.spawn.position

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
            if self.mode.name == "SPAWN":
                if self.position == self.goal:
                    self.mode = Mode("GUIDE", multiplier=0.5)
            if self.mode.name == "GUIDE":
                if self.guide.is_empty():
                    self.mode = self.modeStack.pop()
                    self.set_guide_stack()
                else:
                    self.direction = self.guide.pop()
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


    def engage_chase(self):
        if self.mode.name != "SPAWN":
            if self.mode.name != "FEAR":
                if self.mode.timer is not None:
                    dt = self.mode.time = self.modetimer
                    self.modeStack.push(Mode(name=self.mode.name, timer=dt))
                else:
                    self.modeStack.push(Mode(name=self.mode.name))
                self.mode = Mode("FEAR", timer=7, multiplier=0.5)
                self.modetimer = 0
            else:
                self.mode = Mode("FEAR", timer=7, multiplier=0.5)
                self.modetimer = 0

    def flee(self):
        x = randint(0, COLS*WIDTH)
        y = randint(0, ROWS*HEIGHT)
        self.goal = Vector2(x,y)

    def respawn(self):
        self.mode = Mode("SPAWN", multiplier=2)
        self.modetimer = 0

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

    def chase(self, pacman, blinky=None):
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

    def get_start_node(self):
        for node in self.nodes.homeList:
            if node.ghost_start:
                return node
            return node

    def set_guide_stack(self):
        self.guide = Stack()
        self.guide.push(UP)

    def define_animations(self, row):
        anim = Animation("loop")

        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(0, row, 32, 32))
        anim.add_frame(self.sprite.get_sprite(1, row, 32, 32))
        self.animations["up"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(2, row, 32, 32))
        anim.add_frame(self.sprite.get_sprite(3, row, 32, 32))
        self.animations["down"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(4, row, 32, 32))
        anim.add_frame(self.sprite.get_sprite(5, row, 32, 32))
        self.animations["left"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(6, row, 32, 32))
        anim.add_frame(self.sprite.get_sprite(7, row, 32, 32))
        self.animations["right"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(0, 6, 32, 32))
        anim.add_frame(self.sprite.get_sprite(1, 6, 32, 32))
        self.animations["fear"] = anim

        anim = Animation("loop")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(2, 6, 32, 32))
        anim.add_frame(self.sprite.get_sprite(3, 6, 32, 32))
        self.animations["flash"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(4, 6, 32, 32))
        self.animations["spawnup"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(5, 6, 32, 32))
        self.animations["spawndown"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(6, 6, 32, 32))
        self.animations["spawnleft"] = anim

        anim = Animation("static")
        anim.speed = 10
        anim.add_frame(self.sprite.get_sprite(7, 6, 32, 32))
        self.animations["spawnright"] = anim

    def update_animation(self, dt):
        if self.mode.name == "CHASE" or self.mode.name == "SCATTER":
            if self.direction == UP:
                self.animation = self.animations["up"]
            elif self.direction == DOWN:
                self.animation = self.animations["down"]
            elif self.direction == LEFT:
                self.animation = self.animations["left"]
            elif self.direction == RIGHT:
                self.animation = self.animations["right"]
        elif self.mode.name == "FEAR":
            self.animation = self.animations["fear"]
        elif self.mode.name == "SPAWN":
            if self.direction == UP:
                self.animation = self.animations["spawnup"]
            elif self.direction == DOWN:
                self.animation = self.animations["spawndown"]
            elif self.direction == LEFT:
                self.animation = self.animations["spawnleft"]
            elif self.direction == RIGHT:
                self.animation = self.animations["spawnright"]
        self.image = self.animation.get_frame(dt)

    # def render(self, screen):
    #     """
    #     Draws the ghost the ghost on the screen
    #     """
    #     p = self.position.to_tuple(True)
    #     pygame.draw.circle(screen, self.color, p, self.radius)


class Blinky(Ghost):

    def __init__(self, nodes, sprite):
        Ghost.__init__(self, nodes, sprite)
        self.define_animations(2)
        #self.image = self.sprite.get_sprite(0, 2, 32, 32)
        self.name = "blinky"
        self.color = RED


class Pinky(Ghost):

    def __init__(self, nodes, sprite):
        Ghost.__init__(self, nodes, sprite)
        self.define_animations(3)
        #self.image = self.sprite.get_sprite(0, 3, 32, 32)
        self.name = "pinky"
        self.color = PINK

    def scatter(self):
        self.goal = Vector2(0, 0)

    def chase(self, pacman, blinky=None):
        self.goal = pacman.position + pacman.direction * WIDTH * 4

    def set_start_position(self):
        start_node = self.get_start_node()
        self.node = start_node.neighbors[DOWN]
        self.target = self.node
        self.set_position()


class Inky(Ghost):

    def __init__(self, nodes, sprite):
        Ghost.__init__(self, nodes, sprite)
        self.define_animations(4)
        #self.image = self.sprite.get_sprite(0, 4, 32, 32)
        self.name = "inky"
        self.color = TEAL
        self.escaped = False
        self.pellets_needed = 20

    def scatter(self):
        self.goal = Vector2(WIDTH*COLS, HEIGHT*ROWS)

    def chase(self, pacman, blinky=None):
        vec1 = pacman.position + pacman.direction * WIDTH * 2
        vec2 = (vec1 - blinky.position) * 2
        self.goal = blinky.position + vec2

    def set_start_position(self):
        self.bad_direction = [RIGHT]
        start_node = self.get_start_node()
        pinky_node = start_node.neighbors[DOWN]
        self.node = pinky_node.neighbors[LEFT]
        self.target = self.node
        self.set_position()

class Clyde(Ghost):

    def __init__(self, nodes, sprite):
        Ghost.__init__(self, nodes, sprite)
        self.define_animations(5)
        #self.image = self.sprite.get_sprite(0, 5, 32, 32)
        self.name = "clyde"
        self.color = ORANGE
        self.escaped = False
        self.pellets_needed = 40

    def scatter(self):
        self.goal = Vector2(0, HEIGHT*ROWS)

    def chase(self, pacman, blinky=None):
        d = pacman.position - self.position
        ds = d.magnitude_squared()
        if ds <= (WIDTH*8)**2:
            self.scatter()
        else:
            self.goal = pacman.position + pacman.direction * WIDTH * 4

    def set_start_position(self):
        self.bad_direction = [LEFT]
        start_node = self.get_start_node()
        pinky_node = start_node.neighbors[DOWN]
        self.node = pinky_node.neighbors[RIGHT]
        self.target = self.node
        self.set_position()


class GhostGroup:

    def __init__(self, nodes, sprite):
        self.nodes = nodes
        self.ghosts = [Blinky(nodes, sprite), Pinky(nodes, sprite),Inky(nodes, sprite), Clyde(nodes, sprite)]

    def update(self, dt, pacman):
        for ghost in self.ghosts:
            ghost.update(dt, pacman, self.ghosts[0])

    def engage_chase(self):
        for ghost in self.ghosts:
            ghost.engage_chase()

    def escape(self, pellet_num):
        for ghost in self.ghosts:
            if not ghost.escaped:
                if pellet_num >= ghost.pellets_needed:
                    ghost.bad_direction = []
                    ghost.escaped = True

    def render(self, screen):
        for ghost in self.ghosts:
            ghost.render(screen)


class Mode:
    """
    This class takes care of the Ghost modes and, a timer for when they are
    active as well as their movement speed
    """
    def __init__(self, name="", timer=None, multiplier=1.0):
        self.name = name
        self.timer = timer
        self.multiplier = multiplier

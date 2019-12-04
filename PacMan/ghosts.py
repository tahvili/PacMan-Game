import pygame
from entity import MazeRunner
from constants import *
from vector import Vector2
from random import *
from stack import Stack
from animation import Animation
from typing import *


class Ghost(MazeRunner):

    def __init__(self, nodes: Any, sprite: Any):
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

    def set_start_position(self) -> None:
        """
        Sets the Ghost starting position on the game board
        :return:
        """
        self.node = self.get_start_node()
        self.target = self.node
        self.set_position()

    def update(self, dt: float, pacman: Any, blinky: Any) -> None:
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

    def valid_directions(self) -> Optional[Any]:
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

    def rand_move(self, valid_directions: Optional[Any]) -> Optional[Any]:
        """
        This method will get the list of directions the ghost can move in by
        calling the previous method we just created. Once it has that list of
        directions, it will just simply randomly choose one of those directions.
        """
        move = randint(0, len(valid_directions) - 1)
        return valid_directions[move]

    def closest_direction(self, valid_directions: Optional[Any]) -> Optional[Any]:
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

    def find_spawn(self) -> Any:
        """
        Finds the ghost home on the game board
        """
        for node in self.nodes.homeList:
            if node.ghost_spawn:
                break
        return node

    def goto_spawn(self) -> None:
        """
        sets the ghost's goal attribute to be the position
        in the ghost home
        """
        self.goal = self.spawn.position

    def motion(self) -> None:
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

    def backtrack(self) -> Any:
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


    def engage_chase(self) -> None:
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

    def flee(self) -> None:
        """
        Sets the ghost's goal attribute to the corners of the
        game board
        """
        x = randint(0, COLS*WIDTH)
        y = randint(0, ROWS*HEIGHT)
        self.goal = Vector2(x,y)

    def respawn(self) -> None:
        """
        Changes the ghosts state to the spawn state
        which sets to ghost to run the game board
        """
        self.mode = Mode("SPAWN", multiplier=2)
        self.modetimer = 0

    def setup_mode_stack(self) -> Any:
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

    def scatter(self) -> None:
        """
        This method tells the ghost what his goal is when he is in scatter mode.
        This should correspond to the top right of the screen.
        """
        self.goal = Vector2(SCREENSIZE[0], 0)

    def chase(self, pacman: Any, blinky=None) -> None:
        """
        This method tells the ghost what his goal is when he is in chase mode.
        We are saying that his goal is Pacman's position.
        So wherever Pacman is, that's his goal he's trying to reach. This will
        make it look like the ghost is chasing Pacman.
        """
        self.goal = pacman.position

    def update_mode(self, dt: float) -> None:
        """
        This method  keeps track of the time that has passed, and
        then pop off the next Ghost mode when it needs to
        """
        self.modetimer += dt
        if self.mode.timer is not None:
            if self.modetimer >= self.mode.timer:
                self.mode = self.modeStack.pop()
                self.modetimer = 0

    def get_start_node(self) -> Any:
        """
        Find the start node for the Ghost entity
        """
        for node in self.nodes.homeList:
            if node.ghost_start:
                return node
            return node

    def set_guide_stack(self) -> None:
        """
        adds the up direction to the guide stack
        """
        self.guide = Stack()
        self.guide.push(UP)

    def define_animations(self, row: int) -> None:
        """
        This method sets up the animation.
        """
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

    def update_animation(self, dt: int) -> None:
        """
        Updates ghost's animation
        """
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


class Blinky(Ghost):

    def __init__(self, nodes, sprite):
        """
        Initializer for the Blinky class
        """
        Ghost.__init__(self, nodes, sprite)
        self.define_animations(2)
        self.name = "blinky"
        self.color = RED


class Pinky(Ghost):

    def __init__(self, nodes: Any, sprite: Any) -> None:
        """
        Initializer for the Pinky class
        """
        Ghost.__init__(self, nodes, sprite)
        self.define_animations(3)
        self.name = "pinky"
        self.color = PINK

    def scatter(self) -> None:
        """
        Overridden method: sets the scatter figure to
        be the top left of the game board
        """
        self.goal = Vector2(0, 0)

    def chase(self, pacman: Any, blinky=None) -> None:
        """
        Overridden method: sets the chase figure to
        be a position in front of Pacman entity
        """
        self.goal = pacman.position + pacman.direction * WIDTH * 4

    def set_start_position(self) -> None:
        """
        Overriden method: defines characters starting position
        to be the middle of the ghost home
        """
        start_node = self.get_start_node()
        self.node = start_node.neighbors[DOWN]
        self.target = self.node
        self.set_position()


class Inky(Ghost):

    def __init__(self, nodes: Any, sprite: Any) -> None:
        """
        Initializer for the Inky class
        """
        Ghost.__init__(self, nodes, sprite)
        self.define_animations(4)
        self.name = "inky"
        self.color = TEAL
        self.escaped = False
        self.pellets_needed = 20

    def scatter(self) -> None:
        """
        Overridden method: sets the chase figure to
        the bottom right of the game board
        """
        self.goal = Vector2(WIDTH*COLS, HEIGHT*ROWS)

    def chase(self, pacman: Any, blinky=None) -> None:
        """
        Overridden method: sets the chase figure to
        the know both pacman's and blinky's position to
        be adjacent to their position.
        """
        vec1 = pacman.position + pacman.direction * WIDTH * 2
        vec2 = (vec1 - blinky.position) * 2
        self.goal = blinky.position + vec2

    def set_start_position(self) -> None:
        """
        Overridden method: sets Inky's correct starting position
        left of the ghost home
        """
        self.bad_direction = [RIGHT]
        start_node = self.get_start_node()
        pinky_node = start_node.neighbors[DOWN]
        self.node = pinky_node.neighbors[LEFT]
        self.target = self.node
        self.set_position()

class Clyde(Ghost):

    def __init__(self, nodes: Any, sprite: Any) -> None:
        """
        Initializer for the Clyde class
        """
        Ghost.__init__(self, nodes, sprite)
        self.define_animations(5)
        self.name = "clyde"
        self.color = ORANGE
        self.escaped = False
        self.pellets_needed = 40

    def scatter(self) -> None:
        """
        Overridden method: scatter figure is set
        to top right of the screen
        """
        self.goal = Vector2(0, HEIGHT*ROWS)

    def chase(self, pacman: Any, blinky=None) -> None:
        """
        Overridden method: Clyde chases pacman
        till he gets within 4 spaces of the character
        then he scatters
        """
        d = pacman.position - self.position
        ds = d.magnitude_squared()
        if ds <= (WIDTH*8)**2:
            self.scatter()
        else:
            self.goal = pacman.position + pacman.direction * WIDTH * 4

    def set_start_position(self) -> None:
        """
        Overridden method:
        Clyde's position is the right side of the
        ghost home
        """
        self.bad_direction = [LEFT]
        start_node = self.get_start_node()
        pinky_node = start_node.neighbors[DOWN]
        self.node = pinky_node.neighbors[RIGHT]
        self.target = self.node
        self.set_position()


class GhostGroup:

    """
    This class carries all the individual ghosts and their
    behaviours in a list so it is easier to add implentation
    for  all these ghosts at once

    see ==Main.py== for more uses
    """

    def __init__(self, nodes: Any, sprite: Any) -> None:
        """
        Initilaizer for the ghost group class
        """
        self.nodes = nodes
        self.ghosts = [Blinky(nodes, sprite), Pinky(nodes, sprite),Inky(nodes, sprite), Clyde(nodes, sprite)]

    def update(self, dt: int, pacman: Any) -> None:
        """
        Calls the update methos for every ghost in
        the ghosts list
        """
        for ghost in self.ghosts:
            ghost.update(dt, pacman, self.ghosts[0])

    def engage_chase(self) -> None:
        """
        Starts the chase for every ghost in the ghosts
        list
        """
        for ghost in self.ghosts:
            ghost.engage_chase()

    def escape(self, pellet_num) -> None:
        """
        This method allows special ghosts to exit
        the ghost home after Pacman has collected a certain amount
        of pellets aligning to the ghost's pellet needed attribute
        """
        for ghost in self.ghosts:
            if not ghost.escaped:
                if pellet_num >= ghost.pellets_needed:
                    ghost.bad_direction = []
                    ghost.escaped = True

    def render(self, screen) -> None:
        """
        Calls the render method for the ghosts
        in the ghosts list
        """
        for ghost in self.ghosts:
            ghost.render(screen)


class Mode:
    """
    This class takes care of the Ghost modes and, a timer for when they are
    active as well as their movement speed
    """
    def __init__(self, name="", timer=None, multiplier=1.0) -> None:
        """
        Initialzer for the Mode class
        """
        self.name = name
        self.timer = timer
        self.multiplier = multiplier

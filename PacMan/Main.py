import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman, LifeIcon
from nodes import NodeGroup
from ghosts import GhostGroup
from pellets import Pellets_Group
from sprites import Spritesheet
from maze import Maze
from welcome import Welcome


class GameController:
    """
    This the class that controls our basic game loop, what this method does
    is update what happens in game based on other events, and what just keeps
    game running until we end it
    """

    def __init__(self):
        pygame.init()
        self.nodes = None
        self.pacman = None
        self.ghosts = None
        self.game = None
        self.pellets_eaten = 0
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.background = None
        self.set_background()
        self.clock = pygame.time.Clock()

    def set_background(self):
        """
        We create a background and set it to the color BLACK that we defined in
        the constants.py file.
        """
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background.fill(BLACK)

    def start_game(self):

        self.sheet = Spritesheet()
        self.nodes = NodeGroup("maze.txt")
        self.pellets = Pellets_Group("maze.txt")
        self.pacman = Pacman(self.nodes, self.sheet)
        self.ghosts = GhostGroup(self.nodes, self.sheet)
        self.life_icons = LifeIcon(self.sheet)
        self.paused = False
        self.maze = Maze(self.sheet)
        self.maze.get_maze("maze")
        self.maze.combine_maze(self.background)

    def update(self):
        """
        The update method is a method that we call once per frame of the game.
        It's basically our game loop
        """
        dt = self.clock.tick(30) / 1000.0
        if not self.paused:
            self.pacman.update(dt)
            self.ghosts.update(dt, self.pacman)
        self.check_updater()
        self.render()

    def check_ghost_collision(self):
        self.ghosts.escape(self.pellets_eaten)
        ghost = self.pacman.collide_ghost(self.ghosts.ghosts)
        if ghost is not None:
            if ghost.mode.name == "FEAR":
                ghost.respawn()
            elif ghost.mode.name != "SPAWN":
                if self.pacman.lives == 0:
                    self.start_game()
                else:
                    self.pacman.lives -= 1
                    self.restart_level()

    def check_updater(self):
        """
        This method checks for certain events.
        Right now it is just checking to see when we exit out of the game.
        :return:
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.paused = not self.paused
        self.check_collision()
        self.check_ghost_collision()

    def render(self):
        """
        The render method is the method we'll use to draw the images to the screen.
        it uses the update method, it is consistently running until the
        window is closed, right now it just keeps drawing what we want on screen
        """

        self.screen.blit(self.background, (0, 0))
        #self.nodes.render(self.screen)
        self.pellets.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.life_icons.render(self.screen, self.pacman.lives-1)
        pygame.display.update()

    def check_collision(self):
        """
        This method finds the pellet collison and it has collided, it will
        remove that pellet from the pellet list and then it will also update
        the score accordingly.

        """
        self.paclives = self.pacman.lives
        pellete = self.pacman.collide_pellets(self.pellets.pellets_list)
        if pellete:
            self.pellets.pellets_list.remove(pellete)
            # self.pacman.get_score(pellete.points)
            self.pellets_eaten+=1
            if pellete.name == "powerpellet":
                self.pellets_eaten += 1
                self.ghosts.engage_chase()
            if self.pellets.is_empty():
                self.start_game()
                self.pacman.lives = self.paclives
        else:
            pass

    def restart_level(self):

        self.paused = True
        self.pacman.reset()
        self.ghosts = GhostGroup(self.nodes, self.sheet)


    def get_score(self, points):
        """
        Updates the score with given points and return the final score.

        """
        self.pacman.score += points
        return self.pacman.score

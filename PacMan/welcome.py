import pygame
from constants import *
from Main import *


class Welcome:
    """
    This is the class that controls our basic welcome page, what this method does
    is to ask the user to press the start button to start the game
    """

    def __init__(self):
        pygame.init()
        self.nodes = None
        self.pacman = None
        self.ghost = None
        self.screen = None
        self.background = None
        self.starter = GameController()
        self.starter.set_background()
        self.clock = pygame.time.Clock()

    def start(self):
        """
        This method will launch the welcome screen,
        and prompt the user to click on the start button to start the game
        """
        pygame.init()
        clock = pygame.time.Clock()
        fps = 60
        bg = [0, 0, 0]
        pygame.display.set_caption('PacMan by No Name')
        screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        font = pygame.font.Font('res/SfPixelateBold-vRK4.ttf', 14)
        text01 = font.render('Created by the brilliant', True, (255, 255, 255), (0,0,0))
        text02 = font.render(
            'minds of the group No Name',
            True, (255, 255, 255), (0, 0, 0))
        text03 = font.render(
            'Click on the yellow button bellow to start!',
            True, (255, 255, 255), (0, 0, 0))
        text04 = font.render(
            'Eat the dots, or be eaten by the ghosts!',
            True, (255, 255, 255), (0, 0, 0))

        IMAGE = pygame.image.load(r'res/ready.png').convert()  # or .convert_alpha()
        # Create a rect with the size of the image.
        rect = IMAGE.get_rect()
        rect.center = (224, 400)
        textRect01 = text01.get_rect()
        textRect01.center = (224, 230)
        textRect02 = text02.get_rect()
        textRect02.center = (224, 250)
        textRect03 = text03.get_rect()
        textRect03.center = (224, 270)
        textRect04 = text04.get_rect()
        textRect04.center = (224, 290)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if rect.collidepoint(mouse_pos):
                        self.starter.start_game()
                        while True:
                            self.starter.update()

            screen.fill(bg)
            screen.blit(pygame.image.load(r'res/title.png'), (0, 0))
            screen.blit(text01, textRect01)
            screen.blit(text02, textRect02)
            screen.blit(text03, textRect03)
            screen.blit(text04, textRect04)
            screen.blit(IMAGE, rect)
            pygame.display.update()
            clock.tick(fps)

if __name__ == "__main__":
    game = Welcome()
    game.start()

from abc import ABC, abstractmethod
import pygame
import constants


class View(ABC):
    """
    Handles the drawing of the game
    """
    def __init__(self, game):
        """
        Initializes the view

        Args:
            game: a Game to monitor the state of
        """
        self._game = game

    def setup(self):
        """
        Does any necessary setup for the view
        """
        return

    @abstractmethod
    def draw(self):
        """
        Draws the game based on current state
        """
        pass


class GraphicView(View):
    """
    Draws game in pygame graphic window
    """

    def __init__(self, game):
        super().__init__(game)
        self._screen = None

    def setup(self):
        """
        Sets up the pygame screen
        """
        pygame.init()
        self._screen = pygame.display.set_mode((constants.SCREEN_WIDTH,
                                                constants.SCREEN_HEIGHT))
        self._screen.fill((0, 0, 0))

    def draw(self):
        """
        Displays the current game state
        """
        self._screen.fill((0, 0, 0))
        for entity in self._game.all_sprites:
            self._screen.blit(entity.surf, entity.rect)
        pygame.display.flip()

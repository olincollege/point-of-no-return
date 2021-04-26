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

    def __init__(self, game, screen):
        """
        Initializes a graphical view

        Args:
            game: a Game, the game model to monitor
            screen: the Screen to display the graphics on
        """
        super().__init__(game)
        self._screen = screen

    def setup(self):
        """
        Sets up the pygame screen
        """
        self._screen.fill((0, 0, 255))

    def draw(self):
        """
        Displays the current game state
        """
        self._screen.fill((0, 0, 255))
        for entity in self._game.all_sprites:
            self._screen.blit(entity.surf, entity.rect)

        player_pos = self._game.player.rect.center
        light = pygame.Surface(constants.SCREEN_SIZE, pygame.SRCALPHA)
        light.fill((0, 0, 0, 0))
        pygame.draw.circle(light, (0, 0, 0, constants.LIGHT_DIFF), player_pos,
                           constants.LIGHT_SIZE)

        dark = pygame.Surface(constants.SCREEN_SIZE, pygame.SRCALPHA)
        dark.fill((0, 0, 0, constants.DARKNESS))

        dark.blit(light, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self._screen.blit(dark, (0, 0))

        pygame.display.flip()

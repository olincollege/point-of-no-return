from abc import ABC, abstractmethod
import pygame
import pygame_menu
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
        self._start_menu = pygame_menu.Menu('Point of No Return',
                                            constants.SCREEN_WIDTH,
                                            constants.SCREEN_HEIGHT,
                                            theme=constants.GAME_THEME)
        self._end_menu = pygame_menu.Menu('GAME OVER',
                                          constants.SCREEN_WIDTH,
                                          constants.SCREEN_HEIGHT,
                                          theme=constants.GAME_THEME)
        self._start_menu.add.button('Play', self.start_game)
        self._start_menu.add.button('Quit', pygame_menu.events.EXIT)
        self._end_menu.add.button('Restart', self.restart_game)
        self._end_menu.add.button('Quit', pygame_menu.events.EXIT)

    def setup(self):
        """
        Sets up the pygame screen
        """
        self._screen.fill((0, 0, 255))
        self._start_menu.mainloop(self._screen)

    def start_game(self):
        self._game.running = True
        self._start_menu.disable()

    def restart_game(self):
        self._game.restart()
        self._end_menu.disable()

    def draw(self):
        """
        Displays the current game state
        """
        self._screen.fill((255, 0, 0))

        if not self._game.running:
            self._end_menu.enable()
            self._end_menu.mainloop(self._screen)

        # Display all entities
        for entity in self._game.all_sprites:
            self._screen.blit(entity.surf, entity.rect)

        # Lighting circle around player
        player_pos = self._game.player.rect.topleft
        pos_offset = self._game.player.last_animation['positions']\
            [self._game.player.last_frame]
        player_pos = (player_pos[0] + pos_offset[0],
                      player_pos[1] + pos_offset[1])
        light = pygame.Surface(constants.SCREEN_SIZE, pygame.SRCALPHA)
        light.fill((0, 0, 0, 0))
        pygame.draw.circle(light, (0, 0, 0, constants.LIGHT_DIFF), player_pos,
                           constants.LIGHT_SIZE)

        dark = pygame.Surface(constants.SCREEN_SIZE, pygame.SRCALPHA)
        dark.fill((0, 0, 0, constants.DARKNESS))

        dark.blit(light, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        self._screen.blit(dark, (0, 0))

        # Health bar
        pygame.draw.rect(self._screen, constants.HEALTH_BAR_COLOR,
                         (constants.HEALTH_BAR_POS[0],
                          constants.HEALTH_BAR_POS[1],
                          constants.HEALTH_BAR_UNIT_WIDTH *
                          self._game.player.health,
                          constants.HEALTH_BAR_HEIGHT))

        pygame.display.flip()

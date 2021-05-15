"""
View classes for Point of No Return
"""
from abc import ABC, abstractmethod
import pygame
import pygame_menu
import src.constants as constants
import src.sprites as sprites
from src.utils import blit_alpha


class View(ABC):
    """
    Handles the drawing of the game

    Attributes:
        _game: the Game to display with this class
    """
    def __init__(self, game):
        """
        Initializes the view

        Args:
            game: a Game to monitor the state of
        """
        self._game = game

    @abstractmethod
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
        return


class GraphicView(View):
    """
    Draws game in pygame graphic window

    Attributes:
        _screen: a screen to display the game items on
        _start_menu: a pygame_menu with the start menu for the game
        _controls_menu: a pygame_menu to display the controls for the game
        _pause_menu: a pygame_menu that displays when paused
        _end_menu: a pygame_menu with the end menu for the game
        _sound_effects: a dict mapping actions (strings) to Sounds
        _flashlight: a Flashlight beam to draw on the screen
    """

    def __init__(self, game, screen):
        """
        Initializes a graphical view

        Args:
            game: a Game, the src model to monitor
            screen: the Screen to display the graphics on
        """
        super().__init__(game)
        self._screen = screen
        self._start_menu = pygame_menu.Menu('Point of No Return',
                                            constants.SCREEN_WIDTH,
                                            constants.SCREEN_HEIGHT,
                                            theme=constants.GAME_THEME)
        self._start_menu.add.button('Play', self.start_game)
        self._start_menu.add.button('Controls', self.controls_menu)
        self._start_menu.add.button('Quit', pygame_menu.events.EXIT)

        self._controls_menu = pygame_menu.Menu('CONTROLS',
                                               constants.SCREEN_WIDTH,
                                               constants.SCREEN_HEIGHT,
                                               theme=constants.GAME_THEME)
        self._controls_menu.add.label('Move: WASD').update_font({
            'color': constants.CONTROL_COLOR,
            'size': constants.CONTROL_SIZE})
        self._controls_menu.add.label('Attack: Arrow Keys').update_font({
            'color': constants.CONTROL_COLOR,
            'size': constants.CONTROL_SIZE})
        self._controls_menu.add.label('Attack Current Direction: Space')\
            .update_font({'color': constants.CONTROL_COLOR,
                          'size': constants.CONTROL_SIZE})
        self._controls_menu.add.label('Pause: Esc').update_font({
            'color': constants.CONTROL_COLOR,
            'size': constants.CONTROL_SIZE})
        self._controls_menu.add.button('Back', self.main_menu).update_font({
            'color': constants.CONTROL_COLOR,
            'size': constants.CONTROL_SIZE})

        self._end_menu = pygame_menu.Menu('GAME OVER',
                                          constants.SCREEN_WIDTH,
                                          constants.SCREEN_HEIGHT,
                                          theme=constants.GAME_THEME)
        self._end_menu.add.label(f'Score: {self._game.score}',
                                 label_id='score')\
            .update_font({'color': constants.SCORE_COLOR,
                          'size': constants.SCORE_SIZE})
        self._end_menu.add.button('Restart', self.restart_game)
        self._end_menu.add.button('Main  Menu', self.main_menu)

        self._pause_menu = pygame_menu.Menu('PAUSED',
                                            constants.SCREEN_WIDTH,
                                            constants.SCREEN_HEIGHT,
                                            theme=constants.GAME_THEME)
        self._pause_menu.add.button('Resume', self.unpause)
        self._pause_menu.add.button('Main  Menu', self.main_menu)
        pygame.mixer.music.load(
            f'{constants.AUDIO_FOLDER}/background_music.mp3')
        self._sound_effects = {
            'player_attack': pygame.mixer.Sound(
                f'{constants.AUDIO_FOLDER}/player_attack.wav'),
            'player_hit': pygame.mixer.Sound(
                f'{constants.AUDIO_FOLDER}/player_hit.wav'),
            'demon_hit': pygame.mixer.Sound(
                f'{constants.AUDIO_FOLDER}/demon_hit.wav')
        }
        self._flashlight = sprites.Flashlight(self._game)

    def setup(self):
        """
        Sets up the pygame screen by filling it and starting the start screen
        """
        self._screen.fill((0, 0, 255))
        self.main_menu()

    def main_menu(self):
        """
        Sets up start menu, resetting anything from the end menu
        """
        if not self._start_menu.is_enabled():
            self._game.restart()
            self._controls_menu.disable()
            self._pause_menu.disable()
            self._end_menu.disable()
            self._start_menu.enable()
            self._flashlight = sprites.Flashlight(self._game)
        pygame.mixer.music.play(-1)
        self._start_menu.mainloop(self._screen)

    def controls_menu(self):
        """
        Sets up the controls menu
        """
        self._start_menu.disable()
        self._controls_menu.enable()
        self._controls_menu.mainloop(self._screen)

    def start_game(self):
        """
        Start the game and disable the start menu
        """
        for _ in pygame.event.get():
            continue  # clear any spawn demon events
        self._game.running = True
        self._start_menu.disable()

    def restart_game(self):
        """
        Restart the game and disable the end menu
        """
        for _ in pygame.event.get():
            continue  # clear any spawn demon events
        self._game.restart()
        self._end_menu.disable()
        self._flashlight = sprites.Flashlight(self._game)

    def unpause(self):
        """
        Unpause the game and disable the pause menu
        """
        self._game.paused = False
        self._pause_menu.disable()

    def draw(self):
        """
        Displays the current game state
        """
        self._screen.fill((255, 0, 0))

        if self._game.paused:
            self._pause_menu.enable()
            self._pause_menu.mainloop(self._screen)

        if not self._game.player.alive():
            pygame.mixer.Sound.play(self._sound_effects['player_hit'])
            self._end_menu.enable()
            self._end_menu.get_widget('score')\
                .set_title(f'Score:  {self._game.score}')
            self._end_menu.mainloop(self._screen)

        # Display all entities
        for entity in self._game.all_sprites:
            if isinstance(entity, sprites.Demon) and entity.invincibility_time\
                    == constants.DEFAULT_INVINCIBILITY:
                pygame.mixer.Sound.play(self._sound_effects['demon_hit'])
            self._screen.blit(entity.surf, entity.rect)

        if self._game.player.invincibility_time ==\
                constants.DEFAULT_INVINCIBILITY:
            pygame.mixer.Sound.play(self._sound_effects['player_hit'])
        if self._game.player.attack_started:
            pygame.mixer.Sound.play(self._sound_effects['player_attack'])
        if self._game.demons_killed > 0:
            pygame.mixer.Sound.play(self._sound_effects['demon_hit'])

        # Lighting circle around player
        dark = pygame.Surface(constants.SCREEN_SIZE, pygame.SRCALPHA)
        dark.fill((0, 0, 0, constants.DARKNESS))

        flash_direction = self._game.player.current_direction
        flash_direction = (flash_direction[0], 0)
        self._flashlight.set_direction(flash_direction)
        self._flashlight.update()
        blit_alpha(dark, self._flashlight.surf, self._flashlight.rect.topleft,
                   constants.LIGHT_DIFF, special_flags=pygame.BLEND_RGBA_SUB)
        self._screen.blit(dark, (0, 0))

        # Health bar
        pygame.draw.rect(self._screen, constants.HEALTH_BAR_COLOR_1,
                         (constants.HEALTH_BAR_POS[0],
                          constants.HEALTH_BAR_POS[1],
                          constants.HEALTH_BAR_UNIT_WIDTH *
                          self._game.player.health,
                          constants.HEALTH_BAR_HEIGHT))
        if self._game.player.is_invincible:
            if (self._game.player.invincibility_time //
                    constants.TRANSPARENT_TIME) % 2 == 0:
                pygame.draw.rect(self._screen,
                                 constants.HEALTH_BAR_COLOR_1,
                                 (constants.HEALTH_BAR_POS[0]
                                  + constants.HEALTH_BAR_UNIT_WIDTH
                                  * self._game.player.health,
                                  constants.HEALTH_BAR_POS[1],
                                  constants.HEALTH_BAR_UNIT_WIDTH,
                                  constants.HEALTH_BAR_HEIGHT))
            else:
                pygame.draw.rect(self._screen,
                                 constants.HEALTH_BAR_COLOR_2,
                                 (constants.HEALTH_BAR_POS[0]
                                  + constants.HEALTH_BAR_UNIT_WIDTH
                                  * self._game.player.health,
                                  constants.HEALTH_BAR_POS[1],
                                  constants.HEALTH_BAR_UNIT_WIDTH,
                                  constants.HEALTH_BAR_HEIGHT))

        pygame.display.flip()

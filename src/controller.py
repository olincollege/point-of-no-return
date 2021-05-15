"""
Controllers for Point of No Return
"""
from abc import ABC, abstractmethod
import pygame
import src.constants as constants
from src.constants import MOVES
from src.sprites import Direction


class Controller(ABC):
    """
    Controls sprites in the game

    Attributes:
        _game: an instance of Game to update the state of
        _sprite: a Sprite or Sprite group to update with the controller
    """
    def __init__(self, game, sprite):
        """
        Initializes the controller

        Args:
            game: a Game to update the state of
            sprite: a Sprite or a Sprite group to update using the controller
        """
        self._game = game
        self._sprite = sprite

    @property
    def game(self):
        """
        Returns the game state
        """
        return self._game

    @property
    def sprite(self):
        """
        Returns the sprite for the controller
        """
        return self._sprite

    @abstractmethod
    def update(self):
        """
        Updates the game model based on player inputs
        """
        return


class PlayerController(Controller):
    """
    Controls the player with player input
    """
    def __init__(self, game):
        """
        Creates a Controller for the player

        Args:
            game: a Game containing the player to update with this controller
                and the game state to update
        """
        super().__init__(game, game.player)

    def update(self):
        """
        Updates the player state based on user keyboard input
        """
        pressed_keys = pygame.key.get_pressed()

        # If the sprite is attacking, lock the player's movement
        if self.sprite.is_attacking:
            self.sprite.set_direction((0, 0))
        else:
            if pressed_keys[MOVES['attack']]:
                self.sprite.attack()
            elif pressed_keys[MOVES['attack_up']]:
                self.sprite.attack(Direction.UP)
            elif pressed_keys[MOVES['attack_down']]:
                self.sprite.attack(Direction.DOWN)
            elif pressed_keys[MOVES['attack_left']]:
                self.sprite.attack(Direction.LEFT)
            elif pressed_keys[MOVES['attack_right']]:
                self.sprite.attack(Direction.RIGHT)
            else:
                direction = [pressed_keys[MOVES['right']]
                             - pressed_keys[MOVES['left']],
                             pressed_keys[MOVES['down']]
                             - pressed_keys[MOVES['up']]]
                if (direction[0] > 0 and self.sprite.rect.right >=
                    constants.SCREEN_WIDTH) or (direction[0] < 0 and
                                                self.sprite.rect.left <= 0):
                    direction[0] = 0

                if (direction[1] > 0 and self.sprite.rect.bottom >=
                    constants.SCREEN_HEIGHT) or (direction[1] < 0 and
                                                 self.sprite.rect.top <= 0):
                    direction[1] = 0

                self.sprite.set_direction((direction[0], direction[1]))
        self.sprite.update()


class DemonController(Controller):
    """
    Controls the demons
    """
    def __init__(self, game):
        """
        Creates a Controller for the demons

        Args:
            game: a Game containing the demon Sprite Group to update with this
                controller and the game state to update
        """
        super().__init__(game, game.demons)

    def update(self):
        """
        Updates the demon states to move towards the player
        """
        for demon in self.sprite:
            player_pos = self.game.player.rect.center
            direction = (player_pos[0] - demon.rect.centerx,
                         player_pos[1] - demon.rect.centery)
            dist = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            if dist == 0:
                continue
            scale = 1 / dist
            if self.game.player.is_invincible:
                scale *= constants.DEMON_SLOW_SCALE
            demon.set_direction((direction[0] * scale, direction[1] * scale))
            demon.update()


class ScrollController(Controller):
    """
    Controls all sprites to make the game scroll with player
    """
    def __init__(self, game):
        """
        Creates a Controller for all of the sprites

        Args:
            game: a Game containing the Sprites to update with this controller
                and the game state to update
        """
        super().__init__(game, game.all_sprites)

    def update(self):
        """
        Updates all sprite positions to scroll as the player moves vertically
        """
        for entity in self.sprite:
            entity.move((0, -self.game.player.current_direction[1]
                         * self.game.player.frame_speed))
        for obs in self.game.obstacles:
            obs.update()

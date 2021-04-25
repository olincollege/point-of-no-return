from abc import ABC, abstractmethod
import pygame
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
)
import constants
from sprites import Player


class Controller(ABC):
    """
    Controls sprites
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
        pass


class PlayerController(Controller):
    """
    Controls the player with player input
    """

    def update(self):
        """
        Updates the player state
        """

        pressed_keys = pygame.key.get_pressed()
        direction = [pressed_keys[K_RIGHT] - pressed_keys[K_LEFT],
                     pressed_keys[K_DOWN] - pressed_keys[K_UP]]
        if (direction[0] > 0 and self.sprite.rect.right >=
            constants.SCREEN_WIDTH) or (direction[0] < 0 and
                                        self.sprite.rect.left <= 0):
            direction[0] = 0

        if (direction[1] > 0 and self.sprite.rect.bottom >=
            constants.SCREEN_HEIGHT) or (direction[1] < 0 and
                                         self.sprite.rect.top <= 0):
            direction[1] = 0

        self.sprite.update((direction[0], direction[1]))


class DemonController(Controller):
    """
    Controls the demons
    """

    def update(self):
        """
        Updates the demon states
        """
        for demon in self.sprite:
            player_pos = self.game.player.rect.center
            direction = (player_pos[0] - demon.rect.centerx,
                         player_pos[1] - demon.rect.centery)
            dist = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            demon.update((direction[0] / dist, direction[1] / dist))


class ScrollController(Controller):
    """
    Controls all sprites to make the game scroll with player
    """

    def update(self):
        """
        Updates all sprite positions
        """
        for entity in self.sprite:
            if not isinstance(entity, Player):
                entity.move((0, -self.game.player.current_direction[1]
                             * self.game.player.frame_speed))

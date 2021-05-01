from abc import ABC, abstractmethod
import pygame
import constants
from constants import MOVES


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
    def __init__(self, game):
        super().__init__(game, game.player)

    def update(self):
        """
        Updates the player state
        """
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[MOVES['attack']] and not self.sprite.is_attacking:
            self.sprite.attack()

        if self.sprite.is_attacking:
            self.sprite.update((0, 0))
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

            self.sprite.update((direction[0], direction[1]))


class DemonController(Controller):
    """
    Controls the demons
    """
    def __init__(self, game):
        super().__init__(game, game.demons)

    def update(self):
        """
        Updates the demon states
        """
        for demon in self.sprite:
            player_pos = self.game.player.rect.center
            direction = (player_pos[0] - demon.rect.centerx,
                         player_pos[1] - demon.rect.centery)
            dist = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            if dist == 0:
                continue
            demon.update((direction[0] / dist, direction[1] / dist))


class ScrollController(Controller):
    """
    Controls all sprites to make the game scroll with player
    """
    def __init__(self, game):
        super().__init__(game, game.all_sprites)

    def update(self):
        """
        Updates all sprite positions
        """
        for entity in self.sprite:
            entity.move((0, -self.game.player.current_direction[1]
                         * self.game.player.frame_speed))
        for obs in self.game.obstacles:
            obs.update()

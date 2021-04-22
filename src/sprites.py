import pygame
from pygame.sprite import Sprite
import consants


class Character(Sprite):
    """
    A abstract class to represent a basic character

    Attributes:
        _speed: maximum speed in pixels per second
    """
    def __init__(self, speed, image_path=None, transparent=(0, 0, 0)):
        """
        Initializes the character by setting surf and rect, and setting the
        given image.

        Args:
            speed: int, the max character speed in pixels/second
            image_path: string giving the path to the character art. Defaults
                to None, which will set a white 50x50 square
            transparent: tuple of 3 ints giving the color (RGB) to make
                transparent. Defaults to black.
        """
        super().__init__()
        if image_path is None:
            self.surf = pygame.Surface((50, 50))
            self.surf.fill((255, 255, 255))
        else:
            self.surf = pygame.image.load(image_path).convert()
            self.surf.set_colorkey(transparent, pygame.RLEACCEL)
        self.rect = self.surf.get_rect()
        self._speed = speed

    @property
    def speed(self):
        return self._speed

    @property
    def frame_speed(self):
        return self._speed / consants.FRAME_RATE

    def update(self, direction):
        """
        Updates the character's current position

        Args:
            direction: tuple of 2 floats from -1 to 1, x/y coordinates of
                target speed as percentage of max
        """
        self.rect.move_ip(direction[0] * self.frame_speed,
                          direction[1] * self.frame_speed)


class Player(Character):
    """
    A sprite for the player
    """
    def __init__(self):
        """
        Initializes the player
        """
        super().__init__(consants.PLAYER_SPEED)


class Demon(Character):
    """
    A sprite for all the enemies
    """
    def __init__(self):
        """
        Initializes the demon
        """
        super().__init__(consants.DEMON_SPEED)

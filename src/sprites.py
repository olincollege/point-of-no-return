"""
Sprites in **INSERT TITLE**
"""

import os
import pygame
from pygame.sprite import Sprite
from math import atan2
import constants


class GameSprite(Sprite):
    """
    A sprite class to represent any basic objects and characters

    Attributes:
        _animations: a dictionary with animation sequence names as keys and
            lists of images representing each sequence as values
        _animation_frame: an int, the current frame of the animation
        _current_animation: a string, the current animation sequence
        _frame_length: a float, the number of game frames each animation frame
            runs
    """
    def __init__(self, fps, spawn_pos=None, image_path=None):
        """
        Initializes the character by setting surf and rect, and setting the
        given image.

        Args:
            fps: a float, how many animation frames to do each second
            spawn_pos: tuple of 2 ints, where to spawn this character, defaults
                to top left
            image_path: string giving the path to the character art. Defaults
                to None, which will set a white 50x50 square
        """
        super().__init__()
        self._frame_length = constants.FRAME_RATE / fps
        if image_path is None:
            self.surf = pygame.Surface((50, 50))
            self.surf.fill((255, 255, 255))
        else:
            self._animations = {'stills': []}
            counter = 0
            while(os.access(f'../media/images/{image_path}/{counter}.png',
                            os.F_OK)):
                self._animations['stills'].append(pygame.image.load(
                    f'../media/images/{image_path}/{counter}.png')
                                                  .convert_alpha())
                counter += 1
            self.surf = self._animations['stills'][0]
        self._animation_frame = 0
        self._current_animation = 'stills'

        if spawn_pos is None:
            self.rect = self.surf.get_rect(center=(constants.SCREEN_WIDTH/2,
                                                   constants.SCREEN_HEIGHT/2))
        else:
            self.rect = self.surf.get_rect(center=spawn_pos)

    @property
    def current_animation(self):
        return self._current_animation

    def update(self):
        """
        Updates the character's current animation and does any other necessary
        changes to the character's state.
        """
        self._animation_frame += 1
        self._animation_frame %= len(self._animations[self._current_animation])\
            * self._frame_length
        self.surf = self._animations[self.current_animation]\
            [int(self._animation_frame // self._frame_length)]

    def move(self, delta_pos):
        """
        Moves the sprite's current position a certain number of pixels

        Args:
            delta_pos: tuple of 2 ints, x/y number of pixels to move
        """
        self.rect.move_ip(delta_pos[0], delta_pos[1])


class Character(Sprite):
    """
    A sprite class to represent a basic character

    Attributes:
        _speed: maximum speed in pixels per second
    """
    def __init__(self, speed, spawn_pos=None, image_path=None,
                 transparent=(0, 0, 0)):
        """
        Initializes the character by setting surf and rect, and setting the
        given image.

        Args:
            speed: int, the max character speed in pixels/second
            spawn_pos: tuple of 2 ints, where to spawn this character, defaults
                to top left
            image_path: string giving the path to the character art. Defaults
                to None, which will set a white 50x50 square
            transparent: tuple of 3 ints giving the color (RGB) to make
                transparent. Defaults to black.
        """
        super().__init__()
        if image_path is None:
            self.surf = pygame.Surface((50, 50))
            # Just to see difference, make Demons red
            if isinstance(self, Demon):
                self.surf.fill((255, 0, 0))
            else:
                self.surf.fill((255, 255, 255))
        else:
            self.surf = pygame.image.load(image_path).convert()
            self.surf.set_colorkey(transparent, pygame.RLEACCEL)

        if spawn_pos is None:
            self.rect = self.surf.get_rect(center=(constants.SCREEN_WIDTH/2,
                                                   constants.SCREEN_HEIGHT/2))
        else:
            self.rect = self.surf.get_rect(center=spawn_pos)
        self._speed = speed

    @property
    def speed(self):
        return self._speed

    @property
    def frame_speed(self):
        return self._speed / constants.FRAME_RATE

    def update(self, direction):
        """
        Updates the character's current position and does any other necessary
        changes to the character's state.

        Args:
            direction: tuple of 2 floats from -1 to 1, x/y coordinates of
                target speed as percentage of max
        """
        self.move((direction[0] * self.frame_speed,
                   direction[1] * self.frame_speed))

    def move(self, delta_pos):
        """
        Moves the character's current position a certain number of pixels

        Args:
            delta_pos: tuple of 2 ints, x/y number of pixels to move
        """
        self.rect.move_ip(delta_pos[0], delta_pos[1])


class Player(Character):
    """
    A sprite for the player
    """
    def __init__(self):
        """
        Initializes the player
        """
        super().__init__(constants.PLAYER_SPEED)
        self._current_direction = (0, 0)

    @property
    def current_direction(self):
        """
        Returns the direction the player is currently traveling
        """
        return self._current_direction

    @property
    def current_angle(self):
        """
        Returns the angle the player is currently facing
        """
        return atan2(self._current_direction[1], self._current_direction[0])

    def update(self, direction):
        super().update((direction[0], 0))
        self._current_direction = direction


class Demon(Character):
    """
    A sprite for all the enemies
    """
    def __init__(self, spawn_pos=None):
        """
        Initializes the demon

        Args:
            spawn_pos: a tuple of 2 ints, where to spawn the demon, defaults
                to top left
        """
        super().__init__(constants.DEMON_SPEED, spawn_pos)


class Obstacle(GameSprite):
    """
    A sprite for game obstacles
    """
    def __init__(self, spawn_pos=None):
        """
        Initializes the obstacle

        Args:
            spawn_pos: a tuple of 2 ints, where to spawn the demon, defaults
                to top left
        """
        super().__init__(4, spawn_pos, 'obstacle')

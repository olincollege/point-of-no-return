"""
Sprites in **INSERT TITLE**
"""

from datetime import datetime
from enum import Enum
import json
import os
import pygame
from pygame.sprite import Sprite
from math import atan2, pi
import constants
import utils


class Direction(Enum):
    """
    An enum that represents the four directions. Evaluated to a tuple of two
    ints, which is the direction on a -1 to 1 scale in x-y coordinates
    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __repr__(self):
        if self == Direction.UP:
            return "up"
        if self == Direction.DOWN:
            return "down"
        if self == Direction.LEFT:
            return "left"
        if self == Direction.RIGHT:
            return "right"


class GameSprite(Sprite):
    """
    A sprite class to represent any basic objects and characters

    Attributes:
        _animations: a dictionary with animation sequence names as keys and
            lists of images representing each sequence as values
        _animation_frame: an int, the current frame of the animation
    """
    def __init__(self, fps, image_path, spawn_pos=None):
        """
        Initializes the character by setting surf and rect, and setting the
        given image.

        Args:
            fps: a float, how many animation frames to do each second
            image_path: string giving the path to the character art
            spawn_pos: tuple of 2 ints, where to spawn this character, defaults
                to top left
        """
        super().__init__()
        # Creates animations dictionary and a key for the still images
        self._animations = {'stills': utils.get_animation_info(
            f'../media/images/{image_path}')}
        # Sets current character image to the first still
        self.surf = self._animations['stills']['animations'][0]
        self._animation_frame = 0
        # Default spawn position is the center of the screen
        if spawn_pos is None:
            self.rect = self.surf.get_rect(center=(constants.SCREEN_WIDTH/2,
                                                   constants.SCREEN_HEIGHT/2))
        else:
            self.rect = self.surf.get_rect(center=spawn_pos)

    @property
    def current_animation(self):
        """
        Returns the current animation type for the character
        """
        return self._animations['stills']

    def update(self):
        """
        Updates the character's current animation and does any other necessary
        changes to the character's state.
        """
        if self._animation_frame >= len(self.current_animation['animations'])\
                * self.current_animation['frame_length']:
            self._animation_frame = 0
        self.surf = self.current_animation['animations'][int(
            self._animation_frame // self.current_animation['frame_length'])]
        self._animation_frame += 1

    def move(self, delta_pos):
        """
        Moves the sprite's current position a certain number of pixels

        Args:
            delta_pos: tuple of 2 ints, x/y number of pixels to move
        """
        self.rect.move_ip(delta_pos[0], delta_pos[1])


class MovingSprite(GameSprite):
    """
    A sprite class to represent a basic character that can move

    Attributes:
        _speed: maximum speed in pixels per second
        _current_direction: a tuple of two floats, the last direction this
            sprite moved, on a -1 to 1 scale relative to _speed and ignoring
            motion of the screen
        _current_facing: a Direction (Up, Down, Left, Right), which way this
            sprite is currently facing
    """
    def __init__(self, speed, fps, image_path, spawn_pos=None):
        """
        Initializes the character by setting surf and rect, and setting the
        animation frame images.

        Args:
            speed: int, the max character speed in pixels/second
            fps: a float, how many animation frames to do each second
            spawn_pos: tuple of 2 ints, where to spawn this character, defaults
                to top left
            image_path: string giving the path to the character art
        """
        super().__init__(fps, image_path, spawn_pos)
        # Add the images for the other animation types to the animations
        # dictionary
        path = f'{constants.IMAGE_FOLDER}/{image_path}'
        for direction in ("up", "down", "left", "right"):
            self._animations[direction] = utils.get_animation_info(
                f'{path}/{direction}')
            still = f'still_{direction}'
            self._animations[still] = {}
            self._animations[still]['animations'] =\
                self._animations[direction]['animations'][0:1]
            self._animations[still]['frame_length'] =\
                self._animations[direction]['frame_length']
            self._animations[still]['positions'] =\
                self._animations[direction]['positions'][0:1]
        self._speed = speed
        self._current_direction = (0, 0)
        self._current_facing = Direction.UP

    @property
    def speed(self):
        """
        Returns the speed in pixels per second
        """
        return self._speed

    @property
    def frame_speed(self):
        """
        Returns the pixels per frame speed
        """
        return self._speed / constants.FRAME_RATE

    @property
    def current_direction(self):
        """
        Returns the last direction the sprite faced as a tuple from -1 to 1
        """
        return self._current_direction

    @property
    def current_angle(self):
        """
        Returns the angle the player is currently facing in degrees
        """
        return atan2(self._current_direction[1], self._current_direction[0])\
            * 180 / pi

    @property
    def current_facing(self):
        """
        Returns the current Direction facing of the sprite
        """
        return self._current_facing

    @property
    def current_animation(self):
        """
        Returns the current animation type of the sprite
        """
        if self._current_direction == (0, 0):
            return self._animations[f'still_{repr(self.current_facing)}']
        angle = self.current_angle
        if -45 <= angle <= 45:
            self._current_facing = Direction.RIGHT
        elif 45 < angle < 135:
            self._current_facing = Direction.DOWN
        elif -135 < angle < -45:
            self._current_facing = Direction.UP
        elif abs(angle) >= 135:
            self._current_facing = Direction.LEFT
        return self._animations[repr(self.current_facing)]

    def update(self, direction):
        """
        Updates the character's current position and animation.

        Args:
            direction: tuple of 2 floats from -1 to 1, x/y coordinates of
                target speed as percentage of max
        """
        self._current_direction = direction
        super().update()
        self.move((direction[0] * self.frame_speed,
                   direction[1] * self.frame_speed))

    def move(self, delta_pos):
        """
        Moves the character's current position a certain number of pixels

        Args:
            delta_pos: tuple of 2 ints, x/y number of pixels to move
        """
        self.rect.move_ip(delta_pos[0], delta_pos[1])


class AttackingSprite(MovingSprite):
    """
    A sprite for a character that can attack

    Attributes:
        _attacking: a boolean, True if the sprite is currently attacking and
            False if not
    """
    def __init__(self, speed, fps, image_path, spawn_pos=None):
        """
        Initializes the character by setting surf and rect, and setting the
        animation images.

        Args:
            speed: int, the max character speed in pixels/second
            fps: a float, how many animation frames to do each second
            spawn_pos: tuple of 2 ints, where to spawn this character, defaults
                to top left
            image_path: string giving the path to the character art. Defaults
                to None, which will set a white 50x50 square
        """
        super().__init__(speed, fps, image_path, spawn_pos)
        path = f'{constants.IMAGE_FOLDER}/{image_path}'
        for animation in ("attack_up", "attack_down", "attack_left",
                          "attack_right"):
            self._animations[animation] = utils.get_animation_info(
                f'{path}/{animation}')
        self._attacking = False

    @property
    def is_attacking(self):
        return self._attacking

    @property
    def current_animation(self):
        if self.is_attacking:
            return self._animations[f'attack_{repr(self.current_facing)}']
        return super().current_animation

    def attack(self):
        self._attacking = True
        self._animation_frame = 0

    def update(self, direction):
        super().update(direction)
        if self._attacking and self._animation_frame == len(
                    self.current_animation['animations']) * int(
                    self.current_animation['frame_length']):
            self._attacking = False


class Player(AttackingSprite):
    """
    A sprite for the player
    """
    def __init__(self):
        """
        Initializes the player
        """
        super().__init__(constants.PLAYER_SPEED, constants.PLAYER_FPS,
                         'player', None)


class Demon(MovingSprite):
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
        super().__init__(constants.DEMON_SPEED, constants.DEMON_FPS,
                         'demon', spawn_pos)


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
        super().__init__(4, 'obstacle', spawn_pos)

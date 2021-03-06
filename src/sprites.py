"""
Sprites in Point of No Return
"""
from enum import Enum
from math import atan2, pi
import pygame
from pygame.sprite import Sprite
import src.constants as constants
import src.utils as utils


class Direction(Enum):
    """
    An enum that represents the four directions. Evaluated to a tuple of two
    ints, which is the direction on a -1 to 1 scale in x-y coordinates
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    def __repr__(self):
        if self == Direction.UP:
            return "up"
        if self == Direction.DOWN:
            return "down"
        if self == Direction.LEFT:
            return "left"
        if self == Direction.RIGHT:
            return "right"
        return None


class GameSprite(Sprite):  # pylint: disable=too-many-instance-attributes
    """
    A sprite class to represent any basic objects and characters

    Attributes:
        surf: a pygame surface, the display image for the sprite
        rect: a pygame rectangle, defines the position of the sprite
        mask: a pygame mask, defines the hit-box for the sprite from the surf
        _spawn_pos: a tuple of two ints, the spawn position of the sprite
        _animations: a dictionary with animation sequence names as keys and
            dictionaries with the information for each animation sequence
            (images, center positions, animation frame rate)
        _animation_frame: an int, the current frame of the animation
        _layer: an int, the layer to display the sprite on
        _last_animation: a tuple, first element is the animation dict from
            _animations, second element is the frame of that animation
        _game: a Game that contains all the sprites
    """
    def __init__(self, game, image_path, spawn_pos=None):
        """
        Initializes the character by setting surf and rect, and setting the
        given image.

        Args:
            game: a Game that holds all the sprites
            image_path: string giving the path to the character art
            spawn_pos: tuple of 2 ints, where to spawn this character, defaults
                to the center of the screen
        """
        super().__init__()
        # Creates animations dictionary and a key for the still images
        self._animations = {'stills': utils.get_animation_info(
            f'{constants.IMAGE_FOLDER}/{image_path}')}
        # Sets current character image to the first still
        self.surf = self._animations['stills']['animations'][0]
        self._animation_frame = 0
        # Default spawn position is the center of the screen
        if spawn_pos is None:
            self.rect = self.surf.get_rect(center=(constants.SCREEN_WIDTH / 2,
                                                   constants.SCREEN_HEIGHT / 2))
            self._spawn_pos = (constants.SCREEN_WIDTH / 2,
                               constants.SCREEN_HEIGHT / 2)
        else:
            self.rect = self.surf.get_rect(center=spawn_pos)
            self._spawn_pos = spawn_pos
        self.mask = pygame.mask.from_surface(self.surf)
        self._last_animation = (self._animations["stills"], 0)
        self._layer = self.rect.bottom
        self._game = game

    @property
    def layer(self):
        """
        Returns the display layer for the sprite
        """
        return self._layer

    @property
    def current_animation_name(self):
        """
        Returns the name of the current animation
        """
        return 'stills'

    @property
    def current_animation(self):
        """
        Returns the current animation type for the sprite
        """
        return self._animations[self.current_animation_name]

    @property
    def last_animation(self):
        """
        Returns a dictionary of all the information for the last animation
        """
        return self._last_animation[0]

    @property
    def last_frame(self):
        """
        Returns the frame number the last animation was on
        """
        return self._last_animation[1]

    def reset(self):
        """
        Reset the sprite attributes
        """
        self.rect.center = self._spawn_pos

    def update(self, *args, **kwargs):
        """
        Updates the character's current animation and does any other necessary
        changes to the character's state.
        """
        if self._animation_frame >= len(self.current_animation['animations'])\
                * self.current_animation['frame_length']:
            self._animation_frame = 0

        last_surf = self.surf
        frame = int(self._animation_frame
                    // self.current_animation['frame_length'])
        self.surf = self.current_animation['animations'][frame]
        if last_surf != self.surf:
            self.mask = pygame.mask.from_surface(self.surf)

        last_pos = self._last_animation[0]['positions'][self._last_animation[1]]
        current_pos = self.current_animation['positions'][frame]
        delta = (last_pos[0] - current_pos[0], last_pos[1] - current_pos[1])
        self.move(delta)

        self._animation_frame += 1
        self._last_animation = (self.current_animation, frame)

    def move(self, delta_pos):
        """
        Moves the sprite's current position a certain number of pixels

        Args:
            delta_pos: tuple of 2 ints, x/y number of pixels to move
        """
        self.rect.move_ip(int(delta_pos[0]), int(delta_pos[1]))
        self._layer = self.rect.bottom


class MovingSprite(GameSprite):
    """
    A sprite class to represent a basic character/object that can move

    Attributes:
        _speed: maximum speed in pixels per second
        _current_direction: a tuple of two floats, the last direction this
            sprite moved, on a -1 to 1 scale relative to _speed and ignoring
            motion of the screen
        _current_facing: a Direction (Up, Down, Left, Right), which way this
            sprite is currently facing
        _obstacle_collisions: a boolean, whether to alter direction based on
            obstacle collisions
    """
    def __init__(self, game, speed, image_path, obstacle_collisions=True,
                 spawn_pos=None):
        """
        Initializes the character by setting surf and rect, and setting the
        animation frame images.

        Args:
            speed: int, the max character speed in pixels/second
            spawn_pos: tuple of 2 ints, where to spawn this character, defaults
                to top left
            image_path: string giving the path to the character art
        """
        super().__init__(game, image_path, spawn_pos)
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
        self._obstacle_collisions = obstacle_collisions

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
        if self.current_direction == (0, 0):
            return self._current_facing
        angle = self.current_angle
        if -45 <= angle <= 45:
            self._current_facing = Direction.RIGHT
        elif 45 < angle < 135:
            self._current_facing = Direction.DOWN
        elif -135 < angle < -45:
            self._current_facing = Direction.UP
        elif abs(angle) >= 135:
            self._current_facing = Direction.LEFT
        return self._current_facing

    @property
    def current_animation_name(self):
        """
        Returns the current animation name of the sprite based on the facing
        """
        if self._current_direction == (0, 0):
            return f'still_{repr(self.current_facing)}'
        return repr(self.current_facing)

    def reset(self):
        """
        Reset the sprite attributes
        """
        super().reset()
        self._current_direction = (0, 0)
        self._current_facing = Direction.UP

    def set_direction(self, direction):
        """
        Sets the current direction

        Args:
            direction: tuple of 2 floats from -1 to 1, x/y coordinates of
                target speed as percentage of max
        """
        self._current_direction = direction

    def update(self, *args, **kwargs):
        """
        Updates the character's current position and animation. Also detects
        obstacle collisions and sets the direction accordingly.
        """
        super().update()
        # Detect obstacle collisions and move the sprite accordingly
        if self._obstacle_collisions:
            collisions = utils.spritecollide(self, self._game.obstacles)
            for obstacle in collisions:
                threshold = self.rect.height * .25
                if (obstacle.rect.bottom <= self.rect.bottom <=
                    obstacle.rect.bottom + threshold and
                    self.current_direction[1] < 0) or\
                        (obstacle.rect.bottom - threshold <= self.rect.bottom <=
                         obstacle.rect.bottom and self.current_direction[1] >
                         0):
                    self.set_direction((self.current_direction[0], 0))
        # Move sprite in desired direction
        self.move((self.current_direction[0] * self.frame_speed,
                   self.current_direction[1] * self.frame_speed))


# pylint: disable=too-many-instance-attributes
class AttackingSprite(MovingSprite):
    """
    A sprite for a character that can attack

    Attributes:
        _attacking: a boolean, True if the sprite is currently attacking and
            False if not
        _max_health: an int representing the maximum health of the sprite
        _health: an int representing the sprite's current health
        _max_invincibility: an int representing how many frames the sprite has
            invincibility after being attacked
        _invincibility: an int representing how many more frames this sprite is
            invincible for
        _max_knockback: an int representing the maximum number of frames this
            sprite will be knocked back for
        _knockback: an int representing how many more frames this sprite is
            being knocked-back for
        _knockback_dist: an int representing how many pixels the sprite gets
            knocked-back after an attack
        _knockback_direction: a tuple of two floats representing which direction
            the sprite is getting knocked back in
    """
    # pylint: disable=too-many-arguments
    def __init__(self, game, speed, image_path, obstacle_collisions=True,
                 spawn_pos=None, max_health=1,
                 invincibility_time=constants.DEFAULT_INVINCIBILITY,
                 knockback_time=constants.DEFAULT_KNOCKBACK_TIME,
                 knockback_dist=constants.DEFAULT_KNOCKBACK_DIST):
        """
        Initializes the character by setting surf and rect, and setting the
        animation images and other attributes

        Args:
            game: a Game that contains all the sprites
            speed: int, the max character speed in pixels/second
            spawn_pos: tuple of 2 ints, where to spawn this character, defaults
                to top left
            image_path: string giving the path to the character art. Defaults
                to None, which will set a white 50x50 square
            obstacle_collisions: whether this sprite will be stopped by
                obstacles
            max_health: int representing the max health of the sprite
            invincibility_time: a float, the time in seconds that this sprite
                is invincible for after being attacked.
            knockback_time: a float, the time in seconds that this sprite gets
                knocked backward for after being attacked
            knockback_dist: an int, the number of pixels the sprite gets knocked
                back after being attacked
        """
        super().__init__(game, speed, image_path,
                         obstacle_collisions=obstacle_collisions,
                         spawn_pos=spawn_pos)
        # Add attacking animations
        path = f'{constants.IMAGE_FOLDER}/{image_path}'
        for animation in ("attack_up", "attack_down", "attack_left",
                          "attack_right"):
            self._animations[animation] = utils.get_animation_info(
                f'{path}/{animation}')
        self._attacking = False
        self._max_health = max_health
        self._health = self._max_health
        self._max_invincibility = invincibility_time * constants.FRAME_RATE
        self._invincibility = 0
        self._max_knockback = knockback_time * constants.FRAME_RATE
        self._knockback = 0
        self._knockback_dist = knockback_dist
        self._knockback_direction = (0, 0)

    @property
    def health(self):
        """
        Returns the current health of the sprite
        """
        return self._health

    @property
    def is_invincible(self):
        """
        Returns whether the sprite is currently invincible
        """
        return self._invincibility > 0

    @property
    def invincibility_time(self):
        """
        Returns how much longer the sprite is invincible for in seconds
        """
        return self._invincibility / constants.FRAME_RATE

    @property
    def is_attacking(self):
        """
        Returns whether the sprite is currently attacking
        """
        return self._attacking

    @property
    def attack_started(self):
        """
        Returns whether the sprite just started an attack
        """
        return self.is_attacking and self._animation_frame <= 1

    @property
    def current_animation_name(self):
        """
        Returns the current animation name of the sprite as a string
        """
        if self._knockback > 0:
            return f'still_{repr(self.current_facing)}'
        if self.is_attacking:
            return f'attack_{repr(self.current_facing)}'
        return super().current_animation_name

    @property
    def current_facing(self):
        """
        Return the sprite's current Direction facing
        """
        if self.is_attacking or self._knockback > 0:
            return self._current_facing
        return super().current_facing

    def reset(self):
        """
        Resets the sprite attributes
        """
        super().reset()
        self._attacking = False
        self._health = self._max_health
        self._invincibility = 0
        self._knockback = 0

    def damage(self, attack_direction):
        """
        Damages the sprite by removing 1 from its health and initiates knockback

        Args:
            attack_direction: an (x, y) tuple that gives the way the attack was
                taken (and the way this sprite will be knocked back)
        """
        if self.is_invincible:
            return
        self._health -= 1
        self._invincibility = self._max_invincibility
        dist = (attack_direction[0]**2 + attack_direction[1]**2) ** 0.5
        self._knockback_direction = (attack_direction[0] / dist,
                                     attack_direction[1] / dist)
        self._knockback = self._max_knockback

    def attack(self, direction=None):
        """
        Initiates an attack

        Args:
            direction: which way to start the attack. Defaults to the current
                way the sprite is facing
        """
        if direction is None:
            direction = self.current_facing
        self._current_facing = direction
        self._attacking = True
        self._animation_frame = 0

    def update(self, *args, **kwargs):
        """
        Updates the state of the sprite including animation and movement
        """
        # Handle the sprite getting knocked back by an attack
        if self._knockback > 0:
            step = self._knockback_dist/self._max_knockback / self.frame_speed
            self.set_direction((self.current_direction[0] +
                                self._knockback_direction[0] * step,
                                self.current_direction[1] +
                                self._knockback_direction[1] * step))
        super().update()
        # Handle the sprite attacking
        if self._attacking and self._animation_frame == len(
                    self.current_animation['animations']) * int(
                    self.current_animation['frame_length']):
            self._attacking = False
        # Handle if the sprite is invincible and flash the image
        if self.is_invincible:
            self._invincibility -= 1
            if (self.invincibility_time // constants.TRANSPARENT_TIME) \
                    % 2 == 0:
                self.surf.set_alpha(255)
            else:
                self.surf.set_alpha(constants.INVINCIBILITY_ALPHA)
        else:
            self.surf.set_alpha(255)
        # Change the knockback time left
        if self._knockback > 0:
            self._knockback -= 1


class Player(AttackingSprite):
    """
    A sprite for the player
    """
    def __init__(self, game):
        """
        Initializes the player

        Args:
            game: a Game that contains all the sprites
        """
        super().__init__(game, constants.PLAYER_SPEED, 'player',
                         max_health=constants.PLAYER_HEALTH,
                         invincibility_time=constants.PLAYER_INVINCIBILITY)

    def set_direction(self, direction):
        """
        Sets the current direction and ensures that it can't go off screen

        Args:
            direction: tuple of 2 floats from -1 to 1, x/y coordinates of
                target speed as percentage of max
        """
        delta_pos = (direction[0] * self.frame_speed,
                     direction[1] * self.frame_speed)
        if self.rect.left + delta_pos[0] < 0\
          or self.rect.right + delta_pos[0] > constants.SCREEN_WIDTH:
            self._current_direction = (0, direction[1])
        elif self.rect.top + delta_pos[1] < 0\
           or self.rect.bottom + delta_pos[1] > constants.SCREEN_HEIGHT:
            self._current_direction = (direction[0], 0)
        else:
            self._current_direction = direction


class Demon(AttackingSprite):
    """
    A sprite for all the enemies
    """
    def __init__(self, game, spawn_pos=None):
        """
        Initializes the demon

        Args:
            game: a Game that contains all the sprites
            spawn_pos: a tuple of 2 ints, where to spawn the demon, defaults
                to the center of the screen
        """
        super().__init__(game, constants.DEMON_SPEED, 'demon',
                         spawn_pos=spawn_pos, max_health=constants.DEMON_HEALTH,
                         invincibility_time=constants.DEMON_INVINCIBILITY)


class Flashlight(MovingSprite):
    """
    A transparent sprite for the flashlight beam
    """
    def __init__(self, game):
        """
        Initializes the flashlight

        Args:
            game: a Game that contains all the sprites
        """
        super().__init__(game, constants.PLAYER_SPEED, 'flashlight',
                         obstacle_collisions=False,
                         spawn_pos=constants.FLASHLIGHT_SPAWN)

    @property
    def current_animation_name(self):
        """
        Returns the current animation name of the flashlight
        """
        player_ani = self._game.player.current_animation_name
        return player_ani[player_ani.find('_') + 1:]


class Obstacle(GameSprite):
    """
    A sprite for game obstacles
    """
    def __init__(self, game, spawn_pos=None):
        """
        Initializes the obstacle

        Args:
            game: a Game that contains all the sprites
            spawn_pos: a tuple of 2 ints, where to spawn the obstacle, defaults
                to the center of the screen
        """
        super().__init__(game, 'obstacle', spawn_pos=spawn_pos)

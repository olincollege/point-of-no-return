"""
Tests for functions in sprites.py
"""
import pygame
import pytest
import src.constants as constants
import src.utils as utils
from src.sprites import Direction, GameSprite, MovingSprite
from src.game import Game


pygame.init()
pygame.display.set_mode((1, 1))


def empty_game():
    """
    Create a new instance of a game to use in testing. Clears obstacles to
    remove possible accidental sprite collisions.

    Returns:
        An instance of Game.
    """
    game = Game()
    game.obstacles.empty()
    return game


ANIMATION_CASES = [
    (1, 0),
    (constants.FRAME_RATE//5 + 1, 1),
    (2 * constants.FRAME_RATE//5 + 1, 2),
    (3 * constants.FRAME_RATE//5 + 1, 3),
    (4 * constants.FRAME_RATE//5 + 1, 0),
]


@pytest.mark.parametrize('frames,image', ANIMATION_CASES)
def test_correct_animation_frame(frames, image):
    """
    Tests whether a GameSprite's sprite surf updates to the correct image
    """
    sprite = GameSprite(empty_game(), 'test_animations')
    for _ in range(frames):
        sprite.update()
    # pylint: disable=protected-access
    assert sprite.surf == sprite._animations['stills']['animations'][image]


def shifted_position(direction):
    """
    Helper function to find the shifted position of the next animation for
    checking positioning in test_moving_sprite_properties.

    Args:
        direction: a string representing the direction the sprite animation
            should be in

    Returns:
        A tuple of two floats representing the shifted center position of the
        animation image
    """
    last_pos = \
        utils.get_animation_info(f"{constants.IMAGE_FOLDER}/test_animations")\
        ['positions'][0]
    next_pos = \
        utils.get_animation_info(
            f"{constants.IMAGE_FOLDER}/test_animations/{direction}")\
            ['positions'][0]
    return (constants.SCREEN_WIDTH/2 + last_pos[0] - next_pos[0],
            constants.SCREEN_HEIGHT/2 + last_pos[1] - next_pos[1])


MOVEMENT_CASES = [
    ((0, 0), 'still_up', Direction.UP,
     (constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)),
    ((1, 0), 'right', Direction.RIGHT,
     (shifted_position('right')[0] +
      constants.PLAYER_SPEED//constants.FRAME_RATE,
      shifted_position('right')[1])),
    ((-1, 0), 'left', Direction.LEFT,
     (shifted_position('left')[0] -
      constants.PLAYER_SPEED // constants.FRAME_RATE,
      shifted_position('left')[1])),
    ((0, -1), 'up', Direction.UP,
     (shifted_position('up')[0],
      shifted_position('up')[1] -
      constants.PLAYER_SPEED // constants.FRAME_RATE)),
    ((0, 1), 'down', Direction.DOWN,
     (shifted_position('up')[0],
      shifted_position('up')[1] +
      constants.PLAYER_SPEED // constants.FRAME_RATE)),
    ((-1, -1), 'left', Direction.LEFT,
     (shifted_position('left')[0] -
      constants.PLAYER_SPEED // constants.FRAME_RATE,
      shifted_position('left')[1] -
      constants.PLAYER_SPEED // constants.FRAME_RATE)),
    ((1, 1), 'right', Direction.RIGHT,
     (shifted_position('left')[0] +
      constants.PLAYER_SPEED // constants.FRAME_RATE,
      shifted_position('left')[1] +
      constants.PLAYER_SPEED // constants.FRAME_RATE)),
    ((-1, -2), 'up', Direction.UP,
     (shifted_position('up')[0] -
      constants.PLAYER_SPEED // constants.FRAME_RATE,
      shifted_position('up')[1] -
      2 * constants.PLAYER_SPEED // constants.FRAME_RATE)),
    ((1, 2), 'down', Direction.DOWN,
     (shifted_position('down')[0] +
      constants.PLAYER_SPEED // constants.FRAME_RATE,
      shifted_position('down')[1] +
      2 * constants.PLAYER_SPEED // constants.FRAME_RATE)),
]


@pytest.mark.parametrize('direction,animation,facing,position', MOVEMENT_CASES)
def test_moving_sprite_properties(direction, animation, facing, position):
    """
    Tests whether updating a MovingSprite in a given direction results in the
    correct changes in its attributes (current animation, current facing,
    position).
    """
    sprite = MovingSprite(empty_game(), constants.PLAYER_SPEED,
                          'test_animations')
    sprite.set_direction(direction)
    sprite.update()
    # pylint: disable=protected-access
    assert sprite.current_animation == sprite._animations[animation]
    assert sprite.current_facing == facing
    assert sprite.rect.center == position

"""
Tests for functions in sprites.py
"""
import pygame
import pytest
import src.constants as constants
import src.utils as utils
from src.sprites import Direction, GameSprite, MovingSprite, AttackingSprite
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
    assert sprite.surf == sprite._animations['stills']['animations'][image]


info = utils.get_animation_info("../media/images/test_animations")

MOVEMENT_CASES = [
    ((0, 0), 'still_up', Direction.UP,
     (constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2)),
]


@pytest.mark.parametrize('direction,animation,facing,position', MOVEMENT_CASES)
def test_moving_sprite_properties(direction, animation, facing, position):
    """
    Tests whether updating a MovingSprite in a given direction results in the
    correct changes in its attributes.
    """
    sprite = MovingSprite(empty_game(), 1, 'test_animations')
    sprite.set_direction(direction)
    sprite.update()
    assert sprite.current_animation == sprite._animations[animation]
    assert sprite.current_facing == facing
    assert sprite.rect.center == position

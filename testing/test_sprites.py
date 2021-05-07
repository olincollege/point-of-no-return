"""
Tests for functions in sprites.py
"""
import pygame
import pytest
import src.constants as constants
import src.utils as utils
import src.sprites as sprites
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
    (13, 1),
    (25, 2),
    (37, 3),
]


@pytest.mark.parametrize('frames,image', ANIMATION_CASES)
def test_correct_animation_frame(frames, image):
    """
    Tests whether the sprite surf updates to the correct image
    """
    sprite = sprites.GameSprite(empty_game(), 'test_animations')
    for _ in range(frames):
        sprite.update()
    assert sprite.surf == sprite._animations['stills']['animations'][image]

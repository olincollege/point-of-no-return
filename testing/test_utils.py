"""
Tests for functions in utils.py
"""
import pygame
import pytest
import src.constants as constants
import src.utils as utils


def test_animation_info():
    """
    Tests whether the get_animation_info returns the stuff from /test_animations
    """
    pygame.init()
    _ = pygame.display.set_mode((1, 1))
    info = utils.get_animation_info(f"{constants.IMAGE_FOLDER}/test_animations")
    assert len(info['animations']) == 4
    assert info['positions'] == [(25, 23), (3, 4), (5, 6), (7, 8)]
    assert info['frame_length'] == constants.FRAME_RATE / 5


IS_SWORD_CASES = [
    ((0, 0, 0), False),
    ((255, 255, 255), False),
    ((255, 0, 0), False),
    ((0, 255, 0), False),
    ((0, 0, 255), False),
    ((255, 255, 0), False),
    ((255, 0, 255), False),
    ((0, 255, 255), False),
    ((150, 150, 150), True),
    ((150, 151, 152), True),
    ((110, 200, 120), False),
]


@pytest.mark.parametrize("color,sword", IS_SWORD_CASES)
def test_is_sword(color, sword):
    """
    Tests whether the is_sword function properly detects swords
    """
    assert utils.is_sword(color) == sword

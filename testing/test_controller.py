"""
Test methods for the controllers
"""

import math
import pygame
import pytest
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from src.controller import DemonController
from src.game import Game
from src.sprites import Demon

pygame.init()
pygame.display.set_mode((1, 1))


def empty_game():
    """
    Returns a game set up for testing controllers
    """
    game = Game()
    game.obstacles.empty()
    return game


# We tried to use Pynput to simulate keyboard input but Pygame did not register
# the key presses.
# PC_MOVEMENT_CASES = [
#     ('w', (0, -1)),
#     ('a', (-1, 0)),
#     ('s', (0, 1)),
#     ('d', (1, 0)),
#     (('w', 's'), (0, 0)),
#     (('a', 'd'), (0, 0)),
#     (('w', 'a'), (-1, -1)),
#     (('w', 'd'), (1, -1)),
#     (('a', 's'), (-1, 1)),
#     (('s', 'd'), (1, 1)),
#     (('w', 'a', 's'), (-1, 0)),
#     (('w', 'd', 's'), (1, 0)),
#     (('a', 'w', 'd'), (0, -1)),
#     (('a', 's', 'd'), (0, 1)),
#     (('w', 'a', 's', 'd'), (0, 0))
# ]
#
#
# @pytest.mark.parametrize("keys,direction", PC_MOVEMENT_CASES)
# def test_player_controller_movement(keys, direction):
#     """
#     Tests the movement for the player controller
#     """
#     game = empty_game()
#     player = PlayerController(game)
#     keyboard = Controller()
#     for key in keys:
#         keyboard.press(key)
#     player.update()
#     for key in keys:
#         keyboard.release(key)
#     assert game.player.current_direction == direction
#
#
# PC_ATTACK_CASES = [
#     (Key.up, Direction.UP),
#     (Key.left, Direction.LEFT),
#     (Key.down, Direction.DOWN),
#     (Key.right, Direction.RIGHT)
# ]
#
#
# @pytest.mark.parametrize("key,direction", PC_ATTACK_CASES)
# def test_player_controller_attack(key, direction):
#     """
#     Tests the attacking for the player controller
#     """
#     game = empty_game()
#     player = PlayerController(game)
#     keyboard = Controller()
#     keyboard.press(key)
#     player.update()
#     keyboard.release(key)
#     assert game.player.is_attacking and game.player.current_facing\
#            == direction


angle_to_mid = math.atan2(SCREEN_HEIGHT, SCREEN_WIDTH)
demon_x_dir = math.cos(angle_to_mid)
demon_y_dir = math.sin(angle_to_mid)
DC_CASES = [
    ((SCREEN_WIDTH / 2, 0), (0, 1)),
    ((SCREEN_WIDTH / 2, SCREEN_HEIGHT), (0, -1)),
    ((0, SCREEN_HEIGHT / 2), (1, 0)),
    ((SCREEN_WIDTH, SCREEN_HEIGHT / 2), (-1, 0)),
    ((0, 0), (demon_x_dir, demon_y_dir)),
    ((SCREEN_WIDTH, 0), (-demon_x_dir, demon_y_dir)),
    ((0, SCREEN_HEIGHT), (demon_x_dir, -demon_y_dir)),
    ((SCREEN_WIDTH, SCREEN_HEIGHT), (-demon_x_dir, -demon_y_dir))
]


@pytest.mark.parametrize("spawn,direction", DC_CASES)
def test_demon_controller(spawn, direction):
    """
    Tests the demon controller's movement
    """
    game = empty_game()
    demon = DemonController(game)
    demon_sprite = Demon(game, spawn)
    game.demons.add(demon_sprite)
    game.all_sprites.add(demon_sprite)
    demon.update()
    assert demon_sprite.current_direction == direction

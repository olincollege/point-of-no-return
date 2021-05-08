"""
Tests the Game model
"""

import pygame
import pytest
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT,\
    DEMON_MIN_SPAWN_DIST, DEMON_MAX_SPAWN_DIST,\
    OBSTACLE_MIN_SPAWN_DIST, OBSTACLE_MAX_SPAWN_DIST
from src.game import Game

pygame.init()
pygame.display.set_mode((1, 1))


def test_new_demon():
    """
    Tests creation of new demons
    """
    runs = 10
    game = Game()
    og_sprites = len(game.all_sprites)
    for _ in range(runs):
        game.create_new_demon()
    assert len(game.demons) == runs
    assert len(game.all_sprites) == runs + og_sprites
    for demon in game.demons:
        pos = demon.rect.center
        assert (-DEMON_MIN_SPAWN_DIST >= pos[0] >= -DEMON_MAX_SPAWN_DIST) or\
               (DEMON_MIN_SPAWN_DIST <= pos[0] - SCREEN_WIDTH <=
                DEMON_MAX_SPAWN_DIST) or (-DEMON_MIN_SPAWN_DIST >= pos[1] >=
                                          -DEMON_MAX_SPAWN_DIST) or\
               (DEMON_MIN_SPAWN_DIST <= pos[1] - SCREEN_HEIGHT <=
                DEMON_MAX_SPAWN_DIST)


@pytest.mark.parametrize("is_top", [True, False])
def test_new_obstacle(is_top):
    """
    Tests creation of new obstacles
    """
    runs = 10
    game = Game()
    og_obs = len(game.obstacles)
    og_sprites = len(game.all_sprites)
    for _ in range(runs):
        game.create_new_obstacle(is_top)
    assert len(game.obstacles) == runs + og_obs
    assert len(game.all_sprites) == runs + og_sprites
    for obs in game.obstacles:
        pos = obs.rect.center
        assert 0 <= pos[0] <= SCREEN_WIDTH
        assert (-OBSTACLE_MAX_SPAWN_DIST <= pos[1] <= -OBSTACLE_MIN_SPAWN_DIST)\
            or (OBSTACLE_MIN_SPAWN_DIST <= pos[1] - SCREEN_HEIGHT <=
                OBSTACLE_MAX_SPAWN_DIST)

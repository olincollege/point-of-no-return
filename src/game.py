"""
**INSERT TITLE** Game
"""

import pygame
import random
import constants
import sprites


class Game:
    """
    Holds the current game state
    """
    def __init__(self):
        """
        Initializes this instance of the game
        """
        self.player = sprites.Player()
        self.demons = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

    def create_new_demon(self):
        demon = sprites.Demon((random.randint(0, constants.SCREEN_WIDTH),
                               random.randint(-constants.DEMON_MAX_SPAWN_DIST,
                                              -constants.DEMON_MIN_SPAWN_DIST)))
        self.demons.add(demon)
        self.all_sprites.add(demon)

    def create_new_obstacle(self):
        obs = sprites.Obstacle((random.randint(0, constants.SCREEN_WIDTH),
                                random.randint(-constants.
                                               OBSTACLE_MAX_SPAWN_DIST,
                                               -constants.
                                               OBSTACLE_MIN_SPAWN_DIST)))
        self.obstacles.add(obs)
        self.all_sprites.add(obs)

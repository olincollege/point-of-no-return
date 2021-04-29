"""
**INSERT TITLE** Game
"""

import pygame
import random
import constants
import sprites
import utils


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

    def update(self):
        collisions = pygame.sprite.\
            spritecollide(self.player, self.demons, False,
                          collided=pygame.sprite.collide_mask)
        for demon in collisions:
            if utils.touching_sword(self.player, demon):
                demon.damage(self.player.current_facing.value)
            elif not self.player.is_invincible:
                self.player.damage(demon.current_direction)
        if not self.player.is_attacking and not self.player.is_invincible:
            for demon in collisions:
                self.player.damage(demon.current_direction)

        for demon in self.demons:
            if demon.health <= 0:
                demon.kill()
        if self.player.health <= 0:
            self.player.kill()

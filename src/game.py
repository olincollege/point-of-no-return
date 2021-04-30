"""
**INSERT TITLE** Game
"""

import pygame
import random
import constants
import sprites
from sprites import Direction
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
        self.demons = pygame.sprite.LayeredUpdates()
        self.obstacles = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_sprites.add(self.player)

    def create_new_demon(self):
        spawn_direction = random.choice((Direction.UP, Direction.DOWN,
                                         Direction.LEFT, Direction.RIGHT))
        spawn_dist = random.randint(constants.DEMON_MIN_SPAWN_DIST,
                                    constants.DEMON_MAX_SPAWN_DIST)
        spawn_value = random.randint(0, constants.SCREEN_WIDTH if
                                     spawn_direction.value[0] == 0 else
                                     constants.SCREEN_HEIGHT)
        spawn_pos = None
        if spawn_direction == Direction.UP:
            spawn_pos = (spawn_value, -spawn_dist)
        elif spawn_direction == Direction.DOWN:
            spawn_pos = (spawn_value, constants.SCREEN_HEIGHT + spawn_dist)
        elif spawn_direction == Direction.LEFT:
            spawn_pos = (-spawn_dist, spawn_value)
        elif spawn_direction == Direction.RIGHT:
            spawn_pos = (constants.SCREEN_WIDTH + spawn_dist, spawn_value)
        else:
            spawn_pos = (50, 50)

        demon = sprites.Demon(spawn_pos=spawn_pos)
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
        for entity in self.all_sprites:
            self.all_sprites.change_layer(entity, entity.layer)

        collisions = pygame.sprite.\
            spritecollide(self.player, self.demons, False,
                          collided=pygame.sprite.collide_mask)
        for demon in collisions:
            if utils.touching_sword(self.player, demon):
                demon.damage(self.player.current_facing.value)
            else:
                self.player.damage(demon.current_direction)

        for demon in self.demons:
            if demon.health <= 0:
                demon.kill()
        if self.player.health <= 0:
            self.player.kill()

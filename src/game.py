"""
**INSERT TITLE** Game
"""

import math
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
        self.demons = pygame.sprite.LayeredUpdates()
        self.obstacles = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_sprites.add(self.player)

    def create_new_demon(self):
        min_x = constants.SCREEN_WIDTH + constants.DEMON_MIN_SPAWN_DIST
        min_y = constants.SCREEN_HEIGHT + constants.DEMON_MIN_SPAWN_DIST
        dist = constants.DEMON_MAX_SPAWN_DIST - constants.DEMON_MIN_SPAWN_DIST

        theta = random.uniform(-math.pi, math.pi)
        max_theta = math.atan(min_y / min_x)
        is_x = abs(theta) < max_theta or abs(theta) > math.pi - max_theta
        trig = abs(math.cos(theta) if is_x else math.sin(theta))

        min_rad = (min_x if is_x else min_y) / 2.0 / trig
        rad = random.uniform(min_rad, min_rad + dist / trig)
        spawn_pos = (rad * math.cos(theta) + constants.SCREEN_WIDTH / 2,
                     rad * math.sin(theta) + constants.SCREEN_HEIGHT / 2)
        
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

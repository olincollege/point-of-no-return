"""
Point of No Return Game class
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
        self.running = False
        self.player = sprites.Player(self)
        self.demons = pygame.sprite.LayeredUpdates()
        self.obstacles = pygame.sprite.LayeredUpdates()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.all_sprites.add(self.player)
        self.create_new_obstacle(True)

    def create_new_demon(self):
        """
        Spawns a new demon in the game at a random location outside the screen.
        """
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

        demon = sprites.Demon(self, spawn_pos=spawn_pos)
        self.demons.add(demon)
        self.all_sprites.add(demon)

    def create_new_obstacle(self, is_top):
        """
        Spawns a new obstacle in the game

        Args:
            is_top: a boolean, True if the obstacles should spawn above the
                screen, False if it should spawn below
        """
        y_val = -random.randint(constants.OBSTACLE_MIN_SPAWN_DIST,
                                constants.OBSTACLE_MAX_SPAWN_DIST)
        if not is_top:
            y_val = constants.SCREEN_HEIGHT - y_val

        obs = sprites.Obstacle(self, (random.randint(0, constants.SCREEN_WIDTH),
                                      y_val))
        self.obstacles.add(obs)
        self.all_sprites.add(obs)

    def restart(self):
        """
        Resets game state and restarts the game
        """
        self.player.reset()
        self.demons.empty()
        self.obstacles.empty()
        self.all_sprites.empty()
        self.all_sprites.add(self.player)
        self.create_new_obstacle(True)
        self.running = True

    def update(self):
        """
        Updates the game state, including checking attacks against demons and
        damage to the player. Also creates new obstacles as the player moves
        forward or backward on the map.
        """
        collisions = utils.spritecollide(self.player, self.demons)
        for demon in collisions:
            if utils.touching_sword(self.player, demon):
                demon.damage(self.player.current_facing.value)
            else:
                if demon.current_direction == (0, 0):
                    self.player.damage(demon.current_facing.value)
                else:
                    self.player.damage(demon.current_direction)

        for demon in self.demons:
            if demon.health <= 0:
                demon.kill()

        if self.player.health <= 0:
            self.player.kill()

        for group in (self.all_sprites, self.demons, self.obstacles):
            for entity in group:
                group.change_layer(entity, entity.layer)

        if self.player.current_direction[1] < 0\
                and self.player.layer - constants.OBSTACLE_SPAWN_TRIGGER_DIST\
                < self.obstacles.get_bottom_layer():
            self.create_new_obstacle(True)
        elif self.player.current_direction[1] > 0\
                and self.player.layer + constants.OBSTACLE_SPAWN_TRIGGER_DIST\
                > self.obstacles.get_top_layer():
            self.create_new_obstacle(False)

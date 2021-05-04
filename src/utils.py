"""
Utility helper functions for Point of No Return
"""
import json
import os
import pygame
import constants

event_num = pygame.USEREVENT


def new_event():
    """
    Returns a new event that is unique from all previously defined events
    """
    global event_num
    event_num += 1
    return event_num


def get_animation_info(path):
    """
    Compiles all animation information in a given folder

    Args:
        path: a string, the path to the target folder

    Returns:
        a dict with three elements:
            'animations' maps to a list of images,
            'frame_length' maps to a float, how many game frames to display each
                animation frame
            'positions' maps to a list of 2-element tuples, the offset for each
                frame in the animation
    """
    animation_info = {}
    with open(f'{path}/info.json') as info:
        info_dict = json.loads(''.join(info.readlines()))
        animation_info['frame_length'] = constants.FRAME_RATE / info_dict['fps']
        animation_info['positions'] = []
        for pos in info_dict['pos']:
            animation_info['positions'].append((pos[0], pos[1]))
    animation_info['animations'] = []
    counter = 0
    while os.access(f'{path}/{counter}.png', os.F_OK):
        animation_info['animations'].append(pygame.image.load(
            f'{path}/{counter}.png').convert_alpha())
        counter += 1
    return animation_info


def is_sword(color):
    """
    Finds if a certain pixel is part of the character's sword. This is defined
    as a grayscale pixel (difference no larger than 5%) with an average value
    between 100 and 225.

    Args:
        color: a tuple of rgba values

    Returns:
        a boolean, True iff the color could represent a pixel on the sword
    """
    r = color[0]
    g = color[1]
    b = color[2]
    av = (r + g + b) / 3
    max_diff = av * 0.05
    if abs(r - g) > max_diff or abs(r - b) > max_diff or abs(g - b) > max_diff:
        return False
    return 100 < av < 225


def touching_sword(player, demon):
    """
    Determines whether the demon has been hit by the player's sword

    Args:
        player: the Player that is attacking
        demon: the Demon to check for if it has been hit

    Return a boolean, True iff the demon has been hit by the player's sword
    """
    if not player.is_attacking:
        return False
    collide = pygame.sprite.collide_mask(player, demon)
    if collide is None:
        return False
    return is_sword(player.surf.get_at(collide))


def spritecollide(sprite, group):
    """
    Runs sprite collide with our default parameters

    Args:
         sprite: the sprite to check for collisions with
         group: the sprite group to check for collisions against

    Returns a list of sprites from the group that are colliding with sprite
    """
    return pygame.sprite.spritecollide(sprite, group, False,
                                       collided=lambda s1, s2: pygame.sprite
                                       .collide_mask(s1, s2) is not None)

"""
Utility helper functions for Point of No Return
"""
import json
import os
import pygame
import src.constants as constants


def get_animation_info(path):
    """
    Compiles all animation information in a given folder

    Args:
        path: a string, the path to the target folder

    Returns:
        a dict with three elements:
            'animations' maps to a list of images,
            'frame_length' maps to a float, how many src frames to display each
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
    red = color[0]
    green = color[1]
    blue = color[2]
    average_value = (red + green + blue) / 3
    max_diff = average_value * 0.05
    if abs(red - green) > max_diff or abs(red - blue) > max_diff or\
            abs(green - blue) > max_diff:
        return False
    return 100 < average_value < 225


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


def blit_alpha(target, source, location, opacity, special_flags=None):
    """
    Blits the source onto the target at the specified location and opacity

    Args:
        target: a Surface to blit onto
        source: a Surface that gets made transparent and is put on target
        location: an (x, y) tuple, where to put source on target
        opacity: an int from 0-255, what to set alpha to
        special_flags: optional, any special flags from pygame to pass to blit
    """
    temp = pygame.Surface((source.get_width(), source.get_height()),
                          pygame.SRCALPHA)
    temp.fill((0, 0, 0, opacity))
    temp.blit(source, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    target.blit(temp, location, special_flags=special_flags)

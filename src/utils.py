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

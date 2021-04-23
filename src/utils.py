import pygame

event_num = pygame.USEREVENT


def new_event():
    global event_num
    event_num += 1
    return event_num

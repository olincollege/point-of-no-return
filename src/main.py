"""
Main class with game loop for Point of No Return
"""
import pygame
import constants
from controller import PlayerController, DemonController, ScrollController
from game import Game
from utils import new_event
from view import GraphicView


def main():
    """
    Initializes pygame, runs the main game loop
    """
    pygame.init()
    screen = pygame.display.set_mode(constants.SCREEN_SIZE)
    game = Game()
    player = PlayerController(game)
    demons = DemonController(game)
    all_sprites = ScrollController(game)
    view = GraphicView(game, screen)
    view.setup()

    ADD_DEMON = new_event()
    pygame.time.set_timer(ADD_DEMON, constants.DEMON_SPAWN_TIME)

    clock = pygame.time.Clock()

    exited = False
    while not exited:
        if game.running:
            for event in pygame.event.get():
                if event.type == pygame.locals.KEYDOWN:
                    if event.key == pygame.locals.K_ESCAPE:
                        game.paused = True
                elif event.type == pygame.locals.QUIT:
                    game.running = False
                    exited = True
                elif event.type == ADD_DEMON:
                    game.create_new_demon()

            player.update()
            demons.update()
            all_sprites.update()
            game.update()

            if not game.player.alive():
                game.running = False

            view.draw()
            clock.tick(constants.FRAME_RATE)

if __name__ == '__main__':
    main()

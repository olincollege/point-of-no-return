import pygame
import constants
from controller import PlayerController, DemonController, ObstacleController
from game import Game
from utils import new_event
from view import GraphicView

game = Game()
player = PlayerController(game, game.player)
demons = DemonController(game, game.demons)
obstacles = ObstacleController(game, game.obstacles)
view = GraphicView(game)
view.setup()

ADD_DEMON = new_event()
pygame.time.set_timer(ADD_DEMON, constants.DEMON_SPAWN_TIME)
ADD_OBSTACLE = new_event()
pygame.time.set_timer(ADD_OBSTACLE, constants.OBSTACLE_SPAWN_TIME)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_ESCAPE:
                running = False
        elif event.type == pygame.locals.QUIT:
            running = False
        elif event.type == ADD_DEMON:
            game.create_new_demon()
        elif event.type == ADD_OBSTACLE:
            game.create_new_obstacle()

    player.update()
    demons.update()
    obstacles.update()
    view.draw()
    clock.tick(constants.FRAME_RATE)

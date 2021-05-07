# Point of No Return
A game by Ben and Allison.

## Overview
Point of No Return is a 2D infinite world thriller survival game. You're left to fend for yourself while you navigate a strange world full of dangers you can't yet understand.

## Installation and Setup
Clone this repository to your machine. From the command line, navigate to the `src/` directory. The game can then be run with the command `python main.py`. Alternatively, you can run `main.py` from your IDE.

## Libraries and Packages
Our game is built using [PyGame](https://www.pygame.org/), a Python wrapper for the [Simple DirectMedia Layer (SDL) library](https://www.libsdl.org/), which allows access to a computer's multimedia components. We also used the [PyGame-menu](https://pygame-menu.readthedocs.io/en/4.0.4/) library for main menus in the game. To install the packages needed to run this game using pip, run the following command in Bash:

`$ pip install pygame pygame-menu`

For testing purposes, we also used [Pynput](https://pynput.readthedocs.io/en/latest/) to control the keyboard. To use the test folders, run the following command:

`$ pip install pynput`

## Included Files
`/src`: Contains all source code files for the game (`.py`)
* `sprites.py`: All sprite classes for the game, including basic `GameSprite`, and subclasses `MovingSprite` and `AttackingSprite`. `Player`, `Demon` and `Obstacle` are all subclasses of one of the three larger sprite classes.
* `game.py`: Contains `Game` class which stores the full game state.
* `controller.py`: All controllers for the game, which dictate how the sprites move and interact based on player input or basic AI. Includes abstract `Controller` class and subclasses `PlayerController`, `DemonController`, and `ScrollController`.
* `view.py`: Contains classes for the GUI to display the game. Includes abstract `View` class to accomodate for potential other view types, and subclass `GraphicView` that displays the game in 2D using PyGame.
* `main.py`: Initializes PyGame, view, controllers, and game state. Runs main game loop, which includes PyGame events, updating the game state, and drawing the game.
* `utils.py`: Contains helper utility functions for the game.
* `constants.py`: File for constants used across files.

`/testing`: Contains all files for unit testing the game using pytest
* `test_controller.py`: Unit tests for the controllers in `src/controllers.py`
* `test_utils.py`: Unit tests for the functions in `src/utils.py`

`/media`: Contains all media files, including images and audio, for the game.
* `/images`: Images for sprites and background. Each sprite's folder contains folders with all of their animation frames.
    * `info.json` files: Includes a dictionary with information for the framerate that each animation should be run at, and a list of coordinate pairs giving what point to align the animation images at (e.g. center of the head for the player sprites).
* `/audio`: Music and sound effect files.

## Media Credits
Images:
* [Blood Drip](http://clipart-library.com/clipart/n897862.htm)
* [Demon Sprite](https://www.deviantart.com/studiofallen/art/Demon-Sprite-Sheet-437061869) by StudioFallen on DeviantArt
* [Boulder](https://line.17qq.com/articles/dkgkgkgdv_p5.html)

Audio:

Background music- ["Ghosts in the wind"](http://dig.ccmixter.org/files/Citizen_X0/29247) by Abstract Audio on digiccMixter

Sound effects- Licensed for free use from [Mixkit](https://mixkit.co/)

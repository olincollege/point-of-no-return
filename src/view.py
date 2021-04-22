from abc import ABC, abstractmethod


class View(ABC):
    """
    Handles the drawing of the game
    """
    def __init__(self, game):
        """
        Initializes the view

        Args:
            game: a Game to monitor the state of
        """
        self._game = game

    @abstractmethod
    def draw(self):
        """
        Draws the game based on current state
        """
        pass

from abc import ABC, abstractmethod


class Controller(ABC):
    """
    Handles the player's inputs
    """
    def __init__(self, game):
        """
        Initializes the controller

        Args:
            game: a Game to update the state of
        """
        self._game = game

    @abstractmethod
    def update(self):
        """
        Updates the game model based on player inputs
        """
        pass

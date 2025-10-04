from enum import Enum


class Move(Enum):
    """The choice of move returned by a strategy for one round of the game."""
    SHARE = 0
    STEAL = 1


class GameState:
    """The readonly state of game after some number of rounds."""
    def __init__(self):
        self.my_move_history: list[Move] = []
        self.their_move_history: list[Move] = []
        self.my_points = 0
        self.their_points = 0

from enum import Enum


class GameOutcome(Enum):
    """
    Enum for the status of a game.
    """
    CHALLENGER_WON = 1
    OPPONENT_WON = 2
    DRAW = 3

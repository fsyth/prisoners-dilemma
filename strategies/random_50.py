from dilemma import GameState, Move, strategy

from random import choice


@strategy
def random_50(state: GameState) -> Move:
    return choice((Move.SHARE, Move.STEAL))

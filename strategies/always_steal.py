from dilemma import GameState, Move, strategy


@strategy
def always_steal(state: GameState) -> Move:
    """
    Always steals, no matter what.
    Opposite of always_share.
    """
    return Move.STEAL

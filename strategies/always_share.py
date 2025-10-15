from dilemma import GameState, Move, strategy


@strategy
def always_share(state: GameState) -> Move:
    """
    Always shares, no matter what.
    Opposite of always_steal.
    """
    return Move.SHARE

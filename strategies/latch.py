from dilemma import GameState, Move, strategy


@strategy
def latch(state: GameState) -> Move:
    """
    Steals for the rest of the game if they ever steal.
    Similar to betrayal.
    """
    if Move.STEAL in state.their_move_history:
        return Move.STEAL

    return Move.SHARE

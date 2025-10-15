from dilemma import GameState, Move, strategy


@strategy
def jealous(state: GameState) -> Move:
    """
    Steals when behind on points.
    Similar to competitive.
    """
    return Move.STEAL if state.my_points < state.their_points else Move.SHARE

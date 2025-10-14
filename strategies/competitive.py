from dilemma import GameState, Move, strategy


@strategy
def competitive(state: GameState) -> Move:
    """
    Steals unless ahead on points.
    Similar to jealous.
    """
    return Move.STEAL if state.my_points <= state.their_points else Move.SHARE

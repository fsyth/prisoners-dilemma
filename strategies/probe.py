from dilemma import GameState, Move, strategy


@strategy
def probe(state: GameState) -> Move:
    """Steals first. If they steal in response, play nice."""
    if len(state.their_move_history) == 0:
        return Move.STEAL

    if len(state.their_move_history) == 1:
        return Move.SHARE

    if state.their_move_history[1] == Move.STEAL:
        return Move.SHARE

    return Move.STEAL

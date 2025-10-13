from dilemma import GameState, Move, strategy


@strategy
def betrayal(state: GameState) -> Move:
    """Steals for the rest of the game if they ever share 3 times in a row."""
    if any(state.their_move_history[i:i+3] == 3*[Move.SHARE] for i in range(len(state.their_move_history)-2)):
        return Move.STEAL

    return Move.SHARE

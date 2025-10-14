from dilemma import GameState, Move, strategy


@strategy
def eye_for_an_eye(state: GameState) -> Move:
    """Steals if they stole last turn."""
    if state.turns_played > 0:
        return state.their_move_history[-1]

    return Move.SHARE

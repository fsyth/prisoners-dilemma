from dilemma import GameState, Move, strategy


@strategy
def eye_for_an_eye(state: GameState) -> Move:
    if len(state.their_move_history) > 0:
        return state.their_move_history[-1]

    return Move.SHARE

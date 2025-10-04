from dilemma import GameState, Move, strategy


@strategy
def always_steal(state: GameState) -> Move:
    return Move.STEAL

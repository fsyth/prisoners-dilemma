from dilemma import GameState, Move, strategy


@strategy
def always_share(state: GameState) -> Move:
    return Move.SHARE

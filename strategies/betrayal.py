from dilemma import GameState, Move, strategy


@strategy
def betrayal(state: GameState) -> Move:
	if any(state.their_move_history[i:i+3] == 3*[Move.SHARE] for i in range(len(state.their_move_history)-2)):
		return Move.STEAL

	return Move.SHARE

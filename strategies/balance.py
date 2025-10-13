from dilemma import GameState, Move, strategy

from collections import Counter
from itertools import chain


@strategy
def balance(state: GameState) -> Move:
    """Does whatever there's been least of: steals or shares. Opposite of vibes."""
    counts = Counter(chain(state.my_move_history, state.their_move_history))

    return Move.STEAL if counts[Move.STEAL] < counts[Move.SHARE] else Move.SHARE

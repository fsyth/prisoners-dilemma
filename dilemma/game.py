from dilemma.gamestate import GameState, Move
from dilemma.strategy import StrategyFunc

class Game:
    """A game playable by a pair of StrategyFuncs."""
    def __init__(self, strategy_a: StrategyFunc, strategy_b: StrategyFunc, turn_limit = 200):
        self.strategy_a = strategy_a
        self.strategy_b = strategy_b
        self.turn_limit = turn_limit

        self.move_history: list[tuple[Move, Move]] = []
        self.points_a = 0
        self.points_b = 0

    def perspective_from_a(self) -> GameState:
        """Get the GameState from the perspective of strategy_a."""
        state = GameState()
        state.my_move_history    = [turn[0] for turn in self.move_history]
        state.their_move_history = [turn[1] for turn in self.move_history]
        state.my_points    = self.points_a
        state.their_points = self.points_b
        return state

    def perspective_from_b(self) -> GameState:
        """Get the GameState from the perspective of strategy_b."""
        state = GameState()
        state.my_move_history    = [turn[1] for turn in self.move_history]
        state.their_move_history = [turn[0] for turn in self.move_history]
        state.my_points    = self.points_b
        state.their_points = self.points_a
        return state

    def play_round(self):
        """
        Play a single round of the game, asking each strategy for their move, scoring points.
        """
        # Note that strategies receive a more restricted GameState view of the Game, so they can't
        # modify the game illegally or use hidden information like turn_limit.
        move_a = self.strategy_a(self.perspective_from_a())
        move_b = self.strategy_b(self.perspective_from_b())
        self.move_history.append((move_a, move_b))

        match move_a, move_b:
            case Move.SHARE, Move.SHARE:
                self.points_a += 3
                self.points_b += 3
            case Move.STEAL, Move.SHARE:
                self.points_a += 5
            case Move.SHARE, Move.STEAL:
                self.points_b += 5
            case Move.STEAL, Move.STEAL:
                self.points_a += 1
                self.points_b += 1

    def play_game(self) -> str:
        """
        Play a full game up to the turn limit, asking each strategy for their move.
        Returns the name of the winning strategy, or 'draw'.
        """
        while len(self.move_history) < self.turn_limit:
            self.play_round()

        if self.points_a > self.points_b:
            return self.strategy_a.__name__

        if self.points_a < self.points_b:
            return self.strategy_b.__name__

        return 'draw'

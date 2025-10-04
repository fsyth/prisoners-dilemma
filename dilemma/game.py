from dilemma.gamestate import GameState, Move
from dilemma.strategy import StrategyFunc


DRAW = '<draw>'


class Game:
    """A game playable by a pair of StrategyFuncs."""
    def __init__(self, strategy_a: StrategyFunc, strategy_b: StrategyFunc, turn_limit = 200):
        self.strategy_a = strategy_a
        self.strategy_b = strategy_b
        self.turn_limit = turn_limit

        self.move_history: list[tuple[Move, Move]] = []
        self.points_a = 0
        self.points_b = 0
        self.result: str | None = None

    def __str__(self) -> str:
        return f"""
        {self.strategy_a.__name__} ({self.points_a}) vs {self.strategy_b.__name__} ({self.points_b})
        Last 10 moves: {self.move_history[-10:]}
        Result: {self.result}
        """

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
            case Move.FORFEIT, Move.FORFEIT:
                self.result = DRAW
                return
            case Move.FORFEIT, _:
                self.result = self.strategy_b.__name__
                return
            case _, Move.FORFEIT:
                self.result = self.strategy_a.__name__
                return

        if len(self.move_history) < self.turn_limit:
            return

        if self.points_a > self.points_b:
            self.result = self.strategy_a.__name__
        elif self.points_a < self.points_b:
            self.result = self.strategy_b.__name__
        else:
            self.result = DRAW

    def play_game(self) -> str:
        """
        Play a full game up to the turn limit, asking each strategy for their move.
        Returns the name of the winning strategy, or '<draw>'.
        """
        while self.result is None:
            self.play_round()

        return self.result

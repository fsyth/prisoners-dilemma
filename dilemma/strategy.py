from dilemma.gamestate import Move, GameState
import strategies

import importlib
import pkgutil
from typing import Protocol


class StrategyFunc(Protocol):
    """A Strategy Function takes a GameState as a parameter and returns a Move."""
    def __call__(self, state: GameState) -> Move: ...


_registered_strategies: dict[str, StrategyFunc] = {}


def strategy(func: StrategyFunc) -> StrategyFunc:
    """Decorator to register a strategy for the tournament."""
    _registered_strategies[func.__name__] = func

    return func


def load_strategies() -> dict[str, StrategyFunc]:
    """Automatically import all strategies in the strategies package."""
    for _, name, _ in pkgutil.iter_modules(strategies.__path__):
        importlib.import_module(f'strategies.{name}')

    return _registered_strategies

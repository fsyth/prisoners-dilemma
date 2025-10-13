from dilemma.gamestate import Move, GameState
import strategies

from functools import wraps
from inspect import signature, _empty
from importlib import import_module
from pkgutil import iter_modules
from typing import Protocol


class StrategyFunc(Protocol):
    """A Strategy Function takes a GameState as a parameter and returns a Move."""
    def __call__(self, state: GameState) -> Move: ...


_registered_strategies: dict[str, StrategyFunc] = {}


def strategy(func: StrategyFunc) -> StrategyFunc:
    """Decorator to register a strategy for the tournament."""
    # Validate signature (import-time)
    sig = signature(func)
    params = list(sig.parameters.values())

    if len(params) != 1:
        raise TypeError(f"Strategy '{func.__name__}' must accept exactly one parameter, GameState.")

    param = params[0]
    if param.annotation is _empty:
        raise TypeError(f"Strategy '{func.__name__}' must annotate its parameter as GameState.")

    if param.annotation is not GameState:
        raise TypeError(f"Strategy '{func.__name__}' parameter must be GameState, got {param.annotation!r}")

    if sig.return_annotation is _empty:
        raise TypeError(f"Strategy '{func.__name__}' must annotate its return type as Move.")

    if sig.return_annotation is not Move:
        raise TypeError(f"Strategy '{func.__name__}' return type must be Move, got {sig.return_annotation!r}")

    if not func.__doc__:
        raise TypeError(f"Strategy '{func.__name__}' must include a docstring describing its behavior.")

    if func.__name__ in _registered_strategies:
        raise ValueError(f"Strategy '{func.__name__}' is already registered. Use a unique function name.")

    # Wrap func to validate runtime behavior
    @wraps(func)
    def wrapper(state: GameState) -> Move:
        try:
            move = func(state)
        except Exception as e:
            # Any exception counts as a forfeit
            print(f"{func.__name__} raised an error, forfeiting game:", e, state, sep='\n')
            return Move.FORFEIT

        if not isinstance(move, Move):
            print(f"{func.__name__} did not return a Move, forfeiting game:", state, sep='\n')
            return Move.FORFEIT

        return move

    _registered_strategies[func.__name__] = wrapper

    return wrapper


def load_strategies() -> dict[str, StrategyFunc]:
    """Automatically import all strategies in the strategies package."""
    for _, name, _ in iter_modules(strategies.__path__):
        import_module(f'strategies.{name}')

    return _registered_strategies

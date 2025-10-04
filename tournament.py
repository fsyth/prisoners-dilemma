from dilemma import Game, load_strategies

from itertools import combinations_with_replacement


class Record:
    def __init__(self):
        self.points = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
    
    def __str__(self):
        return f"{self.points} points, {self.wins} wins, {self.draws} draws, {self.losses} losses"


def run_tournament() -> dict[str, Record]:
    """
    Tournament to play every registered strategy against every strategy (including dittos).
    Returns records for each strategy of points accumulated across all games, wins, draws, losses.
    """
    strats = load_strategies()

    records = {name: Record() for name in strats.keys()}

    for strat_a, strat_b in combinations_with_replacement(strats.values(), 2):
        game = Game(strat_a, strat_b)
        game.play_game()

        record_a = records[strat_a.__name__]
        record_b = records[strat_b.__name__]

        record_a.points += game.points_a
        record_b.points += game.points_b

        if game.result == strat_a.__name__:
            record_a.wins += 1
            record_b.losses += 1
        elif game.result == strat_b.__name__:
            record_a.losses += 1
            record_b.wins += 1
        else:
            record_a.draws += 1
            record_b.draws += 1

    return records


if __name__ == '__main__':
    records = run_tournament()

    records = dict(sorted(records.items(), key=lambda item: item[1].points, reverse=True))

    print("\n=== Results ===")
    for name, record in records.items():
        print(f'{name:16} {record}')

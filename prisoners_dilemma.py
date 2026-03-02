from itertools import combinations
from strategies import (
    ALL_STRATEGIES, PAYOFF_MATRIX, COOPERATE, DEFECT,
    TEMPTATION, REWARD, PUNISHMENT, SUCKER,
)


def play_match(strategy_a, strategy_b, rounds, verbose=False):
    strategy_a.reset()
    strategy_b.reset()
    score_a = 0
    score_b = 0

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"  {strategy_a.name}  vs  {strategy_b.name}  ({rounds} rounds)")
        print(f"  [{strategy_a.alignment}/{strategy_a.forgiveness}] vs [{strategy_b.alignment}/{strategy_b.forgiveness}]")
        print(f"{'=' * 60}")
        print(f"{'Round':<8}{strategy_a.name:<16}{strategy_b.name:<16}{'Score':>10}")
        print("-" * 50)

    for round_num in range(1, rounds + 1):
        move_a = strategy_a.choose()
        move_b = strategy_b.choose()
        payoff_a, payoff_b = PAYOFF_MATRIX[(move_a, move_b)]
        score_a += payoff_a
        score_b += payoff_b
        strategy_a.update(move_a, move_b)
        strategy_b.update(move_b, move_a)

        if verbose:
            label_a = "Cooperate" if move_a == COOPERATE else "Defect"
            label_b = "Cooperate" if move_b == COOPERATE else "Defect"
            print(f"{round_num:<8}{label_a:<16}{label_b:<16}{score_a:>4} - {score_b:<4}")

    if verbose:
        print("-" * 50)
        print(f"{'FINAL':<8}{'':<16}{'':<16}{score_a:>4} - {score_b:<4}")

    return score_a, score_b


def run_tournament(strategies, rounds=200, verbose=False):
    scores = {strategy.name: 0 for strategy in strategies}

    for strategy_a, strategy_b in combinations(strategies, 2):
        score_a, score_b = play_match(strategy_a, strategy_b, rounds, verbose=verbose)
        scores[strategy_a.name] += score_a
        scores[strategy_b.name] += score_b

    return scores


def print_rankings(scores, strategies):
    strategy_lookup = {s.name: s for s in strategies}
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    print(f"\n{'Rank':<6}{'Strategy':<22}{'Score':<10}{'Alignment':<12}{'Forgiveness':<14}")
    print("-" * 64)
    for rank, (name, score) in enumerate(sorted_scores, start=1):
        s = strategy_lookup[name]
        print(f"{rank:<6}{name:<22}{score:<10}{s.alignment:<12}{s.forgiveness:<14}")
    print()


def main(rounds=200, verbose=False):
    strategies = [cls() for cls in ALL_STRATEGIES]

    print(f"Prisoner's Dilemma Tournament ({rounds} rounds per match)")
    print(f"Payoffs: T={TEMPTATION}, R={REWARD}, P={PUNISHMENT}, S={SUCKER}")
    print(f"Strategies: {len(strategies)}")

    print(f"\n{'Strategy':<22}{'Alignment':<12}{'Forgiveness':<14}")
    print("-" * 48)
    for s in strategies:
        print(f"{s.name:<22}{s.alignment:<12}{s.forgiveness:<14}")

    scores = run_tournament(strategies, rounds, verbose=verbose)
    print_rankings(scores, strategies)


if __name__ == "__main__":
    main(rounds=200, verbose=False)

from strategies.base import Strategy, COOPERATE, GOOD, FORGIVING


class TitForTat(Strategy):
    category = (GOOD, FORGIVING)

    def choose(self):
        if not self.opponent_history:
            return COOPERATE
        return self.opponent_history[-1]

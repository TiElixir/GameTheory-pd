from strategies.base import Strategy, COOPERATE, GOOD, FORGIVING


class AlwaysCooperate(Strategy):
    category = (GOOD, FORGIVING)

    def choose(self):
        return COOPERATE

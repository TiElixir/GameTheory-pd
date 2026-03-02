import random
from strategies.base import Strategy, COOPERATE, DEFECT, NEUTRAL, FORGIVING


class RandomStrategy(Strategy):
    category = (NEUTRAL, FORGIVING)

    def choose(self):
        return random.choice([COOPERATE, DEFECT])

import random
from strategies.base import Strategy, COOPERATE, DEFECT, EVIL, FORGIVING


class Joss(Strategy):
    category = (EVIL, FORGIVING)

    def __init__(self, sneak_rate=0.1):
        super().__init__()
        self.sneak_rate = sneak_rate

    def choose(self):
        if not self.opponent_history:
            return COOPERATE
        if self.opponent_history[-1] == COOPERATE:
            if random.random() < self.sneak_rate:
                return DEFECT
            return COOPERATE
        return DEFECT

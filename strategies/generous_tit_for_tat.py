import random
from strategies.base import Strategy, COOPERATE, DEFECT, GOOD, FORGIVING


class GenerousTitForTat(Strategy):
    category = (GOOD, FORGIVING)

    def __init__(self, forgiveness_rate=0.1):
        super().__init__()
        self.forgiveness_rate = forgiveness_rate

    def choose(self):
        if not self.opponent_history:
            return COOPERATE
        if self.opponent_history[-1] == DEFECT:
            if random.random() < self.forgiveness_rate:
                return COOPERATE
            return DEFECT
        return COOPERATE

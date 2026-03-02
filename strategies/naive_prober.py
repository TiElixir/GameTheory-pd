import random
from strategies.base import Strategy, COOPERATE, DEFECT, EVIL, FORGIVING


class NaiveProber(Strategy):
    category = (EVIL, FORGIVING)

    def __init__(self, probe_rate=0.1):
        super().__init__()
        self.probe_rate = probe_rate

    def choose(self):
        if not self.opponent_history:
            return COOPERATE
        if self.opponent_history[-1] == COOPERATE:
            if random.random() < self.probe_rate:
                return DEFECT
            return COOPERATE
        return DEFECT

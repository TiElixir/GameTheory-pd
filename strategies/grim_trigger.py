from strategies.base import Strategy, COOPERATE, DEFECT, GOOD, UNFORGIVING


class GrimTrigger(Strategy):
    category = (GOOD, UNFORGIVING)

    def choose(self):
        if DEFECT in self.opponent_history:
            return DEFECT
        return COOPERATE

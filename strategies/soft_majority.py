from strategies.base import Strategy, COOPERATE, DEFECT, GOOD, FORGIVING


class SoftMajority(Strategy):
    category = (GOOD, FORGIVING)

    def choose(self):
        if not self.opponent_history:
            return COOPERATE
        if self.opponent_history.count(DEFECT) > self.opponent_history.count(COOPERATE):
            return DEFECT
        return COOPERATE

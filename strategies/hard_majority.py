from strategies.base import Strategy, COOPERATE, DEFECT, EVIL, UNFORGIVING


class HardMajority(Strategy):
    category = (EVIL, UNFORGIVING)

    def choose(self):
        if not self.opponent_history:
            return DEFECT
        if self.opponent_history.count(DEFECT) >= self.opponent_history.count(COOPERATE):
            return DEFECT
        return COOPERATE

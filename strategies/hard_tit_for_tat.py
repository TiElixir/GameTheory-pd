from strategies.base import Strategy, COOPERATE, DEFECT, GOOD, UNFORGIVING


class HardTitForTat(Strategy):
    category = (GOOD, UNFORGIVING)

    def choose(self):
        if not self.opponent_history:
            return COOPERATE
        recent = self.opponent_history[-3:] if len(self.opponent_history) >= 3 else self.opponent_history
        if DEFECT in recent:
            return DEFECT
        return COOPERATE

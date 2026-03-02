from strategies.base import Strategy, COOPERATE, DEFECT, GOOD, FORGIVING


class TitForTwoTats(Strategy):
    category = (GOOD, FORGIVING)

    def choose(self):
        if len(self.opponent_history) < 2:
            return COOPERATE
        if self.opponent_history[-1] == DEFECT and self.opponent_history[-2] == DEFECT:
            return DEFECT
        return COOPERATE

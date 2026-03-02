from strategies.base import Strategy, DEFECT, EVIL, FORGIVING


class SuspiciousTitForTat(Strategy):
    category = (EVIL, FORGIVING)

    def choose(self):
        if not self.opponent_history:
            return DEFECT
        return self.opponent_history[-1]

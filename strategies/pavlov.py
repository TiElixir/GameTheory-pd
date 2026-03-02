from strategies.base import Strategy, COOPERATE, DEFECT, PAYOFF_MATRIX, REWARD, GOOD, FORGIVING


class Pavlov(Strategy):
    category = (GOOD, FORGIVING)

    def choose(self):
        if not self.my_history:
            return COOPERATE
        last_payoff = PAYOFF_MATRIX[(self.my_history[-1], self.opponent_history[-1])]
        if last_payoff[0] >= REWARD:
            return self.my_history[-1]
        return DEFECT if self.my_history[-1] == COOPERATE else COOPERATE

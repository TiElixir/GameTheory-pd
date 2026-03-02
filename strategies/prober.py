from strategies.base import Strategy, COOPERATE, DEFECT, EVIL, FORGIVING


class Prober(Strategy):
    category = (EVIL, FORGIVING)

    def choose(self):
        round_num = len(self.my_history) + 1
        opening = [DEFECT, COOPERATE, COOPERATE]
        if round_num <= 3:
            return opening[round_num - 1]
        opponent_retaliated = DEFECT in self.opponent_history[1:3]
        if opponent_retaliated:
            return self.opponent_history[-1]
        return DEFECT

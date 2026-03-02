from strategies.base import Strategy, COOPERATE, DEFECT, EVIL, UNFORGIVING


class Graaskamp(Strategy):
    category = (EVIL, UNFORGIVING)

    def choose(self):
        round_num = len(self.my_history) + 1
        if round_num <= 50 and round_num != 50:
            if not self.opponent_history:
                return COOPERATE
            return self.opponent_history[-1]
        if round_num == 50:
            return DEFECT
        if self.opponent_history:
            cooperate_count = self.opponent_history.count(COOPERATE)
            defect_count = self.opponent_history.count(DEFECT)
            if abs(cooperate_count - defect_count) <= len(self.opponent_history) * 0.1:
                return DEFECT
        if not self.opponent_history:
            return COOPERATE
        return self.opponent_history[-1]

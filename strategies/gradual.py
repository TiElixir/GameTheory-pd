from strategies.base import Strategy, COOPERATE, DEFECT, GOOD, FORGIVING


class Gradual(Strategy):
    category = (GOOD, FORGIVING)

    def __init__(self):
        super().__init__()
        self.punishments_remaining = 0
        self.cooperations_remaining = 0
        self.opponent_defections = 0

    def reset(self):
        super().reset()
        self.punishments_remaining = 0
        self.cooperations_remaining = 0
        self.opponent_defections = 0

    def update(self, my_move, opponent_move):
        super().update(my_move, opponent_move)
        if opponent_move == DEFECT and self.punishments_remaining == 0 and self.cooperations_remaining == 0:
            self.opponent_defections += 1
            self.punishments_remaining = self.opponent_defections
            self.cooperations_remaining = 2

    def choose(self):
        if not self.my_history:
            return COOPERATE
        if self.punishments_remaining > 0:
            self.punishments_remaining -= 1
            return DEFECT
        if self.cooperations_remaining > 0:
            self.cooperations_remaining -= 1
            return COOPERATE
        return COOPERATE

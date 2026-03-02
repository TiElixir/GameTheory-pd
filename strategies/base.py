TEMPTATION = 5
REWARD = 3
PUNISHMENT = 1
SUCKER = 0

COOPERATE = "C"
DEFECT = "D"

PAYOFF_MATRIX = {
    (COOPERATE, COOPERATE): (REWARD, REWARD),
    (COOPERATE, DEFECT): (SUCKER, TEMPTATION),
    (DEFECT, COOPERATE): (TEMPTATION, SUCKER),
    (DEFECT, DEFECT): (PUNISHMENT, PUNISHMENT),
}

GOOD = "Good"
EVIL = "Evil"
NEUTRAL = "Neutral"
FORGIVING = "Forgiving"
UNFORGIVING = "Unforgiving"


class Strategy:
    category = (NEUTRAL, FORGIVING)

    def __init__(self):
        self.my_history = []
        self.opponent_history = []

    def choose(self):
        raise NotImplementedError

    def update(self, my_move, opponent_move):
        self.my_history.append(my_move)
        self.opponent_history.append(opponent_move)

    def reset(self):
        self.my_history = []
        self.opponent_history = []

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def alignment(self):
        return self.category[0]

    @property
    def forgiveness(self):
        return self.category[1]

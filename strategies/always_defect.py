from strategies.base import Strategy, DEFECT, EVIL, UNFORGIVING


class AlwaysDefect(Strategy):
    category = (EVIL, UNFORGIVING)

    def choose(self):
        return DEFECT

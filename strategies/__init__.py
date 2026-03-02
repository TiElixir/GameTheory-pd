from strategies.base import (
    Strategy, PAYOFF_MATRIX, COOPERATE, DEFECT,
    TEMPTATION, REWARD, PUNISHMENT, SUCKER,
    GOOD, EVIL, NEUTRAL, FORGIVING, UNFORGIVING,
)
from strategies.always_cooperate import AlwaysCooperate
from strategies.always_defect import AlwaysDefect
from strategies.tit_for_tat import TitForTat
from strategies.random_strategy import RandomStrategy
from strategies.grim_trigger import GrimTrigger
from strategies.pavlov import Pavlov
from strategies.generous_tit_for_tat import GenerousTitForTat
from strategies.suspicious_tit_for_tat import SuspiciousTitForTat
from strategies.tit_for_two_tats import TitForTwoTats
from strategies.joss import Joss
from strategies.graaskamp import Graaskamp
from strategies.detective import Detective
from strategies.hard_majority import HardMajority
from strategies.soft_majority import SoftMajority
from strategies.prober import Prober
from strategies.hard_tit_for_tat import HardTitForTat
from strategies.naive_prober import NaiveProber
from strategies.gradual import Gradual
from strategies.ai_strategy import AIStrategy

ALL_STRATEGIES = [
    AlwaysCooperate, AlwaysDefect, TitForTat, RandomStrategy,
    GrimTrigger, Pavlov, GenerousTitForTat, SuspiciousTitForTat,
    TitForTwoTats, Joss, Graaskamp, Detective, HardMajority,
    SoftMajority, Prober, HardTitForTat, NaiveProber, Gradual,
    AIStrategy,
]

import torch
import torch.nn as nn
import os
import random
from strategies.base import Strategy, COOPERATE, DEFECT, PAYOFF_MATRIX, GOOD, FORGIVING


MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ai_model.pt")

PROBE_MOVES = [COOPERATE, DEFECT, COOPERATE, COOPERATE, DEFECT,
               COOPERATE, DEFECT, DEFECT, COOPERATE, COOPERATE,
               DEFECT, COOPERATE, COOPERATE, DEFECT, COOPERATE,
               DEFECT, COOPERATE, COOPERATE, COOPERATE, DEFECT]
PROBE_LENGTH = len(PROBE_MOVES)


def encode_move(move):
    return 1.0 if move == COOPERATE else 0.0


class OpponentClassifier(nn.Module):
    def __init__(self, input_size=48, num_classes=18):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.BatchNorm1d(128),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.BatchNorm1d(64),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes),
        )

    def forward(self, x):
        return self.net(x)


COUNTER_STRATEGIES = {
    "AlwaysCooperate": "exploit",
    "AlwaysDefect": "defect",
    "TitForTat": "cooperate",
    "RandomStrategy": "defect",
    "GrimTrigger": "cooperate",
    "Pavlov": "cooperate",
    "GenerousTitForTat": "cooperate",
    "SuspiciousTitForTat": "tit_for_tat",
    "TitForTwoTats": "slow_exploit",
    "Joss": "cooperate",
    "Graaskamp": "tit_for_tat",
    "Detective": "tit_for_tat",
    "HardMajority": "cooperate",
    "SoftMajority": "cooperate",
    "Prober": "tit_for_tat",
    "HardTitForTat": "cooperate",
    "NaiveProber": "cooperate",
    "Gradual": "cooperate",
}


def extract_features(my_history, opp_history, probe_length):
    features = []
    for i in range(probe_length):
        features.append(encode_move(my_history[i]))
        features.append(encode_move(opp_history[i]))

    opp_coops = sum(1 for m in opp_history[:probe_length] if m == COOPERATE)
    opp_defects = probe_length - opp_coops
    features.append(opp_coops / probe_length)
    features.append(opp_defects / probe_length)

    retaliations = 0
    forgives = 0
    copies = 0
    for i in range(1, probe_length):
        if my_history[i-1] == DEFECT and opp_history[i] == DEFECT:
            retaliations += 1
        if my_history[i-1] == DEFECT and opp_history[i] == COOPERATE:
            forgives += 1
        if opp_history[i] == my_history[i-1]:
            copies += 1

    features.append(retaliations / max(probe_length - 1, 1))
    features.append(forgives / max(probe_length - 1, 1))
    features.append(copies / max(probe_length - 1, 1))

    first_move = encode_move(opp_history[0])
    features.append(first_move)

    streak = 0
    for m in opp_history[:probe_length]:
        if m == opp_history[0]:
            streak += 1
        else:
            break
    features.append(streak / probe_length)

    switches = sum(1 for i in range(1, probe_length) if opp_history[i] != opp_history[i-1])
    features.append(switches / max(probe_length - 1, 1))

    return features


class AIStrategy(Strategy):
    category = (GOOD, FORGIVING)

    def __init__(self, model=None, deterministic=True):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.classifier = OpponentClassifier().to(self.device)
        self.classified_opponent = None
        self.counter_mode = None
        self.class_names = sorted(COUNTER_STRATEGIES.keys())
        self.exploit_toggle = True

        if model is not None:
            self.classifier = model.to(self.device)
        else:
            self.load_model()

    def load_model(self):
        model_path = os.path.normpath(MODEL_PATH)
        if os.path.exists(model_path):
            self.classifier.load_state_dict(
                torch.load(model_path, map_location=self.device, weights_only=True)
            )
        self.classifier.eval()

    def reset(self):
        super().reset()
        self.classified_opponent = None
        self.counter_mode = None
        self.exploit_toggle = True

    def classify_opponent(self):
        features = extract_features(self.my_history, self.opponent_history, PROBE_LENGTH)
        x = torch.tensor([features], device=self.device, dtype=torch.float32)
        self.classifier.eval()
        with torch.no_grad():
            logits = self.classifier(x)
            pred = torch.argmax(logits, dim=1).item()

        self.classified_opponent = self.class_names[pred]
        self.counter_mode = COUNTER_STRATEGIES.get(self.classified_opponent, "tit_for_tat")

    def choose(self):
        round_num = len(self.my_history)

        if round_num < PROBE_LENGTH:
            return PROBE_MOVES[round_num]

        if self.classified_opponent is None:
            self.classify_opponent()

        return self.counter_move()

    def counter_move(self):
        if self.counter_mode == "cooperate":
            return COOPERATE

        if self.counter_mode == "defect":
            return DEFECT

        if self.counter_mode == "exploit":
            return DEFECT

        if self.counter_mode == "tit_for_tat":
            if not self.opponent_history:
                return COOPERATE
            return self.opponent_history[-1]

        if self.counter_mode == "retaliate_then_cooperate":
            if self.opponent_history and self.opponent_history[-1] == DEFECT:
                return DEFECT
            return COOPERATE

        if self.counter_mode == "slow_exploit":
            self.exploit_toggle = not self.exploit_toggle
            if self.exploit_toggle:
                return DEFECT
            return COOPERATE

        return self.opponent_history[-1] if self.opponent_history else COOPERATE

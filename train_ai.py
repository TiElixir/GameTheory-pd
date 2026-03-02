import torch
import torch.nn as nn
import torch.optim as optim
from tqdm import tqdm
from strategies.base import PAYOFF_MATRIX, COOPERATE, DEFECT
from strategies.ai_strategy import (
    OpponentClassifier, PROBE_MOVES, PROBE_LENGTH,
    encode_move, COUNTER_STRATEGIES, MODEL_PATH,
    extract_features
)
from strategies import ALL_STRATEGIES


EPOCHS = 300
LR = 1e-3
SAMPLES_PER_OPPONENT = 500
ROUNDS_PER_MATCH = 200


def generate_probe_data(opponent_cls, probe_moves):
    opponent = opponent_cls()
    my_history = []
    opp_history = []
    for i in range(PROBE_LENGTH):
        my_move = probe_moves[i]
        opp_move = opponent.choose()
        my_history.append(my_move)
        opp_history.append(opp_move)
        opponent.update(opp_move, my_move)
    
    return extract_features(my_history, opp_history, PROBE_LENGTH)


def build_dataset(opponent_classes, samples_per_opponent):
    class_names = sorted(COUNTER_STRATEGIES.keys())
    class_to_idx = {name: i for i, name in enumerate(class_names)}

    all_features = []
    all_labels = []

    for opp_cls in opponent_classes:
        name = opp_cls.__name__
        if name not in class_to_idx:
            continue
        idx = class_to_idx[name]

        for _ in range(samples_per_opponent):
            features = generate_probe_data(opp_cls, PROBE_MOVES)
            all_features.append(features)
            all_labels.append(idx)

    features_tensor = torch.tensor(all_features, dtype=torch.float32)
    labels_tensor = torch.tensor(all_labels, dtype=torch.long)
    return features_tensor, labels_tensor, class_names


def evaluate_ai(model, opponent_classes, class_names, device):
    class_to_idx = {name: i for i, name in enumerate(class_names)}
    model.eval()

    total_score = 0
    results = []

    for opp_cls in opponent_classes:
        name = opp_cls.__name__
        if name == "AIStrategy" or name not in COUNTER_STRATEGIES:
            continue

        opponent = opp_cls()
        my_history = []
        opp_history = []

        for i in range(PROBE_LENGTH):
            my_move = PROBE_MOVES[i]
            opp_move = opponent.choose()
            my_history.append(my_move)
            opp_history.append(opp_move)
            opponent.update(opp_move, my_move)

        features = extract_features(my_history, opp_history, PROBE_LENGTH)

        x = torch.tensor([features], device=device, dtype=torch.float32)
        with torch.no_grad():
            logits = model(x)
            pred = torch.argmax(logits, dim=1).item()

        predicted_name = class_names[pred]
        correct = predicted_name == name
        counter = COUNTER_STRATEGIES.get(predicted_name, "tit_for_tat")

        score_ai, score_opp = 0, 0
        for i in range(PROBE_LENGTH):
            pa, po = PAYOFF_MATRIX[(my_history[i], opp_history[i])]
            score_ai += pa
            score_opp += po

        for _ in range(ROUNDS_PER_MATCH - PROBE_LENGTH):
            if counter == "cooperate":
                my_move = COOPERATE
            elif counter == "defect" or counter == "exploit":
                my_move = DEFECT
            elif counter == "retaliate_then_cooperate":
                my_move = DEFECT if opp_history[-1] == DEFECT else COOPERATE
            elif counter == "slow_exploit":
                my_move = DEFECT if len(my_history) % 2 == 0 else COOPERATE
            else:
                my_move = opp_history[-1]

            opp_move = opponent.choose()
            pa, po = PAYOFF_MATRIX[(my_move, opp_move)]
            score_ai += pa
            score_opp += po
            my_history.append(my_move)
            opp_history.append(opp_move)
            opponent.update(opp_move, my_move)

        total_score += score_ai
        result = "WIN" if score_ai > score_opp else ("TIE" if score_ai == score_opp else "LOSE")
        tag = "OK" if correct else "WRONG"
        results.append((name, predicted_name, score_ai, score_opp, result, tag))

    return total_score, results


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    opponent_classes = [cls for cls in ALL_STRATEGIES if cls.__name__ != "AIStrategy"]

    print(f"Generating training data ({SAMPLES_PER_OPPONENT} samples per opponent)...")
    features, labels, class_names = build_dataset(opponent_classes, SAMPLES_PER_OPPONENT)
    features = features.to(device)
    labels = labels.to(device)
    print(f"Dataset: {features.shape[0]} samples, {features.shape[1]} features, {len(class_names)} classes")

    model = OpponentClassifier(input_size=features.shape[1], num_classes=len(class_names)).to(device)
    optimizer = optim.Adam(model.parameters(), lr=LR)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=100, gamma=0.5)
    criterion = nn.CrossEntropyLoss()

    print(f"\nTraining classifier for {EPOCHS} epochs...")
    print(f"{'='*60}")

    pbar = tqdm(range(1, EPOCHS + 1), desc="Training")
    for epoch in pbar:
        model.train()
        perm = torch.randperm(features.shape[0], device=device)
        features_shuffled = features[perm]
        labels_shuffled = labels[perm]

        batch_size = 128
        total_loss = 0.0
        correct = 0
        total = 0

        for i in range(0, features.shape[0], batch_size):
            batch_x = features_shuffled[i:i+batch_size]
            batch_y = labels_shuffled[i:i+batch_size]

            logits = model(batch_x)
            loss = criterion(logits, batch_y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item() * batch_x.shape[0]
            preds = torch.argmax(logits, dim=1)
            correct += (preds == batch_y).sum().item()
            total += batch_x.shape[0]

        scheduler.step()
        acc = correct / total * 100
        avg_loss = total_loss / total
        pbar.set_postfix({"Acc": f"{acc:.1f}%", "Loss": f"{avg_loss:.4f}"})

        if epoch % 50 == 0 or epoch == 1:
            tqdm.write(f"Epoch {epoch:>4d} | Acc: {acc:.1f}% | Loss: {avg_loss:.4f}")

    torch.save(model.state_dict(), MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

    print(f"\n{'='*60}")
    print(f"Final Evaluation (200 rounds per match)")
    print(f"{'='*60}")

    total_score, results = evaluate_ai(model, opponent_classes, class_names, device)

    for name, pred, score_ai, score_opp, result, tag in results:
        pred_str = f"(detected: {pred})" if tag == "OK" else f"(MISID: {pred})"
        print(f"  AI vs {name:<22s}  AI: {score_ai:>4d}  Opp: {score_opp:>4d}  [{result}]  {pred_str}")

    wins = sum(1 for _, _, _, _, r, _ in results if r == "WIN")
    ties = sum(1 for _, _, _, _, r, _ in results if r == "TIE")
    losses = sum(1 for _, _, _, _, r, _ in results if r == "LOSE")
    accuracy = sum(1 for _, _, _, _, _, t in results if t == "OK") / len(results) * 100

    print(f"\n  Total AI Score: {total_score}")
    print(f"  Record: {wins}W / {ties}T / {losses}L")
    print(f"  Classifier Accuracy: {accuracy:.1f}%")


if __name__ == "__main__":
    main()

# Prisoner's Dilemma Simulator

A comprehensive simulation and analysis of the Iterated Prisoner's Dilemma, featuring 19 strategies, a PyTorch-based AI, and a modern GUI.

![Simulation GUI](https://raw.githubusercontent.com/TiElixir/GameTheory-pd/main/screenshot.png) *(Note: Placeholder link, replace with actual screenshot if available)*

## 🎮 Features

- **19 Different Strategies**: From classic Tit-For-Tat to complex "Gradual" and "Detective" strategies.
- **AI Opponent Recognition**: A neural-network-backed strategy that identifies its opponent during a probe phase and switches to the optimal counter-strategy.
- **Interactive GUI**: Round-by-round visualization, tournament leaderboards, and strategy categorization (Good/Evil, Forgiving/Unforgiving).
- **Fast CLI Tournament**: Run massive round-robin tournaments in seconds via the terminal.
- **Statistical Features**: Strategies are categorized based on their behavior, helping you understand why "Nice" strategies often finish first.

## ⚖️ Payoff Matrix

The simulation follows the standard Prisoner's Dilemma payoffs:

| Decision | Opponent Cooperates | Opponent Defects |
| :--- | :--- | :--- |
| **You Cooperate** | **REWARD (3, 3)** | **SUCKER (0, 5)** |
| **You Defect** | **TEMPTATION (5, 0)** | **PUNISHMENT (1, 1)** |

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PyTorch (for the AI strategy)
- Tqdm (for training progress)
- Tkinter (usually comes with Python)

```bash
pip install torch tqdm
```

### Running the Simulator
- **Launch the GUI**: `python gui.py`
- **Run a CLI Tournament**: `python prisoners_dilemma.py`
- **Train the AI model**: `python train_ai.py`

## 🧠 AI Strategy (LSTM Classified Counter)

The **AIStrategy** does not just follow a static rule. It uses a 20-round **Probe Phase** to analyze the opponent.
1. **Probe**: Plays a diagnostic sequence of moves to see how the opponent reacts.
2. **Classify**: Uses a trained **OpponentClassifier** (MLP with 48 statistical features) to identify which strategy it is facing.
3. **Counter**: Immediately switches to the mathematically optimal counter-play (e.g., pure exploitation for `AlwaysCooperate`, or strict Tit-For-Tat for `Detective`).

## 📂 Project Structure

- `gui.py`: The Tkinter-based dashboard.
- `prisoners_dilemma.py`: Core simulation logic and CLI entry point.
- `train_ai.py`: Supervised training loop for the AI classifier.
- `strategies/`: Package containing individual strategy implementations.
  - `ai_strategy.py`: The PyTorch model and AI logic.
  - `base.py`: The `Strategy` base class and game constants.
  - `...`: 18 individual strategy files.

## 📜 Strategies Included

1.  **AlwaysCooperate**: The easiest to exploit.
2.  **AlwaysDefect**: The classic "Evil" strategy.
3.  **TitForTat**: The legendary winner—starts nice, then copies you.
4.  **GrimTrigger**: Forgives nothing. One defection and it's over.
5.  **Pavlov**: (Win-Stay, Lose-Shift).
6.  **GenerousTitForTat**: Tit-For-Tat with a 10% chance to forgive.
7.  **Gradual**: Calibrates its retaliation based on the number of times it has been betrayed.
8.  **Detective**: Probes you early; if you don't fight back, it exploits you forever.
9.  **AIStrategy**: Our custom neural network strategy.
... and 10 others.

---
Created by Antigravity AI for Game Theory research.

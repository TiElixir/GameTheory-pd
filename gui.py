import tkinter as tk
from tkinter import ttk
import os
from itertools import combinations
from strategies import (
    ALL_STRATEGIES, PAYOFF_MATRIX, COOPERATE, DEFECT,
    GOOD, EVIL, NEUTRAL, FORGIVING, UNFORGIVING,
)
from strategies.ai_strategy import MODEL_PATH, PROBE_LENGTH


BG_DARK = "#0f0f1a"
BG_CARD = "#1a1a2e"
BG_INPUT = "#16213e"
FG_TEXT = "#e0e0e0"
FG_DIM = "#8888aa"
FG_HEADER = "#ffffff"
ACCENT = "#7c3aed"
ACCENT_HOVER = "#9333ea"
GREEN = "#22c55e"
RED = "#ef4444"
GOLD = "#facc15"
BLUE = "#3b82f6"
CYAN = "#06b6d4"
BORDER = "#2a2a4a"


class PrisonersDilemmaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Prisoner's Dilemma Simulator")
        self.root.configure(bg=BG_DARK)
        self.root.geometry("1100x820")
        self.root.minsize(950, 700)

        self.strategy_map = {cls.__name__: cls for cls in ALL_STRATEGIES}
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()
        self.build_ui()

    def configure_styles(self):
        self.style.configure("Title.TLabel", background=BG_DARK, foreground=FG_HEADER,
                             font=("Segoe UI", 20, "bold"))
        self.style.configure("Sub.TLabel", background=BG_DARK, foreground=FG_DIM,
                             font=("Segoe UI", 10))
        self.style.configure("Card.TFrame", background=BG_CARD)
        self.style.configure("Dark.TFrame", background=BG_DARK)
        self.style.configure("Field.TLabel", background=BG_CARD, foreground=FG_TEXT,
                             font=("Segoe UI", 11))
        self.style.configure("Score.TLabel", background=BG_DARK, foreground=GOLD,
                             font=("Segoe UI", 13, "bold"))
        self.style.configure("TagGood.TLabel", background=BG_DARK, foreground=GREEN,
                             font=("Segoe UI", 10, "bold"))
        self.style.configure("TagEvil.TLabel", background=BG_DARK, foreground=RED,
                             font=("Segoe UI", 10, "bold"))
        self.style.configure("TagNeutral.TLabel", background=BG_DARK, foreground=FG_DIM,
                             font=("Segoe UI", 10, "bold"))
        self.style.configure("TagAI.TLabel", background=BG_DARK, foreground=CYAN,
                             font=("Segoe UI", 10, "bold"))
        self.style.configure("AIStatus.TLabel", background=BG_DARK, foreground=CYAN,
                             font=("Segoe UI", 9))
        self.style.configure("Custom.TCombobox", fieldbackground=BG_INPUT,
                             background=BG_INPUT, foreground=FG_TEXT,
                             selectbackground=ACCENT, selectforeground="#fff",
                             arrowcolor=FG_TEXT)
        self.style.map("Custom.TCombobox",
                       fieldbackground=[("readonly", BG_INPUT)],
                       selectbackground=[("readonly", ACCENT)])
        self.style.configure("Treeview", background=BG_CARD, foreground=FG_TEXT,
                             fieldbackground=BG_CARD, rowheight=26,
                             font=("Consolas", 10), borderwidth=0)
        self.style.configure("Treeview.Heading", background=BG_INPUT, foreground=FG_HEADER,
                             font=("Segoe UI", 10, "bold"), borderwidth=0)
        self.style.map("Treeview", background=[("selected", ACCENT)],
                       foreground=[("selected", "#fff")])

    def build_ui(self):
        header = ttk.Frame(self.root, style="Dark.TFrame")
        header.pack(fill="x", padx=24, pady=(18, 4))
        ttk.Label(header, text="Prisoner's Dilemma", style="Title.TLabel").pack(anchor="w")
        sub_frame = ttk.Frame(header, style="Dark.TFrame")
        sub_frame.pack(anchor="w", fill="x")
        ttk.Label(sub_frame, text=f"Game Theory Simulation  |  T=5  R=3  P=1  S=0  |  {len(ALL_STRATEGIES)} Strategies",
                  style="Sub.TLabel").pack(side="left")

        ai_trained = os.path.exists(os.path.normpath(MODEL_PATH))
        ai_status = "LSTM Model Loaded" if ai_trained else "AI Model Not Trained"
        self.ai_status_label = ttk.Label(sub_frame, text=f"  [AI: {ai_status}]",
                                          style="AIStatus.TLabel")
        self.ai_status_label.pack(side="left", padx=(10, 0))

        controls = ttk.Frame(self.root, style="Card.TFrame")
        controls.pack(fill="x", padx=24, pady=12, ipady=8)
        inner = ttk.Frame(controls, style="Card.TFrame")
        inner.pack(padx=16, pady=8, fill="x")

        names = sorted(self.strategy_map.keys())

        ttk.Label(inner, text="Strategy A", style="Field.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 4))
        self.combo_a = ttk.Combobox(inner, values=names, state="readonly",
                                    style="Custom.TCombobox", width=20, font=("Segoe UI", 11))
        self.combo_a.set("AIStrategy")
        self.combo_a.grid(row=0, column=1, padx=4, pady=4)
        self.combo_a.bind("<<ComboboxSelected>>", lambda e: self.update_tags())

        ttk.Label(inner, text="vs", style="Field.TLabel").grid(row=0, column=2, padx=4)

        ttk.Label(inner, text="Strategy B", style="Field.TLabel").grid(row=0, column=3, sticky="w", padx=(4, 4))
        self.combo_b = ttk.Combobox(inner, values=names, state="readonly",
                                    style="Custom.TCombobox", width=20, font=("Segoe UI", 11))
        self.combo_b.set("AlwaysDefect")
        self.combo_b.grid(row=0, column=4, padx=4, pady=4)
        self.combo_b.bind("<<ComboboxSelected>>", lambda e: self.update_tags())

        ttk.Label(inner, text="Rounds", style="Field.TLabel").grid(row=0, column=5, sticky="w", padx=(16, 4))
        self.rounds_var = tk.StringVar(value="200")
        self.rounds_entry = tk.Entry(inner, textvariable=self.rounds_var, width=6,
                                     bg=BG_INPUT, fg=FG_TEXT, insertbackground=FG_TEXT,
                                     font=("Segoe UI", 11), bd=0, highlightthickness=1,
                                     highlightcolor=ACCENT, highlightbackground=BORDER)
        self.rounds_entry.grid(row=0, column=6, padx=4, pady=4)

        self.run_btn = tk.Button(inner, text="Run Match", bg=ACCENT, fg="#fff",
                                 activebackground=ACCENT_HOVER, activeforeground="#fff",
                                 font=("Segoe UI", 11, "bold"), bd=0, padx=14, pady=5,
                                 cursor="hand2", command=self.run_match)
        self.run_btn.grid(row=0, column=7, padx=(16, 6), pady=4)

        self.tournament_btn = tk.Button(inner, text="Tournament", bg=BG_INPUT, fg=GOLD,
                                        activebackground=ACCENT, activeforeground="#fff",
                                        font=("Segoe UI", 11, "bold"), bd=0, padx=14, pady=5,
                                        cursor="hand2", command=self.run_tournament)
        self.tournament_btn.grid(row=0, column=8, padx=4, pady=4)

        tags_frame = ttk.Frame(self.root, style="Dark.TFrame")
        tags_frame.pack(fill="x", padx=24, pady=(0, 2))
        self.tag_a_label = ttk.Label(tags_frame, text="", style="TagAI.TLabel")
        self.tag_a_label.pack(side="left", padx=(0, 20))
        self.tag_b_label = ttk.Label(tags_frame, text="", style="TagGood.TLabel")
        self.tag_b_label.pack(side="left", padx=(0, 20))
        self.score_label = ttk.Label(tags_frame, text="", style="Score.TLabel")
        self.score_label.pack(side="right")
        self.update_tags()

        table_frame = ttk.Frame(self.root, style="Dark.TFrame")
        table_frame.pack(fill="both", expand=True, padx=24, pady=(4, 18))

        self.tree = ttk.Treeview(table_frame, columns=("round", "move_a", "move_b", "score"),
                                 show="headings", selectmode="browse")
        self.tree.heading("round", text="Round")
        self.tree.heading("move_a", text="Strategy A")
        self.tree.heading("move_b", text="Strategy B")
        self.tree.heading("score", text="Running Score")
        self.tree.column("round", width=70, anchor="center")
        self.tree.column("move_a", width=250, anchor="center")
        self.tree.column("move_b", width=250, anchor="center")
        self.tree.column("score", width=160, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.tag_configure("cooperate", foreground=GREEN)
        self.tree.tag_configure("defect", foreground=RED)
        self.tree.tag_configure("mixed", foreground=FG_TEXT)
        self.tree.tag_configure("probe", foreground=FG_DIM, font=("Consolas", 10, "italic"))
        self.tree.tag_configure("final", foreground=GOLD, font=("Consolas", 10, "bold"))
        self.tree.tag_configure("tournament", foreground=FG_TEXT)
        self.tree.tag_configure("rank1", foreground=GOLD, font=("Consolas", 10, "bold"))
        self.tree.tag_configure("good", foreground=GREEN)
        self.tree.tag_configure("evil", foreground=RED)
        self.tree.tag_configure("neutral", foreground=FG_DIM)
        self.tree.tag_configure("ai", foreground=CYAN, font=("Consolas", 10, "bold"))

    def get_tag_style(self, name):
        if name == "AIStrategy":
            return "TagAI.TLabel"
        s = self.strategy_map[name]()
        return f"Tag{s.alignment}.TLabel"

    def get_category_text(self, name):
        if name == "AIStrategy":
            return "AI | Classifier + Counter"
        s = self.strategy_map[name]()
        return f"{s.alignment} | {s.forgiveness}"

    def update_tags(self):
        name_a = self.combo_a.get()
        name_b = self.combo_b.get()
        if name_a in self.strategy_map:
            style = self.get_tag_style(name_a)
            text = self.get_category_text(name_a)
            self.tag_a_label.config(text=f"A: {text}", style=style)
        if name_b in self.strategy_map:
            style = self.get_tag_style(name_b)
            text = self.get_category_text(name_b)
            self.tag_b_label.config(text=f"B: {text}", style=style)

    def get_rounds(self):
        try:
            return max(1, int(self.rounds_var.get()))
        except ValueError:
            return 200

    def run_match(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        name_a = self.combo_a.get()
        name_b = self.combo_b.get()
        rounds = self.get_rounds()

        strategy_a = self.strategy_map[name_a]()
        strategy_b = self.strategy_map[name_b]()

        self.tree.heading("round", text="Round")
        self.tree.heading("move_a", text=name_a)
        self.tree.heading("move_b", text=name_b)
        self.tree.heading("score", text="Running Score")

        score_a, score_b = 0, 0
        ai_detected = None

        for round_num in range(1, rounds + 1):
            move_a = strategy_a.choose()
            move_b = strategy_b.choose()
            payoff_a, payoff_b = PAYOFF_MATRIX[(move_a, move_b)]
            score_a += payoff_a
            score_b += payoff_b
            strategy_a.update(move_a, move_b)
            strategy_b.update(move_b, move_a)

            label_a = "Cooperate" if move_a == COOPERATE else "Defect"
            label_b = "Cooperate" if move_b == COOPERATE else "Defect"

            tag = "mixed"
            if round_num <= PROBE_LENGTH and (name_a == "AIStrategy" or name_b == "AIStrategy"):
                tag = "probe"
            elif move_a == COOPERATE and move_b == COOPERATE:
                tag = "cooperate"
            elif move_a == DEFECT and move_b == DEFECT:
                tag = "defect"
            
            # Extract info if AI detected someone
            if name_a == "AIStrategy" and round_num == PROBE_LENGTH + 1:
                ai_detected = strategy_a.classified_opponent
                label_a += f" (ID: {ai_detected})"
            if name_b == "AIStrategy" and round_num == PROBE_LENGTH + 1:
                det = strategy_b.classified_opponent
                label_b += f" (ID: {det})"

            self.tree.insert("", "end", values=(
                round_num, label_a, label_b, f"{score_a} - {score_b}"
            ), tags=(tag,))

        winner = name_a if score_a > score_b else (name_b if score_b > score_a else "TIE")
        self.tree.insert("", "end", values=(
            "FINAL", "-", "-", f"{score_a} - {score_b}"
        ), tags=("final",))

        status_text = f"Result:  {name_a} {score_a}  vs  {name_b} {score_b}  [{winner}]"
        if ai_detected:
            status_text += f"  |  AI Detection: {ai_detected}"
        
        self.score_label.config(text=status_text)
        self.update_tags()
        self.tree.yview_moveto(0)

    def run_tournament(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        rounds = self.get_rounds()
        strategies = [cls() for cls in ALL_STRATEGIES]
        scores = {s.name: 0 for s in strategies}

        self.tree.heading("round", text="Rank")
        self.tree.heading("move_a", text="Strategy")
        self.tree.heading("move_b", text="Category")
        self.tree.heading("score", text="Total Score")

        for sa, sb in combinations(strategies, 2):
            sa.reset()
            sb.reset()
            sc_a, sc_b = 0, 0
            for _ in range(rounds):
                ma = sa.choose()
                mb = sb.choose()
                pa, pb = PAYOFF_MATRIX[(ma, mb)]
                sc_a += pa
                sc_b += pb
                sa.update(ma, mb)
                sb.update(mb, ma)
            scores[sa.name] += sc_a
            scores[sb.name] += sc_b

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        lookup = {cls.__name__: cls for cls in ALL_STRATEGIES}

        for rank, (name, score) in enumerate(ranked, 1):
            category = self.get_category_text(name)
            if rank == 1:
                tag = "rank1"
            elif name == "AIStrategy":
                tag = "ai"
            else:
                s = lookup[name]()
                tag = s.alignment.lower()
            self.tree.insert("", "end", values=(
                f"#{rank}", name, category, score
            ), tags=(tag,))

        winner_name = ranked[0][0]
        winner_score = ranked[0][1]

        ai_rank_raw = [i for i, (n, _) in enumerate(ranked, 1) if n == "AIStrategy"]
        ai_rank = ai_rank_raw[0] if ai_rank_raw else "?"
        ai_score = next((s for n, s in ranked if n == "AIStrategy"), 0)

        self.score_label.config(
            text=f"Winner: {winner_name} ({winner_score} pts)  |  AI Rank: #{ai_rank} ({ai_score} pts)"
        )
        self.tree.yview_moveto(0)


if __name__ == "__main__":
    root = tk.Tk()
    PrisonersDilemmaGUI(root)
    root.mainloop()

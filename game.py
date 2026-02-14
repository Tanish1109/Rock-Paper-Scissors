import tkinter as tk
import random
from tkinter import ttk

# --- Game Logic ---
choices = ["Rock", "Paper", "Scissors"]
score_user = 0
score_comp = 0
rounds_played = 0
max_rounds = 5
total_games = 0
total_wins = 0
total_losses = 0
total_ties = 0
rounds_completed = 0
player_name = "Player"

def play(user_choice, btn=None):
    global score_user, score_comp, rounds_played, total_games, total_wins, total_losses, total_ties, rounds_completed
    comp_choice = random.choice(choices)
    rounds_played += 1

    if user_choice == comp_choice:
        result.set(f"Draw! Both chose {user_choice}")
    elif (user_choice == "Rock" and comp_choice == "Scissors") or \
         (user_choice == "Paper" and comp_choice == "Rock") or \
         (user_choice == "Scissors" and comp_choice == "Paper"):
        score_user += 1
        result.set(f"You Win! {user_choice} beats {comp_choice}")
        launch_full_confetti()   # 🎉 trigger confetti immediately on every round win
    else:
        score_comp += 1
        result.set(f"You Lose! {comp_choice} beats {user_choice}")

    score_label.config(text=f"{player_name}: {score_user} | Computer: {score_comp}")

    if btn:
        bounce(btn)

    progress['value'] = (rounds_played / max_rounds) * 100

    # Match end logic (leaderboard + stats)
    if rounds_played == max_rounds:
        total_games += 1
        rounds_completed += 1
        round_label.config(text=f"Rounds Completed: {rounds_completed}")

        if score_user > score_comp:
            leaderboard.set(f"🏆 {player_name} Wins the Match!")
            total_wins += 1
        elif score_comp > score_user:
            leaderboard.set("💻 Computer Wins the Match!")
            total_losses += 1
        else:
            leaderboard.set("🤝 It's a Tie!")
            total_ties += 1

        rounds_played = 0
        score_user = 0
        score_comp = 0
        progress['value'] = 0

        win_rate = (total_wins / total_games) * 100 if total_games else 0
        winrate_label.config(text=f"Win Rate: {win_rate:.1f}%")
        scoretracker_label.config(
            text=f"Matches: {total_games} | Wins: {total_wins} | Losses: {total_losses} | Ties: {total_ties}"
        )

# --- Confetti at extreme edges ---
def launch_full_confetti():
    colors = ["#FF6B6B", "#FFD93D", "#6BCB77", "#4D96FF", "#B983FF", "#FF8E00"]
    pieces = []
    width, height = 1500, 500   # window size

    # Spawn confetti anywhere on the canvas
    for _ in range(200):   # more pieces for a bigger celebration
        x = random.randint(0, width)
        y = random.randint(-50, height//2)  # start above or mid‑screen
        size = random.randint(8, 16)
        color = random.choice(colors)
        shape = canvas.create_rectangle(x, y, x+size, y+size, fill=color, outline="")
        pieces.append(shape)

    animate_confetti(pieces)


def animate_confetti(pieces):
    def step():
        alive = False
        for shape in pieces:
            if not canvas.coords(shape):
                continue
            dx = random.randint(-1, 1)
            dy = random.randint(5, 9)
            canvas.move(shape, dx, dy)
            if canvas.coords(shape)[3] > 650:
                canvas.delete(shape)
            else:
                alive = True
        if alive:
            root.after(30, step)
        else:
            canvas.delete("all")
    step()

# --- Hover Effect ---
def on_enter(e):
    e.widget.config(bg="#FFD369", font=("Cambria", 18, "bold"))
def on_leave(e):
    e.widget.config(bg="#222831", font=("Cambria", 14))

# --- Bounce Animation ---
def bounce(btn):
    def grow():
        btn.config(font=("Cambria", 18, "bold"))
        root.after(150, shrink)
    def shrink():
        btn.config(font=("Cambria", 14))
    grow()

# --- GUI Setup ---
root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("700x650")
root.config(bg="#222831")

canvas = tk.Canvas(root, width=700, height=650, bg="#222831", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# --- Player name input ---
def set_name():
    global player_name
    player_name = name_entry.get() or "Player"
    score_label.config(text=f"{player_name}: 0 | Computer: 0")
    name_entry.destroy()
    name_btn.destroy()

name_entry = tk.Entry(root, font=("Cambria", 14))
name_entry.place(x=250, y=10)
name_btn = tk.Button(root, text="Set Name", command=set_name, font=("Cambria", 12))
name_btn.place(x=400, y=8)

# --- Centered Main Frame ---
main_frame = tk.Frame(root, bg="#222831")
main_frame.place(relx=0.5, rely=0.45, anchor="center")

# Title
title_label = tk.Label(main_frame, text="Rock Paper Scissors", font=("Cambria", 28, "bold"), fg="#FFD369", bg="#222831")
title_label.pack(pady=10)

# Result display
result = tk.StringVar()
result_label = tk.Label(main_frame, textvariable=result, font=("Cambria", 16), fg="white", bg="#222831")
result_label.pack(pady=5)

# Score display
score_label = tk.Label(main_frame, text="Player: 0 | Computer: 0", font=("Cambria", 16), fg="#00ADB5", bg="#222831")
score_label.pack(pady=5)

# Buttons
rock_btn = tk.Button(main_frame, text="🪨 Rock", font=("Cambria", 14), command=lambda: play("Rock", rock_btn), bg="#222831", fg="white", width=12)
rock_btn.pack(pady=5)
rock_btn.bind("<Enter>", on_enter); rock_btn.bind("<Leave>", on_leave)

paper_btn = tk.Button(main_frame, text="📄 Paper", font=("Cambria", 14), command=lambda: play("Paper", paper_btn), bg="#222831", fg="white", width=12)
paper_btn.pack(pady=5)
paper_btn.bind("<Enter>", on_enter); paper_btn.bind("<Leave>", on_leave)

scissors_btn = tk.Button(main_frame, text="✂️ Scissors", font=("Cambria", 14), command=lambda: play("Scissors", scissors_btn), bg="#222831", fg="white", width=12)
scissors_btn.pack(pady=5)
scissors_btn.bind("<Enter>", on_enter); scissors_btn.bind("<Leave>", on_leave)

# --- Bottom stats ---
bottom_frame = tk.Frame(root, bg="#222831")
bottom_frame.place(relx=0.5, rely=0.9, anchor="center")

leaderboard = tk.StringVar()
leaderboard_label = tk.Label(bottom_frame, textvariable=leaderboard, font=("Cambria", 14, "bold"), fg="#FFD369", bg="#222831")
leaderboard_label.pack(pady=5)

round_label = tk.Label(bottom_frame, text="Rounds Completed: 0", font=("Cambria", 14), fg="#FFD369", bg="#222831")
round_label.pack(pady=5)

winrate_label = tk.Label(bottom_frame, text="Win Rate: 0%", font=("Cambria", 14), fg="#FFD369", bg="#222831")
winrate_label.pack(pady=5)

scoretracker_label = tk.Label(bottom_frame, text="Matches: 0 | Wins: 0 | Losses: 0 | Ties: 0", font=("Cambria", 14), fg="#FFD369", bg="#222831")
scoretracker_label.pack(pady=5)

progress = ttk.Progressbar(bottom_frame, orient="horizontal", length=400, mode="determinate")
progress.pack(pady=5)

footer = tk.Label(bottom_frame, text="Made with ❤️ by Team RPS", font=("Cambria", 14), fg="#FFD369", bg="#222831")
footer.pack(pady=5)

# --- Names bottom-right ---
names_frame = tk.Frame(root, bg="#222831")
names_frame.place(relx=0.85, rely=0.8)

students = ["CK", "TANISH SHETH", "SUMANTH A S", "SHIVAGANESH"]
for name in students:
    tk.Label(names_frame, text=name, font=("Cambria", 12, "bold"), fg="#EEEEEE", bg="#222831").pack(anchor="e")

# --- Mainloop ---
root.mainloop()

import tkinter as tk
from tkinter import messagebox
import time
import os

root = tk.Tk()

root.title("BrainVitta AI")
root.geometry("700x850")
root.configure(bg="#8B5A2B")

WOOD = "#8B5A2B"
DARK_WOOD = "#5C3A1E"
MARBLE = "#D2691E"
EMPTY = "#DEB887"
SELECTED = "#FFD700"

INITIAL_BOARD = [
    [-1,-1,1,1,1,-1,-1],
    [-1,-1,1,1,1,-1,-1],
    [1,1,1,1,1,1,1],
    [1,1,1,0,1,1,1],
    [1,1,1,1,1,1,1],
    [-1,-1,1,1,1,-1,-1],
    [-1,-1,1,1,1,-1,-1]
]

board = [row[:] for row in INITIAL_BOARD]

buttons = []
history = []

selected = None

moves = 0
score = 0

player_name = "Player"

best_score = 0
best_player = "None"

start_time = time.time()
# ================= BEST SCORE =================

def load_best_score():

    global best_score
    global best_player

    if os.path.exists("best_score.txt"):

        with open("best_score.txt", "r") as f:

            data = f.read().split(",")

            if len(data) == 2:

                best_player = data[0]

                try:
                    best_score = int(data[1])
                except:
                    best_score = 0


def save_best_score():

    global best_score
    global best_player

    if score > best_score:

        best_score = score
        best_player = player_name

        with open("best_score.txt", "w") as f:

            f.write(f"{best_player},{best_score}")


# ================= WELCOME PAGE =================

def welcome_page():

    for widget in root.winfo_children():

        widget.destroy()

    tk.Label(
        root,
        text="🧠 BRAINVITTA GAME\n\nRutuja Gaikwad Creation",
        font=("Georgia", 24, "bold"),
        bg=WOOD,
        fg="white"
    ).pack(pady=30)

    tk.Label(
        root,
        text="Enter Player Name",
        font=("Georgia", 14),
        bg=WOOD,
        fg="white"
    ).pack(pady=10)

    global name_entry

    name_entry = tk.Entry(
        root,
        font=("Georgia", 14)
    )

    name_entry.pack()

    tk.Button(
        root,
        text="📖 Instructions",
        font=("Georgia", 14, "bold"),
        command=instruction_page
    ).pack(pady=15)

    tk.Button(
        root,
        text="🎮 Start Game",
        font=("Georgia", 14, "bold"),
        command=start_game
    ).pack(pady=10)


# ================= INSTRUCTIONS =================

def instruction_page():

    global player_name

    player_name = name_entry.get()

    if player_name.strip() == "":
        player_name = "Player"

    for widget in root.winfo_children():

        widget.destroy()

    text = """
🧠 HOW TO PLAY BRAINVITTA

1. Select a marble.

2. Jump over another marble.

3. The jumped marble disappears.

4. Move only:
   • Horizontal
   • Vertical

🎯 Goal:
Finish with minimum marbles.

🏆 Ranking

1 Marble  = Genius
2 Marbles = Excellent
3 Marbles = Intelligent

🤖 AI Hint Available
↩ Undo Available
🔄 Restart Available
"""

    tk.Label(
        root,
        text=text,
        justify="left",
        font=("Georgia", 14),
        bg=WOOD,
        fg="white"
    ).pack(pady=20)

    tk.Button(
        root,
        text="🎮 Start Game",
        font=("Georgia", 14, "bold"),
        command=start_game
    ).pack(pady=10)
    # ================= START GAME =================

def start_game():

    global start_time

    load_best_score()

    start_time = time.time()

    for widget in root.winfo_children():
        widget.destroy()

    create_game_screen()


# ================= GAME LOGIC =================

def count_marbles():

    total = 0

    for row in board:
        total += row.count(1)

    return total


def calculate_score():

    global score

    marbles = count_marbles()

    if marbles == 1:
        score = 100

    elif marbles == 2:
        score = 80

    elif marbles == 3:
        score = 60

    else:
        score = 0


def save_state():

    history.append(
        (
            [row[:] for row in board],
            moves
        )
    )


def valid_moves():

    directions = [
        (0,2),
        (0,-2),
        (2,0),
        (-2,0)
    ]

    for r in range(7):

        for c in range(7):

            if board[r][c] == 1:

                for dr,dc in directions:

                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < 7 and 0 <= nc < 7:

                        mr = (r + nr)//2
                        mc = (c + nc)//2

                        if board[nr][nc] == 0 and board[mr][mc] == 1:
                            return True

    return False


# ================= AI HINT =================

def ai_hint():

    directions = [
        (0,2),
        (0,-2),
        (2,0),
        (-2,0)
    ]

    for r in range(7):

        for c in range(7):

            if board[r][c] == 1:

                for dr,dc in directions:

                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < 7 and 0 <= nc < 7:

                        mr = (r + nr)//2
                        mc = (c + nc)//2

                        if board[nr][nc] == 0 and board[mr][mc] == 1:

                            messagebox.showinfo(
                                "🤖 AI Hint",
                                f"Suggested Move:\n({r},{c}) ➜ ({nr},{nc})"
                            )
                            return

    messagebox.showinfo(
        "🤖 AI Hint",
        "No valid moves available."
    )


# ================= RESULT =================

def check_result():

    marbles = count_marbles()

    save_best_score()

    if marbles == 1:

        messagebox.showinfo(
            "🏆 Genius",
            "Congratulations!\nYou finished with 1 marble."
        )

    elif marbles == 2:

        messagebox.showinfo(
            "⭐ Excellent",
            "Congratulations!\nYou finished with 2 marbles."
        )

    elif marbles == 3:

        messagebox.showinfo(
            "💡 Intelligent",
            "Congratulations!\nYou finished with 3 marbles."
        )

    elif not valid_moves():

        messagebox.showinfo(
            "Game Over",
            f"No valid moves left.\n\nMarbles Remaining: {marbles}"
        )
        # ================= UPDATE BOARD =================

def update_board():

    calculate_score()

    for r in range(7):

        for c in range(7):

            if board[r][c] == -1:

                buttons[r][c].config(
                    text="",
                    bg=DARK_WOOD
                )

            elif board[r][c] == 1:

                buttons[r][c].config(
                    text="●",
                    bg=MARBLE,
                    fg="white"
                )

            else:

                buttons[r][c].config(
                    text="○",
                    bg=EMPTY,
                    fg="black"
                )

    info_label.config(
        text=
        f"Player: {player_name}\n"
        f"Marbles: {count_marbles()}   "
        f"Moves: {moves}   "
        f"Score: {score}\n"
        f"Best: {best_player} ({best_score})"
    )


# ================= TIMER =================

def update_timer():

    seconds = int(time.time() - start_time)

    timer_label.config(
        text=f"⏱ Time: {seconds}s"
    )

    root.after(
        1000,
        update_timer
    )


# ================= RESTART =================

def restart():

    global board
    global moves
    global history
    global selected
    global start_time

    board = [row[:] for row in INITIAL_BOARD]

    moves = 0
    history = []
    selected = None

    start_time = time.time()

    update_board()


# ================= UNDO =================

def undo():

    global board
    global moves

    if history:

        old_board, old_moves = history.pop()

        board = [row[:] for row in old_board]

        moves = old_moves

        update_board()

    else:

        messagebox.showinfo(
            "Undo",
            "No moves available."
        )


# ================= CLICK =================

def click(r, c):

    global selected
    global moves

    if board[r][c] == 1 and selected is None:

        selected = (r, c)

        buttons[r][c].config(
            bg=SELECTED
        )

        return

    if selected is None:
        return

    sr, sc = selected

    if board[r][c] != 0:

        selected = None
        update_board()
        return

    if not (
        (abs(r - sr) == 2 and c == sc)
        or
        (abs(c - sc) == 2 and r == sr)
    ):

        selected = None
        update_board()
        return

    mr = (sr + r) // 2
    mc = (sc + c) // 2

    if board[mr][mc] != 1:

        selected = None
        update_board()
        return

    save_state()

    board[sr][sc] = 0
    board[mr][mc] = 0
    board[r][c] = 1

    moves += 1

    selected = None

    update_board()

    check_result()
    # ================= GAME SCREEN =================

def create_game_screen():

    global buttons
    global info_label
    global timer_label

    buttons = []

    title = tk.Label(
        root,
        text="🧠 BRAINVITTA",
        font=("Georgia", 26, "bold"),
        bg=WOOD,
        fg="white"
    )

    title.pack(pady=10)

    # ===== TOP BUTTONS =====

    control = tk.Frame(
        root,
        bg=WOOD
    )

    control.pack(pady=10)

    tk.Button(
        control,
        text="🔄 Restart",
        width=12,
        font=("Georgia",12,"bold"),
        command=restart
    ).grid(
        row=0,
        column=0,
        padx=10
    )

    tk.Button(
        control,
        text="↩ Undo",
        width=12,
        font=("Georgia",12,"bold"),
        command=undo
    ).grid(
        row=0,
        column=1,
        padx=10
    )

    tk.Button(
        control,
        text="🤖 AI Hint",
        width=12,
        font=("Georgia",12,"bold"),
        command=ai_hint
    ).grid(
        row=0,
        column=2,
        padx=10
    )

    # ===== BOARD =====

    board_frame = tk.Frame(
        root,
        bg=WOOD
    )

    board_frame.pack(pady=10)

    for r in range(7):

        row_buttons = []

        for c in range(7):

            btn = tk.Button(
                board_frame,
                width=4,
                height=2,
                font=("Georgia",18,"bold"),
                command=lambda r=r, c=c: click(r, c)
            )

            btn.grid(
                row=r,
                column=c,
                padx=3,
                pady=3
            )

            row_buttons.append(btn)

        buttons.append(row_buttons)

    # ===== INFO =====

    info_label = tk.Label(
        root,
        text="",
        font=("Georgia",14),
        bg=WOOD,
        fg="white"
    )

    info_label.pack(pady=10)

    # ===== TIMER =====

    timer_label = tk.Label(
        root,
        text="⏱ Time: 0s",
        font=("Georgia",14,"bold"),
        bg=WOOD,
        fg="gold"
    )

    timer_label.pack()

    update_board()
    update_timer()


# ================= START APP =================

welcome_page()

root.mainloop()
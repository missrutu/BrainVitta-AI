import tkinter as tk
from tkinter import messagebox
import time
import os


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("BrainVitta Game - Rutuja Gaikwad Creation")
root.geometry("650x850")
root.configure(bg="#8B5A2B")


# ================= BOARD =================

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

selected = None
buttons = []
history = []

moves = 0
score = 0

player_name = "Player"

best_score = 0
best_player = "None"

start_time = time.time()


# ================= COLORS =================

WOOD = "#8B5A2B"
DARK_WOOD = "#5C3A1E"
MARBLE = "#D2691E"
EMPTY = "#DEB887"
SELECTED = "#FFD700"


# ================= SCORE =================

def load_best_score():

    global best_score, best_player

    if os.path.exists("best_score.txt"):

        with open("best_score.txt","r") as f:

            data = f.read().split(",")

            if len(data)==2:
                best_player = data[0]
                best_score = int(data[1])



def save_best_score():

    global best_score,best_player

    if score > best_score:

        best_score = score
        best_player = player_name

        with open("best_score.txt","w") as f:
            f.write(f"{best_player},{best_score}")



# ================= WELCOME =================


def welcome_page():

    for widget in root.winfo_children():
        widget.destroy()


    title = tk.Label(
        root,
        text="🧠 Welcome to\nRutuja Gaikwad Creation\n\nBRAINVITTA GAME",
        font=("Georgia",24,"bold"),
        bg=WOOD,
        fg="white"
    )

    title.pack(pady=30)



    tk.Label(
        root,
        text="A Strategy Puzzle Game",
        font=("Georgia",16),
        bg=WOOD,
        fg="white"
    ).pack()



    tk.Label(
        root,
        text="Enter Player Name",
        font=("Georgia",14),
        bg=WOOD,
        fg="white"
    ).pack(pady=10)



    global name_entry

    name_entry = tk.Entry(
        root,
        font=("Georgia",14)
    )

    name_entry.pack()



    tk.Button(
        root,
        text="Start Game 🎮",
        font=("Georgia",14,"bold"),
        command=instruction_page
    ).pack(pady=15)



    tk.Button(
        root,
        text="Skip Instructions ➡",
        command=start_game
    ).pack()



# ================= INSTRUCTIONS =================


def instruction_page():

    global player_name

    player_name = name_entry.get()

    if player_name=="":
        player_name="Player"



    for widget in root.winfo_children():
        widget.destroy()



    instructions = """
🧠 HOW TO PLAY BRAINVITTA

1. Select a marble.

2. Jump over another marble.

3. The jumped marble disappears.

4. Move only:
   Horizontal
   Vertical

🎯 Goal:
Finish with minimum marbles.

🏆 Score:

1 Marble = Genius
2 Marbles = Excellent
3 Marbles = Intelligent
"""



    tk.Label(
        root,
        text=instructions,
        font=("Georgia",14),
        bg=WOOD,
        fg="white",
        justify="left"
    ).pack(pady=30)



    tk.Button(
        root,
        text="Start Game 🎮",
        font=("Georgia",14),
        command=start_game
    ).pack(pady=10)



    tk.Button(
        root,
        text="Skip ➡",
        command=start_game
    ).pack()
    # ================= START GAME =================

def start_game():

    global start_time

    load_best_score()

    start_time = time.time()


    for widget in root.winfo_children():
        widget.destroy()


    create_game_screen()



# ================= GAME FUNCTIONS =================


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

                    nr = r+dr
                    nc = c+dc


                    if 0 <= nr < 7 and 0 <= nc < 7:

                        mr = (r+nr)//2
                        mc = (c+nc)//2


                        if board[nr][nc]==0 and board[mr][mc]==1:
                            return True


    return False




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



def update_timer():

    seconds = int(time.time()-start_time)

    timer_label.config(
        text=f"⏱ Time: {seconds}s"
    )


    root.after(
        1000,
        update_timer
    )



# ================= RESTART =================


def restart():

    global board,moves,history,start_time,selected


    board = [
        row[:]
        for row in INITIAL_BOARD
    ]

    moves = 0

    history = []

    selected = None

    start_time=time.time()


    update_board()



# ================= UNDO =================


def undo():

    global board,moves


    if history:

        state,last_move = history.pop()


        board = [
            row[:]
            for row in state
        ]


        moves = last_move


        update_board()


    else:

        messagebox.showinfo(
            "Undo",
            "No moves available"
        )



# ================= CLICK MOVE =================


def click(r,c):

    global selected,moves


    if board[r][c]==1 and selected is None:

        selected=(r,c)

        buttons[r][c].config(
            bg=SELECTED
        )

        return



    if selected is None:
        return



    sr,sc = selected



    if board[r][c]!=0:

        selected=None
        update_board()
        return



    if not(
        (abs(r-sr)==2 and c==sc)
        or
        (abs(c-sc)==2 and r==sr)
    ):

        selected=None
        update_board()
        return



    mr=(sr+r)//2
    mc=(sc+c)//2



    if board[mr][mc]!=1:

        selected=None
        update_board()
        return



    save_state()


    board[sr][sc]=0
    board[mr][mc]=0
    board[r][c]=1


    moves+=1

    selected=None


    update_board()
    # ================= GAME SCREEN =================


def create_game_screen():

    global buttons, info_label, timer_label


    buttons=[]


    tk.Label(
        root,
        text="🧠 BRAINVITTA",
        font=("Georgia",28,"bold"),
        bg=WOOD,
        fg="white"
    ).pack(pady=15)



    board_frame=tk.Frame(
        root,
        bg=WOOD
    )

    board_frame.pack()



    for r in range(7):

        row=[]

        for c in range(7):

            btn=tk.Button(
                board_frame,
                width=4,
                height=2,
                font=("Georgia",18),
                command=lambda r=r,c=c: click(r,c)
            )


            btn.grid(
                row=r,
                column=c,
                padx=3,
                pady=3
            )


            row.append(btn)


        buttons.append(row)



    info_label=tk.Label(
        root,
        font=("Georgia",14),
        bg=WOOD,
        fg="white"
    )

    info_label.pack(pady=10)



    timer_label=tk.Label(
        root,
        font=("Georgia",14),
        bg=WOOD,
        fg="white"
    )

    timer_label.pack()



    # ============ CONTROL BUTTONS ============

    control=tk.Frame(
        root,
        bg=WOOD
    )

    control.pack(pady=20)



    restart_button=tk.Button(
        control,
        text="Restart 🔄",
        font=("Georgia",12,"bold"),
        width=12,
        command=restart
    )

    restart_button.grid(
        row=0,
        column=0,
        padx=15
    )



    undo_button=tk.Button(
        control,
        text="Undo ↩",
        font=("Georgia",12,"bold"),
        width=12,
        command=undo
    )

    undo_button.grid(
        row=0,
        column=1,
        padx=15
    )
    # ============ TOP BUTTONS ============

    control = tk.Frame(
        root,
        bg=WOOD
    )

    control.pack(pady=10)


    restart_button = tk.Button(
        control,
        text="🔄 Restart",
        font=("Georgia",12,"bold"),
        width=12,
        command=restart
    )

    restart_button.grid(
        row=0,
        column=0,
        padx=20
    )


    undo_button = tk.Button(
        control,
        text="↩ Undo",
        font=("Georgia",12,"bold"),
        width=12,
        command=undo
    )

    undo_button.grid(
        row=0,
        column=1,
        padx=20
    )


    update_board()

    update_timer()



# ================= RUN GAME =================


welcome_page()

root.mainloop()
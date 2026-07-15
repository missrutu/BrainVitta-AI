board = [
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [-1, -1, 1, 1, 1, -1, -1],
    [-1, -1, 1, 1, 1, -1, -1]
]


def print_board():
    print()
    for row in board:
        for cell in row:
            if cell == -1:
                print("  ", end="")
            elif cell == 1:
                print("O ", end="")
            else:
                print(". ", end="")
        print()
    print()


def count_marbles():
    count = 0
    for row in board:
        count += row.count(1)
    return count


while True:

    print_board()
    print("Marbles Left:", count_marbles())

    try:
        sr = int(input("Start Row: "))
        sc = int(input("Start Col: "))

        er = int(input("End Row: "))
        ec = int(input("End Col: "))

    except ValueError:
        print("\nPlease enter numbers only!")
        continue

    # Check board boundaries
    if not (0 <= sr <= 6 and 0 <= sc <= 6 and
            0 <= er <= 6 and 0 <= ec <= 6):
        print("\nCoordinates must be between 0 and 6!")
        continue

    # Check valid cells
    if board[sr][sc] == -1 or board[er][ec] == -1:
        print("\nInvalid board position!")
        continue

    # Start must contain marble
    if board[sr][sc] != 1:
        print("\nNo marble at starting position!")
        continue

    # End must be empty
    if board[er][ec] != 0:
        print("\nDestination is not empty!")
        continue

    dr = er - sr
    dc = ec - sc

    # Must move exactly 2 spaces horizontally or vertically
    if not (
        (abs(dr) == 2 and dc == 0) or
        (abs(dc) == 2 and dr == 0)
    ):
        print("\nMove must be exactly 2 spaces!")
        continue

    middle_row = (sr + er) // 2
    middle_col = (sc + ec) // 2

    # Must jump over a marble
    if board[middle_row][middle_col] != 1:
        print("\nNo marble to jump over!")
        continue

    # Make move
    board[sr][sc] = 0
    board[middle_row][middle_col] = 0
    board[er][ec] = 1

    print("\nMove Successful!")

    if count_marbles() == 1:
        print("\n🎉 YOU WIN! Only one marble remains!")
        break

    choice = input("\nContinue? (y/n): ")

    if choice.lower() == "n":
        break

print("\nGame Over!")
from tkinter import *
import random

def next_turn(row, col):
    global player
    if game_btns[row][col]['text'] == "" and check_winner() == False:
        game_btns[row][col]['text'] = player

        if check_winner() == False:
            if player == players[0]:
                player = players[1]
                label.config(text=(players[1] + " turn"))
                computer_turn()

        elif check_winner() == True:
            label.config(text=(players[0] + " wins!"))

        elif check_winner() == 'tie':
            label.config(text=("Tie, No Winner!"))

def computer_turn():
    global player

    def minimax(board, depth, is_maximizing):
        winner = get_winner(board)
        if winner == "o":
            return 10 - depth
        if winner == "x":
            return depth - 10
        if not any("" in row for row in board):
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "o"
                        score = minimax(board, depth + 1, False)
                        board[r][c] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "x"
                        score = minimax(board, depth + 1, True)
                        board[r][c] = ""
                        best_score = min(score, best_score)
            return best_score

    def get_best_move():
        best_score = -float("inf")
        move = None
        for r in range(3):
            for c in range(3):
                if game_btns[r][c]['text'] == "":
                    game_btns[r][c]['text'] = "o"
                    board = [[game_btns[i][j]['text'] for j in range(3)] for i in range(3)]
                    score = minimax(board, 0, False)
                    game_btns[r][c]['text'] = ""
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        return move

    available_moves = [(r, c) for r in range(3) for c in range(3) if game_btns[r][c]['text'] == ""]

    if available_moves and check_winner() == False:
        move = get_best_move()
        if move:
            game_btns[move[0]][move[1]]['text'] = player

        if check_winner() == False:
            player = players[0]
            label.config(text=(players[0] + " turn"))

        elif check_winner() == True:
            label.config(text=(players[1] + " wins!"))

        elif check_winner() == 'tie':
            label.config(text=("Tie, No Winner!"))

def get_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != "":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != "":
        return board[0][2]
    return None

def check_winner():
    # check all 3 horizontal conditions
    for row in range(3):
        if game_btns[row][0]['text'] == game_btns[row][1]['text'] == game_btns[row][2]['text'] != "":
            game_btns[row][0].config(bg="lightblue")
            game_btns[row][1].config(bg="lightblue")
            game_btns[row][2].config(bg="lightblue")
            return True

    # check all 3 vertical conditions
    for col in range(3):
        if game_btns[0][col]['text'] == game_btns[1][col]['text'] == game_btns[2][col]['text'] != "":
            game_btns[0][col].config(bg="lightblue")
            game_btns[1].config(bg="lightblue")
            game_btns[2][col].config(bg="lightblue")
            return True

    # check diagonals conditions
    if game_btns[0][0]['text'] == game_btns[1][1]['text'] == game_btns[2][2]['text'] != "":
        game_btns[0][0].config(bg="lightblue")
        game_btns[1][1].config(bg="lightblue")
        game_btns[2][2].config(bg="lightblue")
        return True
    elif game_btns[0][2]['text'] == game_btns[1][1]['text'] == game_btns[2][0]['text'] != "":
        game_btns[0][2].config(bg="lightblue")
        game_btns[1][1].config(bg="lightblue")
        game_btns[2][0].config(bg="lightblue")
        return True

    # if there are no empty spaces left
    if check_empty_spaces() == False:
        for row in range(3):
            for col in range(3):
                game_btns[row][col].config(bg='lightcoral')

        return 'tie'

    else:
        return False

def check_empty_spaces():
    spaces = 9

    for row in range(3):
        for col in range(3):
            if game_btns[row][col]['text'] != "":
                spaces -= 1

    if spaces == 0:
        return False
    else:
        return True

def start_new_game():
    global player
    player = players[0]

    label.config(text=(player + " turn"))

    for row in range(3):
        for col in range(3):
            game_btns[row][col].config(text="", bg="#D3D3D3")

window = Tk()
window.title("Tic-Tac-Toe Player vs Computer")
window.configure(bg="lightgrey")

players = ["x", "o"]
player = players[0]

game_btns = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

label = Label(text=(player + " turn"), font=('consolas', 40), bg="lightgrey", fg="darkblue")
label.pack(side="top")

restart_btn = Button(text="restart", font=(
    'consolas', 20), command=start_new_game, bg="lightgreen", fg="darkgreen")
restart_btn.pack(side="top")

btns_frame = Frame(window, bg="lightgrey")
btns_frame.pack()

for row in range(3):
    for col in range(3):
        game_btns[row][col] = Button(btns_frame, text="", font=('consolas', 50), width=4, height=1, bg="#D3D3D3",
                                     command=lambda row=row, col=col: next_turn(row, col))
        game_btns[row][col].grid(row=row, column=col)

window.mainloop()
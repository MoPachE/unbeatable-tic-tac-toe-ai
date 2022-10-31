import random

board = [
    ['*', '*', '*'],
    ['*', '*', '*'],
    ['*', '*', '*']
]

player1 = 'X'
player2 = 'O'

start = True
stupid = False

print('Welcome to Python Tic Tac Toe!')
gamemode = str(input('Press enter to start a game'))
gamemode.lower()
if not gamemode == 'pvp' and not gamemode == 'easy' and not gamemode == 'medium' and not gamemode == 'hard':
    print("\n")
    gamemode = 'hard'


# Player move
def move(player):
    p_move = str(input('Where do you want to go? [ROW] [COLUMN]\n'))

    if p_move == 'Lamarcus Dinglebingle Sr.':
        for i in range(len(board)):
            for j in range(len(board)):
                board[i][j] = player
        print('\n\nYou got ratioed, kid\n\n')
        return

    if not len(p_move) == 3:
        print('Invalid format, try again!\n')
        move(player)
        return
    if (int(p_move[0]) < 1 or int(p_move[0]) > 3) or (int(p_move[2]) < 1 or int(p_move[2]) > 3):
        print('Invalid row or column. Make sure the # is between 1 and 3!\n')
        move(player)
        return
    if not board[int(p_move[0]) - 1][int(p_move[2]) - 1] == '*':
        print('Spot taken, try again!\n')
        move(player)
        return

    board[int(p_move[0]) - 1][int(p_move[2]) - 1] = player


# Easy-mode "ai"
def ai_easy():
    ai_move_x = random.randint(0, 2)
    ai_move_y = random.randint(0, 2)
    if not '*' in board[ai_move_x][ai_move_y]:
        ai_easy()
        return
    print(f'CPU attacks at row {ai_move_x + 1} and column {ai_move_y + 1}')
    board[ai_move_x][ai_move_y] = player2


# Hard-mode ai
def ai_hard():
    global start
    global board
    global ai_scores
    ai_scores = []
    global ai_moves
    ai_moves = []
    global board_save

    if start:
        if board[1][1] == '*':
            board[1][1] = player2
        else:
            board[0][2] = player2
        start = False
        return

    moves = ai_findMoves()
    for i in moves:
        score = ai_scoreBoard()[0]
        pos = ai_scoreBoard()[1]

        if score == 1:
            board[i[0]][i[1]] = '*'
            board[pos[0]][pos[1]] = player2
            return

        if score == -1:
            board[i[0]][i[1]] = '*'
            board[pos[0]][pos[1]] = player2
            return

        if score == 0:
            board[i[0]][i[1]] = player2
            ai_moves.append([i[0], i[1]])

            board_save = [row[:] for row in board]
            ai_recurse()  # Recursion to fill the lists
            board = [row[:] for row in board_save]
            board[i[0]][i[1]] = '*'

    # This is outside of the for loop
    max_score_index = ai_scores.index(max(ai_scores))
    board[ai_moves[max_score_index][0]][ai_moves[max_score_index][1]] = player2


# Recursion function
currentPlayer = player2
end = False


def ai_recurse():
    global currentPlayer
    global end
    global stupid

    if end and not stupid: return  # sneaky little way to end recursion

    if currentPlayer == player1:
        currentPlayer = player2
    else:
        currentPlayer = player1

    r_score = ai_scoreBoard()[0]
    if currentPlayer == player1:
        r_score *= -1

    if r_score == 0:
        ai_scores.append(r_score)
        end = True
        return

    if len(ai_findMoves()) == 1:
        if currentPlayer == player1 and r_score == 1:
            ai_scores.append(-1)
            end = True
            return
        else:
            ai_scores.append(r_score)
            end = True
            return

    board[ai_scoreBoard()[1][0]][ai_scoreBoard()[1][1]] = currentPlayer
    # print_board()
    # print(r_score)
    ai_recurse()


# Hard-mode ai - finding available moves
def ai_findMoves():
    o = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '*': o.append([i, j])
    return o


# Hard-mode ai - scoring the board
def ai_scoreBoard():
    # AI win
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not board[i][j] == '*': continue
            board[i][j] = player2
            if check_win() == player2:
                board[i][j] = '*'
                return [1, [i, j]]
            board[i][j] = '*'
    # Player block
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not board[i][j] == '*': continue
            board[i][j] = player1
            if check_win() == player1:
                board[i][j] = '*'
                return [-1, [i, j]]
            board[i][j] = '*'
    # Since none returned, it has to be a draw
    return [0, [-1, -1]]


# Check win
def check_win():
    win = 'none'

    # Horizontal
    for i in range(len(board)):
        if not '*' in board[i]:
            if board[i][0] == board[i][1] and board[i][1] == board[i][2]: return board[i][0]

            # Vertical
    temp_board = [
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]]
    ]
    for i in range(len(temp_board)):
        if not '*' in temp_board[i]:
            if temp_board[i][0] == temp_board[i][1] and temp_board[i][1] == temp_board[i][2]: return temp_board[i][0]

            # Diagonal
    if (not board[0][0] == '*') and (board[0][0] == board[1][1] and board[1][1] == board[2][2]): return board[0][0]
    if (not board[2][0] == '*') and (board[2][0] == board[1][1] and board[1][1] == board[0][2]): return board[2][0]

    # Draw
    draw = True
    for i in board:
        if '*' in i:
            draw = False
    if draw: return 'draw'

    return win


# Print the board
def print_board():
    for i in range(len(board)):
        for j in range(len(board[i])):
            if i == 0:
                print(f'\n\n {board[i][j]} | {board[i][j + 1]} | {board[i][j + 2]}\n------------')
                break
            elif i == 1:
                print(f' {board[i][j]} | {board[i][j + 1]} | {board[i][j + 2]}\n------------')
                break
            else:
                print(f' {board[i][j]} | {board[i][j + 1]} | {board[i][j + 2]}\n\n')
                break


# end of function declarations


# Main Game Loop       <--------
while True:
    # Check win
    cw = check_win()
    if cw == 'draw':
        print("DRAW! Start the game over or accept friendship.")
        break
    elif not cw == 'none':
        print(f'Player "{cw}" won! Congrats!')
        break

    # Player 1 goes
    print('\n"X" player goes!')
    move(player1)
    print_board()
    if not check_win() == 'none': continue

    # Next game-event goes
    if gamemode == 'pvp':
        print('"O" player goes!')
        move(player2)
        print_board()
        if not check_win() == 'none': continue
    elif gamemode == 'easy':
        ai_easy()
        print_board()
        if not check_win() == 'none': continue
    elif gamemode == 'medium':
        stupid = True
        ai_hard()
        print('AI places its move!')
        print_board()
        if not check_win() == 'none': continue
    elif gamemode == 'hard':
        ai_hard()
        print('AI places its move!')
        print_board()
        if not check_win() == 'none': continue
    else:
        print('This gamemode does not exist!')
        break
# Main Game Loop END   <--------
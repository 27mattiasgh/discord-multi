def minimax(board, player):
    #if someone has already won the game
    winner = getWinner(board)
    if winner != Player.Blank:
        return winner * player, -1
    move = -1
    score = -2

    for i in range(9):
        if board[i] == Player.Blank:
            copy_board = board.copy()
            copy_board[i] = player
            opponent = getOpponentFor(player)

            #play the move if it wins
            if getWinner(copy_board) == Player.Computer:
                return Player.Computer, i



            #else just run the algorithm    
            else:
                copy_score = -minimax(copy_board, opponent)[0]
            
            #make this move the best move
            if copy_score > score:
                score = copy_score
                move = i

    #if board is full
    if move == -1:
        return 0, -1

    return score, move

def getWinner(board):
    #rows
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2]:
            return board[i]

    #columns     
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6]:
            return board[i]

    #diagonals
    if board[0] == board[4] == board[8]:
        return board[0]
    if board[2] == board[4] == board[6]:
        return board[2]
        
    #no winner
    return Player.Blank

def getOpponentFor(player):
    return Player.Human if player == Player.Computer else Player.Computer

class Player:
    Human = -1
    Blank = 0
    Computer = 1 


def Engine(board):
    return minimax(board, Player.Computer)[1]

def Win(board):
    return minimax(board, Player.Computer)[0]
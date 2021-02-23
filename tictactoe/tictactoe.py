# write your code here

# Return true if the space is empty
def is_space(board, pos_x, pos_y):
    return board[pos_x][pos_y] == '_'       # Assuming '_' to be empty space


# Take the board and make move on given location
def make_move(board, pos_x, pos_y, c):
    board[pos_x][pos_y] = c
    return board


def get_position(board):

    while True:
        pos = input('Enter the coordinates: ').split()

        if len(pos) == 2:
            x, y = pos
            if x not in '1 2 3 4 5 6 7 8 9'.split() or y not in '1 2 3 4 5 6 7 8 9'.split():
                print('You should enter numbers!')
            elif x not in ('1', '2', '3') or y not in ('1', '2', '3'):
                print('Coordinates should be from 1 to 3!')
            elif not is_space(board, int(x) - 1, int(y) - 1):
                print('This cell is occupied! Choose another one!')
            else:
                return int(x) - 1, int(y) - 1

        else:
            print('You should enter numbers!')


def board_matrix(states):
    return [[s for s in states[i:i + 3]] for i in range(0, 7, 3)]      # Convert the string list to matrix list of
    # string


def display_board(board):

    print('---------')
    for row in range(3):
        print('|', end=' ')
        for col in range(3):
            print(board[row][col], end=' ')
        print('|')
    print('---------')


# check if board is full
def is_board_full(board):

    for row in board:
        if '_' in row:
            return False

    return True


# Take the board and the player character to check if they won
def is_winner(board, c):

    return ((board[0][0] == c and board[0][1] == c and board[0][2] == c)
            or (board[1][0] == c and board[1][1] == c and board[1][2] == c)
            or (board[2][0] == c and board[2][1] == c and board[2][2] == c)
            # coloumns
            or (board[0][0] == c and board[1][0] == c and board[2][0] == c)
            or (board[0][1] == c and board[1][1] == c and board[2][1] == c)
            or (board[0][2] == c and board[1][2] == c and board[2][2] == c)
            # Diagonals
            or (board[0][0] == c and board[1][1] == c and board[2][2] == c)
            or (board[2][0] == c and board[1][1] == c and board[0][2] == c))


# Analyze the board state
def board_analyser(board):

    x_count = [row.count('X') for row in board]
    o_count = [row.count('O') for row in board]
    diff = sum(x_count) - sum(o_count)

    if not is_winner(board, 'X') and not is_winner(board, 'O'):     # check if player hasn't won
        if diff in (0, 1):
            if not is_board_full(board):    # check if board is not full
                print('Game not finished')
            else:
                print('Draw')
        else:
            print('Impossible')
    elif is_winner(board, 'X') and not is_winner(board, 'O'):   # check if only single player has won
        print('X wins')
    elif is_winner(board, 'O') and not is_winner(board, 'X'):
        print('O wins')
    else:
        print('Impossible')


def start_game():
    '''Game main function'''

    EMPTY_GRID = '_________'
    board = board_matrix(list(EMPTY_GRID))      # Return the string as a matrix list
    p = 'X'

    while True:
        display_board(board)
        if p == 'X':
            x, y = get_position(board)
            board = make_move(board, x, y, p)
            if is_winner(board, p):
                display_board(board)
                break
            p = 'O'
        else:
            x, y = get_position(board)
            board = make_move(board, x, y, p)
            if is_winner(board, p):
                display_board(board)
                board_analyser(board)
                break
            p = 'X'


start_game()

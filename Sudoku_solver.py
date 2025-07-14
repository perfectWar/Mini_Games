def solve_sudoku(board):
    
    # Find the next empty cell (represented by 0)
    find = find_empty(board)
    if not find:
        # If no empty cell is found, the puzzle is solved
        return True
    else:
        row, col = find

    # Try numbers from 1 to 9 in the empty cell
    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            # If the number is valid, place it on the board
            board[row][col] = num

            # Recursively call solve_sudoku on the updated board
            if solve_sudoku(board):
                return True

            # If the recursive call returns False, it means this path was a dead end.
            # We must "backtrack" by resetting the cell to 0 and trying the next number.
            board[row][col] = 0

    # If we've tried all numbers and none lead to a solution, return False
    return False


def is_valid(board, num, pos):
    # Checks if placing a number 'num' at position 'pos' (row, col) is valid
    row, col = pos

    # 1. Check the row
    for i in range(len(board[0])):
        if board[row][i] == num and col != i:
            return False

    # 2. Check the column
    for i in range(len(board)):
        if board[i][col] == num and row != i:
            return False

    # 3. Check the 3x3 box
    box_x = col // 3
    box_y = row // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def find_empty(board):
    """
    Finds the first empty cell (represented by 0) in the board.
    Returns a tuple (row, col) or None if no empty cell is found.
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None


def print_board(board):
    # pretty print of the board 
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")


if __name__ == "__main__":
    # Example board (0 represents an empty cell)
    example_board = [
        [0,0,0,2,6,0,7,0,1],
        [6,8,0,0,7,0,0,9,0],
        [1,9,0,0,0,4,5,0,0],
        [8,2,0,1,0,0,0,4,0],
        [0,0,4,6,0,2,9,0,0],
        [0,5,0,0,0,3,0,2,8],
        [0,0,9,3,0,0,0,7,4],
        [0,4,0,0,5,0,0,3,6],
        [7,0,3,0,1,8,0,0,0]
    ]

    print("Unsolved Sudoku Board:")
    print_board(example_board)
    print("\n=========================\n")

    solve_sudoku(example_board)

    print("Solved Sudoku Board:")
    print_board(example_board)

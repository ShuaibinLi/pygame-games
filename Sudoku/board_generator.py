import numpy as np
from random import shuffle


class SudokuBoard(object):
    """
    Randomly generate a Sudoku game board (9X9, 6X6, 4X4)
     using backtracking
    """

    def __init__(self, size=9, difficulty=0.5):
        self.size = size
        self.difficulty = difficulty
        self.nums = [i for i in range(1, size + 1)]
        board = np.array([[0] * size] * size)

        def fill_board(board):
            for i in range(size * size):
                row, col = i // size, i % size
                if board[row][col] == 0:
                    shuffle(self.nums)
                    for num in self.nums:
                        if self._check_valid(board, num, (row, col)):
                            board[row][col] = num
                            if self._check_fulfill(board):
                                return True
                            else:
                                if fill_board(board):
                                    return True
                    break
            board[row][col] = 0

        fill_board(board)
        self.board = board
        # initialize masked board
        self.masked_board = self._mask_board()

    def _check_fulfill(self, board):
        for row in range(self.size):
            for col in range(self.size):
                if board[row][col] == 0:
                    return False
        return True

    def _check_valid(self, board, num, pos):
        # check row
        if num not in board[pos[0]]:
            # check column
            if num not in board[:, pos[1]]:
                # check box
                box_nums = []
                box_h = int(np.sqrt(self.size))
                box_w = self.size // box_h
                start_pos = [pos[0] // box_h * box_h, pos[1] // box_w * box_w]
                for m in range(start_pos[0], start_pos[0] + box_h):
                    for n in range(start_pos[1], start_pos[1] + box_w):
                        box_nums.append(board[m][n])
                if num not in box_nums:
                    return True
        return False

    def _mask_board(self):
        board = self.board.copy()
        mask = np.random.choice([True, False], size=board.shape, p=[self.difficulty, 1 - self.difficulty])
        board[mask] = 0
        return board


if __name__ == '__main__':
    sudoku_board = SudokuBoard(size=6, difficulty=0.5)
    board = sudoku_board.board
    print(sudoku_board.board)
    print('==============')
    print(sudoku_board.masked_board)

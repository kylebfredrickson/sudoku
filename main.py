from statistics import median
import time

from board import Cell, SmartSudokuBoard

def print_row(row):
    row = "".join([str(cell) for cell in row])
    print(row)

def array_to_dict(arr):
    d = {}
    for r in range(len(arr)):
        for c in range(len(arr[r])):
            val = arr[r][c]
            if val != 0:
                d[(r,c)] = val
    return d

class SudokuSolver:
    def count_possibilities(board):
        count = 0
        for loc in board:
            cell = board.get_cell(loc)
            if not cell.is_filled():
                count += len(cell.candidates) - 1
        return count

    def get_unfilled(board, locs):
        return list(filter(lambda loc: not board.get_cell(loc).is_filled(), locs))

    # Technique 0: Brute Force
    def backtrack(board, idx=0):
        if idx == board.max:
            return True
        else:
            loc = (idx // board.size, idx % board.size)
            cell = board.get_cell(loc)
            if Cell.is_filled(cell):
                return SudokuSolver.backtrack(board, idx + 1)
            else:
                for candidate in cell.candidates:
                    board.set_cell(loc, candidate)
                    if SudokuSolver.backtrack(board, idx + 1):
                        return True
                    else:
                        board.clear_cell(loc)
                return False

    # Technique 1: Set cells with a single candidate.
    def set_one_remaining(board):
        unfilled = SudokuSolver.get_unfilled(board, [loc for loc in board])
        for loc in unfilled:
            cell = board.get_cell(loc)
            if len(cell.candidates) == 1:
                board.set_cell(loc, list(cell.candidates)[0])

    # Technique 2: Set cells if the candidate only exists once in a logical block.
    def set_unique(board, locs):
        unfilled = SudokuSolver.get_unfilled(board, locs)
        for num in range(1, board.size + 1):
            occurrences = []
            for i in range(len(unfilled)):
                if num in board.get_cell(unfilled[i]).candidates:
                    occurrences.append(i)

            if len(occurrences) == 1:
                board.set_cell(unfilled[occurrences[0]], num)

    def set_all_unique(board):
        for i in range(0, board.size):
            SudokuSolver.set_unique(board, board.get_row(i))
            SudokuSolver.set_unique(board, board.get_col(i))
            SudokuSolver.set_unique(board, board.get_square(i))

    # Technique 3: Remove candidates from row/column if the candidate only exists in one row/column within a square.
    def remove_unique_in_square_row(board, idx, num):
        occurrences = []
        excluded = None
        for row in range(board.square_size):
            square_row = board.get_square_row(idx, row)
            for cell_idx in square_row:
                cell = board.get_cell(cell_idx)
                if not cell.is_filled() and num in cell:
                    occurrences.append(row)
                    excluded = square_row
                    break

        if len(occurrences) == 1:
            locs = board.get_row(idx // board.square_size * board.square_size + occurrences[0],excluded=excluded)
            board.remove_candidate(locs, num)

    def remove_unique_in_square_col(board, idx, num):
        occurrences = []
        excluded = None
        for col in range(board.square_size):
            square_row = board.get_square_col(idx, col)
            for cell_idx in square_row:
                cell = board.get_cell(cell_idx)
                if not cell.is_filled() and num in cell:
                    occurrences.append(col)
                    excluded = square_row
                    break

        if len(occurrences) == 1:
            locs = board.get_col(idx % board.square_size * board.square_size + occurrences[0],excluded=excluded)
            board.remove_candidate(locs, num)

    def remove_all_unique_in_row_col(board):
        for i in range(board.size):
            for num in range(1, board.size + 1):
                SudokuSolver.remove_unique_in_square_row(board, i, num)
                SudokuSolver.remove_unique_in_square_col(board, i, num)

    def solve(board, backtrack=False):
        start = time.time()
        i = 0

        while True:
            old_board = board.copy()

            if backtrack:
                SudokuSolver.backtrack(board)
            else:
                SudokuSolver.set_one_remaining(board)
                SudokuSolver.set_all_unique(board)
                SudokuSolver.remove_all_unique_in_row_col(board)

            i += 1

            if not board.is_legal() or board == old_board or board.is_solved():
                break

        time_to_solve = time.time() - start

        if board.is_solved():
            print(f"Solved in {time_to_solve:.5f}s and {i} iterations.")
        else:
            print(f"Failed. {SudokuSolver.count_possibilities(board)} possibilities.")

    def slow_solve(board):
        start = time.time()
        solvable = SudokuSolver.backtrack(board)
        time_to_solve = time.time() - start
        if solvable:
            print(f"Solved in {time_to_solve:.5f}s.")
        else:
            print(f"Failed.")

def main():
    easy = [[0, 0, 2, 0, 3, 1, 9, 4, 0],
            [0, 8, 0, 9, 6, 0, 3, 0, 0],
            [0, 1, 3, 0, 0, 0, 6, 0, 2],
            [1, 7, 0, 0, 0, 6, 4, 0, 0],
            [3, 0, 0, 5, 4, 8, 0, 6, 0],
            [6, 0, 0, 0, 0, 0, 2, 9, 8],
            [0, 0, 4, 3, 7, 5, 0, 0, 0],
            [7, 0, 0, 1, 0, 0, 0, 3, 9],
            [0, 3, 1, 0, 8, 0, 0, 0, 4],
           ]

    med = [[0, 0, 0, 0, 6, 0, 2, 0, 0],
           [8, 0, 0, 0, 0, 5, 0, 0, 0],
           [0, 0, 0, 7, 2, 8, 0, 0, 0],
           [0, 7, 0, 0, 0, 2, 0, 8, 0],
           [0, 0, 0, 0, 3, 0, 0, 4, 0],
           [1, 0, 2, 4, 5, 0, 0, 6, 0],
           [0, 3, 1, 0, 0, 0, 0, 0, 0],
           [0, 0, 4, 0, 0, 0, 3, 0, 9],
           [5, 0, 0, 0, 0, 0, 4, 0, 0],
          ]

    hard = [[0, 3, 0, 0, 0, 0, 0, 4, 0],
            [0, 0, 0, 0, 3, 8, 0, 6, 0],
            [8, 0, 0, 0, 0, 7, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 9],
            [4, 6, 0, 0, 9, 0, 0, 3, 2],
            [0, 0, 0, 2, 0, 0, 0, 7, 1],
            [0, 5, 0, 0, 1, 3, 0, 0, 0],
            [0, 0, 4, 0, 0, 0, 5, 0, 0],
            [0, 0, 9, 0, 0, 4, 0, 0, 0],
           ]

    little = [[1, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0],
             ]

    little_board = SmartSudokuBoard(array_to_dict(little), 4)
    easy_board = SmartSudokuBoard(array_to_dict(easy))
    med_board = SmartSudokuBoard(array_to_dict(med))
    hard_board = SmartSudokuBoard(array_to_dict(hard))

    board = med_board
    SudokuSolver.solve(board, backtrack=False)
    print(board)

if __name__ == "__main__":
    main()
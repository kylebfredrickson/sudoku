import time
from itertools import combinations

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
    def is_valid(board, loc, num):
        if num in [board.get_cell(loc).value for loc in board.get_filled(board.get_row(loc[0], excluded=loc))]:
            return False
        elif num in [board.get_cell(loc).value for loc in board.get_filled(board.get_col(loc[1], excluded=loc))]:
            return False
        elif num in [board.get_cell(loc).value for loc in board.get_filled(board.get_square(board.loc_to_square_idx(loc), excluded=loc))]:
            return False
        else:
            return True

    def backtrack(board, idx=0):
        if idx == board.max:
            return True
        else:
            loc = (idx // board.size, idx % board.size)
            cell = board.get_cell(loc)
            if Cell.is_filled(cell):
                return SudokuSolver.backtrack(board, idx + 1)
            else:
                for num in range(1, board.size + 1):
                    if SudokuSolver.is_valid(board, loc, num):
                        board.set_cell(loc, num)
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

    # Technique 4:
    def remove_complete_permutation(board, locs, size):
        if size < len(locs):
            indices = [i for i in range(len(locs))]
            for idx_subset in combinations(indices, size):
                vals = set()
                for idx in idx_subset:
                    vals = vals.union(board.get_cell(locs[idx]).candidates)
                if len(vals) == size:
                    for idx in list(set(indices).difference(idx_subset)):
                        for val in vals:
                            board.remove_candidate([locs[idx]], val)

    def remove_all_complete_permutations(board):
        for i in range(board.size):
            for size in range(1,board.size + 1):
                SudokuSolver.remove_complete_permutation(board, board.get_unfilled(board.get_row(i)), size)
                SudokuSolver.remove_complete_permutation(board, board.get_unfilled(board.get_col(i)), size)
                SudokuSolver.remove_complete_permutation(board, board.get_unfilled(board.get_square(i)), size)

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
                SudokuSolver.remove_all_complete_permutations(board)

            i += 1
            if board == old_board:
                backtrack = True

            if not board.is_legal() or board.is_solved():
                break

        time_to_solve = time.time() - start

        if board.is_solved():
            print(f"Solved in {time_to_solve:.5f}s and {i} iterations.")
        else:
            print(f"Failed. {SudokuSolver.count_possibilities(board)} possibilities.")

def main():
    b = [[8, 7, 0, 0, 1, 0, 9, 5, 4],
         [0, 6, 0, 0, 0, 7, 8, 1, 3],
         [0, 0, 0, 0, 0, 0, 6, 2, 7],
         [0, 0, 7, 0, 0, 1, 5, 0, 2],
         [0, 0, 0, 0, 2, 0, 0, 8, 0],
         [5, 0, 0, 0, 0, 0, 0, 3, 0],
         [9, 0, 0, 0, 4, 0, 1, 0, 5],
         [0, 0, 8, 9, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 3, 0, 0],
        ]

    board = SmartSudokuBoard(array_to_dict(b))

    SudokuSolver.solve(board, backtrack=False)
    print(board)

if __name__ == "__main__":
    main()
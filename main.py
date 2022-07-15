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

    def set_one_remaining(board):
        unfilled = SudokuSolver.get_unfilled(board, [loc for loc in board])
        for loc in unfilled:
            cell = board.get_cell(loc)
            if len(cell.candidates) == 1:
                board.set_cell(loc, list(cell.candidates)[0])

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

    # def remove_unique_in_row(board, square_row, square_col, num):
    #     row_occurrences = []
    #     for row in range(0, 3):
    #         for cell in board.get_square_row(square_row, square_col, row):
    #             if num in cell and cell.value() != num:
    #                 row_occurrences.append(row)
    #                 break

    #     if len(row_occurrences) == 1:
    #         print(f"In square ({square_row}, {square_col}), {num} occurs uniquely in row {row_occurrences[0]}")
    #         cols = list(set([x for x in range(0, 3)]) - set([square_col]))
    #         for col in cols:
    #             print(f"\tRemoving {num} from square ({square_row}, {col}) row {row_occurrences[0]}.")
    #             other_row = board.get_square_row(square_row, col, row_occurrences[0])
    #             SudokuSolver.remove_from_all(other_row, [num])

    # def remove_unique_in_col(board, square_row, square_col, num):
    #     col_occurrences = []
    #     for col in range(0, 3):
    #         for cell in board.get_square_col(square_row, square_col, col):
    #             if num in cell and cell.value() != num:
    #                 col_occurrences.append(col)
    #                 break

    #     if len(col_occurrences) == 1:
    #         print(f"In square ({square_row}, {square_col}), {num} occurs uniquely in col {col_occurrences[0]}.")
    #         # Bug here
    #         rows = list(set([x for x in range(0, 3)]) - set([square_row]))
    #         for row in rows:
    #             print(f"\tRemoving {num} from square ({row}, {square_col}) column {col_occurrences[0]}.")
    #             other_row = board.get_square_col(row, square_col, col_occurrences[0])
    #             SudokuSolver.remove_from_all(other_row, [num])
    def remove_unique_in_row_col(board, fn, idx, num, row):
        pass
        # print(fn)

    def remove_all_unique_in_row_col(board):
        for i in range(board.size):
            for num in range(1, board.size + 1):
                SudokuSolver.remove_unique_in_row_col(board, board.get_square_row, i, num, True)
                SudokuSolver.remove_unique_in_row_col(board, board.get_square_col, i, num, False)

    def fast_solve(board):
        start = time.time()

        i = 0
        while True:
            old_board = board.copy()

            SudokuSolver.set_one_remaining(board)
            SudokuSolver.set_all_unique(board)
            SudokuSolver.remove_all_unique_in_row_col(board)

            # 4. Pair trick
            # 5. Triplet trick

            i += 1

            if not board.is_legal() or board == old_board or board.is_solved():
                break

        time_to_solve = time.time() - start

        if board.is_solved():
            print(f"Solved in {time_to_solve:.5f}s and {i} iterations.")
        else:
            print(f"Failed. {SudokuSolver.count_possibilities(board)} possibilities.")

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

    def slow_solve(board):
        start = time.time()
        solvable = SudokuSolver.backtrack(board)
        time_to_solve = time.time() - start
        if solvable:
            print(f"Solved in {time_to_solve:.5f}s.")
        else:
            print(f"Failed.")

def main():
    easy = [[0, 0, 1, 0, 5, 3, 7, 8, 9],
            [7, 8, 4, 0, 0, 1, 0, 0, 0],
            [5, 3, 0, 8, 7, 0, 0, 0, 4],
            [0, 0, 0, 5, 2, 0, 1, 6, 0],
            [1, 0, 2, 6, 0, 0, 9, 0, 0],
            [0, 0, 7, 0, 0, 8, 0, 4, 5],
            [3, 2, 0, 0, 0, 0, 5, 0, 0],
            [0, 7, 0, 1, 9, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 5, 4, 7, 6],
           ]

    med = [[0, 0, 0, 0, 0, 0, 0, 3, 7],
           [0, 0, 9, 8, 0, 0, 0, 0, 5],
           [0, 3, 0, 4, 0, 0, 0, 0, 2],
           [0, 0, 0, 0, 6, 0, 0, 0, 3],
           [5, 7, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 4, 0, 0, 0, 8, 6, 0],
           [0, 8, 0, 7, 3, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 2, 0, 9, 0, 0, 0, 0],
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

    board = hard_board
    # SudokuSolver.fast_solve(board)
    SudokuSolver.slow_solve(board)
    print(board)

if __name__ == "__main__":
    main()
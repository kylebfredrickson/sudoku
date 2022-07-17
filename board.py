import copy
from math import sqrt
import numpy

from cell import Cell

def exclude(locs, excluded):
    if type(excluded) is not list:
        excluded = [excluded]
    return list(filter(lambda loc: loc not in excluded, locs))

class SudokuBoard:
    def __init__(self, nums, size=9):
        self.size = size
        self.square_size = int(sqrt(size))
        self.max = size * size
        self.board = numpy.array([[Cell(size) for _ in range(size)] for _ in range(size)])

        for (loc, num) in nums.items():
            self.set_cell(loc, num)

    def loc_to_square_idx(self, loc):
        return loc[0] // self.square_size * self.square_size + loc[1] // self.square_size

    def get_cell(self, loc):
        return self.board[loc[0], loc[1]]

    def set_cell(self, loc, value):
        self.board[loc[0], loc[1]].set(value)

    def clear_cell(self, loc):
        self.board[loc[0], loc[1]].clear()

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < self.max:
            result = (self.n // self.size, self.n % self.size)
            self.n += 1
            return result
        else:
            raise StopIteration

    def get_row(self, row, excluded=[]):
        return exclude([(row, col) for col in range(self.size)], excluded)

    def get_col(self, col, excluded=[]):
        return exclude([(row, col) for row in range(self.size)], excluded)

    def get_square(self, idx, excluded=[]):
        row = idx // self.square_size
        col = idx % self.square_size
        square = [(self.square_size * row + i // self.square_size,
                   self.square_size * col + i % self.square_size) for i in range(self.size)]
        return exclude(square, excluded)

    def get_square_row(self, idx, row, excluded=[]):
        square = self.get_square(idx)
        return exclude([square[row * self.square_size + i] for i in range(self.square_size)], excluded)

    def get_square_col(self, idx, col, excluded=[]):
        square = self.get_square(idx)
        return exclude([square[i * self.square_size + col] for i in range(self.square_size)], excluded)

    def get_filled(self, locs):
        return list(filter(lambda loc: self.get_cell(loc).is_filled(), locs))

    def is_filled(self):
        for loc in self:
            if not self.get_cell(loc).is_filled():
                return False
        return True

    def is_legal(self):
        for loc in self:
            if len(self.get_cell(loc).candidates) == 0:
                return False
        return True

    def is_solved(self):
        if self.is_filled():
            all = [x for x in range(1, self.size + 1)]

            for i in range(0, self.size):
                row = [self.get_cell(loc).value for loc in self.get_row(i)]
                row.sort()
                col = [self.get_cell(loc).value for loc in self.get_col(i)]
                col.sort()
                square = [self.get_cell(loc).value for loc in self.get_square(i)]
                square.sort()

                if row != all or col != all or square != all:
                    return False
            return True
        else:
            return False

    def copy(self):
        return copy.deepcopy(self)

    def __eq__(self, other):
        for loc in self:
            if not self.get_cell(loc) == other.get_cell(loc):
                return False
        return True

    def __str__(self):
        return "\n".join(["".join([str(cell) for cell in row]) for row in self.board])

class SmartSudokuBoard(SudokuBoard):
    def __init__(self, nums, size=9):
        super().__init__(nums, size)

    def remove_candidate(self, locs, candidate):
        for loc in locs:
            self.get_cell(loc) - candidate

    def __add_candidate(self, locs, candidate):
        for loc in locs:
            self.get_cell(loc) + candidate

    def set_cell(self, loc, value):
        super().set_cell(loc, value)

        row_locs = self.get_row(loc[0], excluded=loc)
        self.remove_candidate(row_locs, value)

        col_locs = self.get_col(loc[1], excluded=loc)
        self.remove_candidate(col_locs, value)

        square_locs = self.get_square(self.loc_to_square_idx(loc), excluded=loc)
        self.remove_candidate(square_locs, value)

    # Possible that there is a bug here.
    def clear_cell(self, loc):
        value = self.get_cell(loc).value
        super().clear_cell(loc)

        # Remove known values from candidate list.
        nums = [self.get_cell(loc).value for loc in self.get_filled(self.get_row(loc[0]))]
        nums.extend([self.get_cell(loc).value for loc in self.get_filled(self.get_col(loc[1]))])
        nums.extend([self.get_cell(loc).value for loc in self.get_filled(self.get_square(self.loc_to_square_idx(loc)))])
        for num in list(set(nums)):
            self.remove_candidate([loc], num)

        # Add value back to candidate lists for rows, column, and square.
        row_locs = self.get_row(loc[0], excluded=loc)
        self.__add_candidate(row_locs, value)

        col_locs = self.get_col(loc[1], excluded=loc)
        self.__add_candidate(col_locs, value)

        square_locs = self.get_square(self.loc_to_square_idx(loc), excluded=loc)
        self.__add_candidate(square_locs, value)
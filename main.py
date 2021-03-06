import numpy as np


def easy_puzzle():
    return np.array([
        [7, 1, 0, 0, 0, 9, 0, 8, 0],
        [3, 0, 4, 0, 2, 0, 0, 0, 7],
        [0, 0, 0, 7, 0, 1, 6, 0, 0],
        [1, 7, 0, 0, 6, 0, 0, 0, 0],
        [2, 8, 0, 0, 9, 0, 0, 3, 1],
        [0, 0, 0, 0, 8, 0, 0, 6, 9],
        [0, 0, 2, 3, 0, 4, 0, 0, 0],
        [4, 0, 0, 0, 1, 0, 3, 0, 6],
        [0, 3, 0, 9, 0, 0, 0, 5, 2],
    ])


def medium_puzzle():
    return np.array([
        [4, 1, 0, 0, 2, 8, 0, 0, 0],
        [0, 8, 9, 0, 0, 1, 0, 0, 0],
        [2, 5, 0, 0, 6, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 2, 0, 9, 0],
        [0, 2, 1, 0, 9, 0, 8, 4, 0],
        [0, 3, 0, 8, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 4, 0, 0, 7, 9],
        [0, 0, 0, 1, 0, 0, 4, 6, 0],
        [0, 0, 0, 9, 3, 0, 0, 2, 8],
    ])


def hard_puzzle():
    return np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 3],
        [0, 0, 3, 4, 9, 8, 0, 0, 0],
        [0, 9, 0, 7, 0, 0, 0, 1, 8],
        [0, 0, 7, 0, 0, 0, 5, 3, 4],
        [0, 0, 0, 0, 7, 0, 0, 0, 0],
        [3, 8, 5, 0, 0, 0, 9, 0, 0],
        [6, 5, 0, 0, 0, 1, 0, 8, 0],
        [0, 0, 0, 5, 3, 4, 6, 0, 0],
        [9, 0, 0, 0, 0, 0, 0, 0, 0],
    ])


class Sudoku:
    def __init__(self):
        self.grid = hard_puzzle()
        self.options = self.init_options()

    def __repr__(self):
        string = ''
        num = 3
        vert = 3
        for row in self.grid:
            for c in row:
                string += str(c) + ' ' if c != 0 else '  '
                num -= 1
                if not num:
                    string += '|'
                    num = 3
            string += '\n'
            vert -= 1
            if not vert:
                string += '-' * 20 + '\n'
                vert = 3
        return string

    def init_options(self):
        options = []
        for r in range(self.grid.shape[0]):
            options.append([])
            for c in range(self.grid.shape[1]):
                options[r].append(set(range(1, 10)))

        return options

    def exclude_options(self):
        self.options = self.init_options()
        for r in range(self.grid.shape[0]):
            for c in range(self.grid.shape[1]):
                self._exclude_row_and_column(r, c)

    def _exclude_row_and_column(self, r, c):
        # get rid of options if there is already a given number
        if self.grid[r][c]:
            self.options[r][c] = set()
            return

        # get rid of number options in same row
        for option in self.grid[r]:
            if option in self.options[r][c]:
                self.options[r][c].remove(option)

        # get rid of number options in same col
        for row in range(self.grid.shape[0]):
            option = self.grid[row][c]
            if option in self.options[r][c]:
                self.options[r][c].remove(option)

        # get rid of numbers in same box
        self.remove_box(r, c)

    def remove_box(self, r, c):
        if 0 <= r <= 2:
            if 0 <= c <= 2:
                self._remove_options_box(r, c, range(3), range(3))
                return
            if 3 <= c <= 5:
                self._remove_options_box(r, c, range(3), range(3, 6))
                return
            if 6 <= c <= 8:
                self._remove_options_box(r, c, range(3), range(6, 9))
                return

        if 3 <= r <= 5:
            if 0 <= c <= 2:
                self._remove_options_box(r, c, range(3, 6), range(3))
                return
            if 3 <= c <= 5:
                self._remove_options_box(r, c, range(3, 6), range(3, 6))
                return
            if 6 <= c <= 8:
                self._remove_options_box(r, c, range(3, 6), range(6, 9))
                return

        if 6 <= r <= 8:
            if 0 <= c <= 2:
                self._remove_options_box(r, c, range(6, 9), range(3))
                return
            if 3 <= c <= 5:
                self._remove_options_box(r, c, range(6, 9), range(3, 6))
                return
            if 6 <= c <= 8:
                self._remove_options_box(r, c, range(6, 9), range(6, 9))
                return

    def _remove_options_box(self, r, c, rows, columns):
        for i in rows:
            for j in columns:
                if self.grid[i][j] in self.options[r][c]:
                    self.options[r][c].remove(self.grid[i][j])

    def passes_constraints(self):
        # check each row - make sure no duplicates
        # check each col - make sure no duplicates
        # check each box - make sure no duplicates
        return self.no_duplicate_rows() and self.no_duplicate_columns() and self.no_duplicate_boxes()

    def no_duplicate_rows(self):
        for r in range(self.grid.shape[0]):
            only1 = set(range(1, 10))  # 1,2,3,4,5,6,7,8,9
            for c in range(self.grid.shape[1]):
                candidate = self.grid[r][c]
                if candidate:
                    try:
                        only1.remove(self.grid[r][c])
                    except KeyError:
                        return False
        return True

    def no_duplicate_columns(self):
        for c in range(self.grid.shape[1]):
            only1 = set(range(1, 10))  # 1,2,3,4,5,6,7,8,9
            for r in range(self.grid.shape[0]):
                candidate = self.grid[r][c]
                if candidate:
                    try:
                        only1.remove(self.grid[r][c])
                    except KeyError:
                        return False
        return True

    def no_duplicate_boxes(self):
        value = True
        value &= self._no_duplicates_in_box(range(3), range(3))
        value &= self._no_duplicates_in_box(range(3), range(3, 6))
        value &= self._no_duplicates_in_box(range(3), range(6, 9))

        value &= self._no_duplicates_in_box(range(3, 6), range(3))
        value &= self._no_duplicates_in_box(range(3, 6), range(3, 6))
        value &= self._no_duplicates_in_box(range(3, 6), range(6, 9))

        value &= self._no_duplicates_in_box(range(6, 9), range(3))
        value &= self._no_duplicates_in_box(range(6, 9), range(3, 6))
        value &= self._no_duplicates_in_box(range(6, 9), range(6, 9))

        return value

    def _no_duplicates_in_box(self, rows, cols):
        only1 = set(range(1, 10))  # 1,2,3,4,5,6,7,8,9
        for r in rows:
            for c in cols:
                candidate = self.grid[r][c]
                if candidate:
                    try:
                        only1.remove(self.grid[r][c])
                    except KeyError:
                        return False
        return True

    def is_complete(self):
        for row in self.grid:
            for val in row:
                if not val:
                    return False
        return True

    def _remove_non_unique_in_coord(self, r, c, options_count):
        coord_options_set = self.options[r][c]
        new_coord_options_set = set()

        for num in coord_options_set:
            if options_count[num] == 1:
                new_coord_options_set.add(num)

        self.options[r][c] = new_coord_options_set

    def _naked_rows(self, r, row_options_count):
        for c in range(self.grid.shape[1]):
            coord_options_set = self.options[r][c]
            coord_already_filtered = False
            for num in coord_options_set:
                if row_options_count[num] == 1 and not coord_already_filtered:
                    self._remove_non_unique_in_coord(r, c, row_options_count)
                    coord_already_filtered = True

    def _unique_option_rows(self):
        for r in range(self.grid.shape[0]):
            row_options_count = self._unique_option_row(r)
            self._naked_rows(r, row_options_count)

    def _unique_option_row(self, r):
        row_options_count = np.zeros(10, int)
        for c in range(self.grid.shape[1]):
            coord_options_set = self.options[r][c]
            for i in coord_options_set:
                row_options_count[i] += 1
        return row_options_count

    def _naked_columns(self, c, col_options_count):
        for r in range(self.grid.shape[0]):
            coord_options_set = self.options[r][c]
            coord_already_filtered = False
            for num in coord_options_set:
                if col_options_count[num] == 1 and not coord_already_filtered:
                    self._remove_non_unique_in_coord(r, c, col_options_count)
                    coord_already_filtered = True

    def _unique_option_columns(self):
        for c in range(self.grid.shape[1]):
            col_options_count = self._unique_option_column(c)
            self._naked_columns(c, col_options_count)

    def _unique_option_column(self, c):
        col_options_count = np.zeros(10, int)
        for r in range(self.grid.shape[0]):
            coord_options_set = self.options[r][c]
            for i in coord_options_set:
                col_options_count[i] += 1
        return col_options_count

    def _naked_boxes(self, rows, cols, options_count):
        for r in rows:
            for c in cols:
                coord_options_set = self.options[r][c]
                coord_already_filtered = False
                for num in coord_options_set:
                    if options_count[num] == 1 and not coord_already_filtered:
                        self._remove_non_unique_in_coord(r, c, options_count)
                        coord_already_filtered = True

    def _unique_option_boxes(self):
        box_1_options_count = self._unique_option_box(range(3), range(3))
        self._naked_boxes(range(3), range(3), box_1_options_count)

        box_2_options_count = self._unique_option_box(range(3), range(3, 6))
        self._naked_boxes(range(3), range(3, 6), box_2_options_count)

        box_3_options_count = self._unique_option_box(range(3), range(6, 9))
        self._naked_boxes(range(3), range(6, 9), box_3_options_count)

        box_4_options_count = self._unique_option_box(range(3, 6), range(3))
        self._naked_boxes(range(3, 6), range(3), box_4_options_count)

        box_5_options_count = self._unique_option_box(range(3, 6), range(3, 6))
        self._naked_boxes(range(3, 6), range(3, 6), box_5_options_count)

        box_6_options_count = self._unique_option_box(range(3, 6), range(6, 9))
        self._naked_boxes(range(3, 6), range(6, 9), box_6_options_count)

        box_7_options_count = self._unique_option_box(range(6, 9), range(3))
        self._naked_boxes(range(6, 9), range(3), box_7_options_count)

        box_8_options_count = self._unique_option_box(range(6, 9), range(3, 6))
        self._naked_boxes(range(6, 9), range(3, 6), box_8_options_count)

        box_9_options_count = self._unique_option_box(range(6, 9), range(6, 9))
        self._naked_boxes(range(6, 9), range(6, 9), box_9_options_count)

    def _unique_option_box(self, rows, cols):
        box_options_count = np.zeros(10, int)
        for r in rows:
            for c in cols:
                coord_options_set = self.options[r][c]
                for i in coord_options_set:
                    box_options_count[i] += 1
        return box_options_count

    def recurse(self):
        # if not self.passes_constraints():
        #     return
        if self.is_complete():
            return self

        self.exclude_options()
        self._unique_option_rows()
        self._unique_option_columns()
        self._unique_option_boxes()

        queue = []
        for r in range(self.grid.shape[0]):
            for c in range(self.grid.shape[1]):
                options = self.options[r][c]
                if options and isinstance(options, set) and len(options) == 0:
                    return

                if options:
                    node = Node(r, c, options)
                    queue.append(node)

        queue.sort(key=len)

        while queue:
            node = queue.pop(0)
            for option in node.options:
                self.grid[node.r][node.c] = option
                # check works
                # check done
                solution = self.recurse()
                if solution:
                    return solution
                self.grid[node.r][node.c] = 0


class Node:
    def __init__(self, r, c, options):
        self.r = r
        self.c = c
        self.options = options

    def __len__(self):
        return len(self.options)

    def __repr__(self):
        return f'({self.r}, {self.c}) - ' + repr(self.options)


if __name__ == '__main__':
    s = Sudoku()
    print(s.recurse())

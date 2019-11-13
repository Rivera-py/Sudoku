import itertools


# Takes initial information and replaces unknown values with possible values
def initial_possibilities(matrix):
    for row in matrix:
        for column_index, cell in enumerate(row):
            if cell == "?":
                row[column_index] = list(range(1, 10, 1))


# Locks a cell as its value but replacing it with a string -- should only be passed an integer
def lock_cell(row_index, column_index, matrix):
    matrix[row_index][column_index] = str(matrix[row_index][column_index])


# Removing possibilities based on solved cells -- can only be given a solved cell
def update_row(update_number, row_index, matrix):
    for col_index, cell in enumerate(matrix[row_index]):
        if isinstance(cell, list):
            if update_number in cell:
                cell.remove(update_number)


def update_column(update_number, column_index, matrix):
    for row in matrix:
        if isinstance(row[column_index], list):
            if update_number in row[column_index]:
                row[column_index].remove(update_number)


def update_grid(update_number, row_index, column_index, matrix):
    grid_row_start = 3 * int(row_index / 3)
    grid_column_start = 3 * int(column_index / 3)
    for grid_row in range(grid_row_start, grid_row_start + 3):
        for grid_column in range(grid_column_start, grid_column_start + 3):
            if isinstance(matrix[grid_row][grid_column], list):
                if update_number in matrix[grid_row][grid_column]:
                    matrix[grid_row][grid_column].remove(update_number)


# Locks in a cells value and updates row/column/grid adjacent unsolved cells
def solve_cell(row_index, column_index, matrix):
    update_row(matrix[row_index][column_index], row_index, matrix)
    update_column(matrix[row_index][column_index], column_index, matrix)
    update_grid(matrix[row_index][column_index], row_index, column_index, matrix)
    lock_cell(row_index, column_index, matrix)


# Checks over every cell for solvable cells
def scan_and_solve(matrix):
    for row_index, row in enumerate(matrix):
        for column_index, cell in enumerate(row):
            if isinstance(cell, int):
                solve_cell(row_index, column_index, matrix)


# If a cell has only one possibility, it must be that number
def one_possibility(matrix):
    for row in matrix:
        for column_index, elt in enumerate(row):
            if isinstance(elt, list):
                if len(elt) == 1:
                    row[column_index] = row[column_index][0]


def unique_row_possibility(matrix):
    cell_solution_possible = False
    for row in matrix:
        for column_index, cell in enumerate(row):
            if isinstance(cell, list):
                for possibility in cell:
                    counter = 0
                    for check_column_index, checking_cell in enumerate(row):
                        if isinstance(checking_cell, list):
                            if possibility in checking_cell:
                                counter += 1
                    if counter == 1:
                        row[column_index] = possibility
                        cell_solution_possible = True
                        break
    return cell_solution_possible


def unique_column_possibility(matrix):
    cell_solution_possible = False
    for row_index, row in enumerate(matrix):
        for column_index, cell in enumerate(row):
            if isinstance(cell, list):
                for possibility in cell:
                    counter = 0
                    for check_row_index, checking_row in enumerate(matrix):
                        if isinstance(checking_row[column_index], list):
                            if possibility in checking_row[column_index]:
                                counter += 1
                    if counter == 1:
                        row[column_index] = possibility
                        cell_solution_possible = True
                        break
    return cell_solution_possible


def unique_grid_possibility(matrix):
    for row_index, row in enumerate(matrix):
        for column_index, cell in enumerate(row):
            if isinstance(cell, list):
                for possibility in cell:
                    counter = 0
                    grid_row_start = 3 * int(row_index / 3)
                    grid_column_start = 3 * int(column_index / 3)
                    for grid_row in range(grid_row_start, grid_row_start + 3):
                        for grid_column in range(grid_column_start, grid_column_start + 3):
                            if isinstance(matrix[grid_row][grid_column], list):
                                if (grid_row, grid_column) != (row_index, column_index):
                                    counter += 1
                    if counter == 1:
                        row[column_index] = possibility
                        return True
    return False


# Functions designed to obtain all possibilities of all unsolved cells of each row/column in a given grid
def retrieve_grid_row_possibilities(grid_row_index, grid_column_index, matrix):
    grid_row_start = 3 * grid_row_index
    grid_column_start = 3 * grid_column_index
    grid_row_possibilities = [[], [], []]
    for grid_row in range(3):
        for grid_column in range(3):
            if isinstance(matrix[grid_row_start + grid_row][grid_column_start + grid_column], list):
                grid_row_possibilities[grid_row] += matrix[grid_row_start + grid_row][grid_column_start + grid_column]
    for row_possibilities in range(3):
        grid_row_possibilities[row_possibilities] = list(set(grid_row_possibilities[row_possibilities]))
    return grid_row_possibilities


def retrieve_grid_col_possibilities(grid_row_index, grid_column_index, matrix):
    grid_row_start = 3 * grid_row_index
    grid_column_start = 3 * grid_column_index
    grid_col_possibilities = [[], [], []]
    for grid_row in range(3):
        for grid_col in range(3):
            if isinstance(matrix[grid_row_start + grid_row][grid_column_start + grid_col], list):
                grid_col_possibilities[grid_col] += matrix[grid_row_start + grid_row][grid_column_start + grid_col]
    for row_possibilities in range(3):
        grid_col_possibilities[row_possibilities] = list(set(grid_col_possibilities[row_possibilities]))
    return grid_col_possibilities


# Using the retrieve functions to find grid row/column-secluded possibilities and eliminate them from the other grids
def eliminate_grid_secluded_row_possibilities(grid_row_index, grid_column_index, matrix):
    grid_row_possibilities = retrieve_grid_row_possibilities(grid_row_index, grid_column_index, matrix)
    for row_index, grid_row in enumerate(grid_row_possibilities):
        for possibility in grid_row:
            counter = 0
            for row_check in range(3):
                if possibility in grid_row_possibilities[row_check]:
                    counter += 1
            if counter == 1:
                amend_row_index = 3 * grid_row_index + row_index
                grid_column_start = 3 * grid_column_index
                for non_grid_cells in set(range(9)) - set(range(grid_column_start, grid_column_start + 3)):
                    if isinstance(matrix[amend_row_index][non_grid_cells], list):
                        if possibility in matrix[amend_row_index][non_grid_cells]:
                            matrix[amend_row_index][non_grid_cells].remove(possibility)


def eliminate_grid_secluded_column_possibilities(grid_row_index, grid_column_index, matrix):
    grid_column_possibilities = retrieve_grid_col_possibilities(grid_row_index, grid_column_index, matrix)
    for column_index, grid_col in enumerate(grid_column_possibilities):
        for possibility in grid_col:
            counter = 0
            for column_check in range(3):
                if possibility in grid_column_possibilities[column_check]:
                    counter += 1
            if counter == 1:
                grid_row_start = 3 * grid_row_index
                amend_column_index = 3 * grid_column_index + column_index
                for non_grid_cells in set(range(9)) - set(range(grid_row_start, grid_row_start + 3)):
                    if isinstance(matrix[non_grid_cells][amend_column_index], list):
                        if possibility in matrix[non_grid_cells][amend_column_index]:
                            matrix[non_grid_cells][amend_column_index].remove(possibility)


# Extending the two algorithms to each grid
def eliminate_all_grid_secluded_row_possibilities(matrix):
    for grid_row in range(3):
        for grid_column in range(3):
            eliminate_grid_secluded_row_possibilities(grid_row, grid_column, matrix)


def eliminate_all_grid_secluded_column_possibilities(matrix):
    for grid_row in range(3):
        for grid_column in range(3):
            eliminate_grid_secluded_column_possibilities(grid_row, grid_column, matrix)


# Checks for n cells containing the same n possibilities and removes all those possibilities on the same row/column/grid
def locked_row_possibilities(row):
    unsolved_cells = []
    for column_index, cell in enumerate(row):
        if isinstance(cell, list):
            unsolved_cells += [[column_index, cell]]
    for group_size in range(2, 5):
        unsolved_cells_correct_size = []
        for unsolved_cell_check in unsolved_cells:
            if len(unsolved_cell_check[1]) == group_size:
                unsolved_cell_check[1].sort()
                unsolved_cells_correct_size += [unsolved_cell_check]
        for correct_cell in unsolved_cells_correct_size:
            column_indices = []
            for comparing_cells in unsolved_cells_correct_size:
                if comparing_cells[1] == correct_cell[1]:
                    column_indices += [comparing_cells[0]]
            if len(column_indices) == group_size:
                for removing_index in set(range(9)) - set(column_indices):
                    if isinstance(row[removing_index], list):
                        row[removing_index] = list(set(row[removing_index]) - set(correct_cell[1]))


def locked_column_possibilities(column, matrix):
    unsolved_cells = []
    for row_index, row in enumerate(matrix):
        if isinstance(row[column], list):
            unsolved_cells += [[row_index, row[column]]]
    for group_size in range(2, 5):
        unsolved_cells_correct_size = []
        for unsolved_cell_check in unsolved_cells:
            if len(unsolved_cell_check[1]) == group_size:
                unsolved_cell_check[1].sort()
                unsolved_cells_correct_size += [unsolved_cell_check]
        for correct_cell in unsolved_cells_correct_size:
            row_indices = []
            for comparing_cells in unsolved_cells_correct_size:
                if comparing_cells[1] == correct_cell[1]:
                    row_indices += [comparing_cells[0]]
            if len(row_indices) == group_size:
                for removingindex in set(range(9)) - set(row_indices):
                    if isinstance(matrix[removingindex][column], list):
                        matrix[removingindex][column] = list(set(matrix[removingindex][column]) - set(correct_cell[1]))


def locked_grid_possibilities(grid_row_index, grid_column_index, matrix):
    unsolved_cells = []
    grid_row_start = 3 * grid_row_index
    grid_column_start = 3 * grid_column_index
    for grid_row in range(grid_row_start, grid_row_start + 3):
        for grid_column in range(grid_column_start, grid_column_start + 3):
            if isinstance(matrix[grid_row][grid_column], list):
                unsolved_cells += [[grid_row, grid_column, matrix[grid_row][grid_column]]]
    for group_size in range(2, 5):
        unsolved_cells_correct_size = []
        for unsolved_cell_check in unsolved_cells:
            if len(unsolved_cell_check[2]) == group_size:
                unsolved_cells_correct_size += [unsolved_cell_check]
        for correct_cell in unsolved_cells_correct_size:
            cell_indices = []
            for comparing_cell in unsolved_cells_correct_size:
                if comparing_cell[2] == correct_cell[2]:
                    cell_indices += [[comparing_cell[0], comparing_cell[1]]]
            if len(cell_indices) == group_size:
                for rem_row in range(grid_row_start, grid_row_start + 3):
                    for rem_col in range(grid_column_start, grid_column_start + 3):
                        if not([rem_row, rem_col] in cell_indices):
                            if isinstance(matrix[rem_row][rem_col], list):
                                rem_vals = set(correct_cell[2])
                                matrix[rem_row][rem_col] = list(set(matrix[rem_row][rem_col]) - rem_vals)


# Applies each of the three "locked" methods to each respective row/column/grid
def all_locked_row_possibilities(matrix):
    for row in matrix:
        locked_row_possibilities(row)


def all_locked_col_possibilities(matrix):
    for column_index in range(9):
        locked_column_possibilities(column_index, matrix)


def all_locked_grid_possibilitites(matrix):
    for grid_row_index in range(3):
        for grid_col_index in range(3):
            locked_grid_possibilities(grid_row_index, grid_col_index, matrix)


# If there is a grid row/column possibility which is not in adjacent cells then it should be secluded to that line
def reverse_grid_seclude_row_possibilities(grid_row_index, grid_column_index, matrix):
    grid_row_start = 3 * grid_row_index
    grid_column_start = 3 * grid_column_index
    grid_row_possibilities = retrieve_grid_row_possibilities(grid_row_index, grid_column_index, matrix)
    for row_index, row_possibilities in enumerate(grid_row_possibilities):
        for row_possibility in row_possibilities:
            counter = 0
            for non_grid_column in set(range(9)) - set(range(grid_column_start, grid_column_start + 3)):
                if isinstance(matrix[grid_row_start + row_index][non_grid_column], list):
                    if row_possibility in matrix[grid_row_start + row_index][non_grid_column]:
                        counter += 1
            if counter == 0:
                for not_current_row in set(range(grid_row_start, grid_row_start + 3)) - {grid_row_start + row_index}:
                    for column_index in range(grid_column_start, grid_column_start + 3):
                        if isinstance(matrix[not_current_row][column_index], list):
                            if row_possibility in matrix[not_current_row][column_index]:
                                matrix[not_current_row][column_index].remove(row_possibility)


def reverse_grid_seclude_column_possibilities(grid_row_index, grid_column_index, matrix):
    grid_row_start = 3 * grid_row_index
    grid_col_start = 3 * grid_column_index
    grid_row_possibilities = retrieve_grid_col_possibilities(grid_row_index, grid_column_index, matrix)
    for col_index, column_possibilities in enumerate(grid_row_possibilities):
        for column_possibility in column_possibilities:
            counter = 0
            for non_grid_row in set(range(9)) - set(range(grid_row_start, grid_row_start + 3)):
                if isinstance(matrix[non_grid_row][grid_col_start + col_index], list):
                    if column_possibility in matrix[non_grid_row][grid_col_start + col_index]:
                        counter += 1
            if counter == 0:
                for not_current_column in set(range(grid_col_start, grid_col_start + 3)) - {grid_col_start + col_index}:
                    for row_index in range(grid_row_start, grid_row_start + 3):
                        if isinstance(matrix[row_index][not_current_column], list):
                            if column_possibility in matrix[row_index][not_current_column]:
                                matrix[row_index][not_current_column].remove(column_possibility)


def reverse_all_grid_seclude_row_possibilities(matrix):
    for grid_row_index in range(3):
        for grid_column_index in range(3):
            reverse_grid_seclude_row_possibilities(grid_row_index, grid_column_index, matrix)


def reverse_all_grid_seclude_column_possibilities(matrix):
    for grid_row_index in range(3):
        for grid_column_index in range(3):
            reverse_grid_seclude_column_possibilities(grid_row_index, grid_column_index, matrix)


# If n cells in a row/column/grid each have n unique possibilities then they should only contain those values
def hidden_row_subset(row):
    unsolved_cells = []
    for column_index, cell in enumerate(row):
        if isinstance(cell, list):
            row[column_index].sort()
            unsolved_cells += [[column_index, cell]]
    for group_size in range(2, 5):
        for unsolved_cell in unsolved_cells:
            for possibility_subset in itertools.combinations(unsolved_cell[1], group_size):
                column_indices = []
                for comparison_cell in unsolved_cells:
                    if set(possibility_subset).issubset(set(comparison_cell[1])):
                        column_indices += [comparison_cell[0]]
                if len(column_indices) == group_size:
                    counter = 0
                    for checking_cell in unsolved_cells:
                        disjoint = set(checking_cell[1]).isdisjoint(set(possibility_subset))
                        if (not disjoint) and (not checking_cell[0] in column_indices):
                            counter += 1
                    if counter == 0:
                        for column in column_indices:
                            row[column] = list(possibility_subset)


def hidden_column_subset(column, matrix):
    unsolved_cells = []
    for row_index, row in enumerate(matrix):
        if isinstance(row[column], list):
            unsolved_cells += [[row_index, row[column]]]
    for group_size in range(2, 5):
        for unsolved_cell in unsolved_cells:
            for possibility_subset in itertools.combinations(unsolved_cell[1], group_size):
                row_indices = []
                for comparison_cell in unsolved_cells:
                    if set(possibility_subset).issubset(set(comparison_cell[1])):
                        row_indices += [comparison_cell[0]]
                if len(row_indices) == group_size:
                    counter = 0
                    for checking_cell in unsolved_cells:
                        disjoint = set(checking_cell[1]).isdisjoint(set(possibility_subset))
                        if (not disjoint) and (not checking_cell[0] in row_indices):
                            counter += 1
                    if counter == 0:
                        for row in row_indices:
                            matrix[row][column] = list(possibility_subset)


def hidden_grid_subset(grid_row_index, grid_column_index, matrix):
    unsolved_cells = []
    grid_row_start = 3 * grid_row_index
    grid_column_start = 3 * grid_column_index
    for grid_row in range(grid_row_start, grid_row_start + 3):
        for grid_column in range(grid_column_start, grid_column_start + 3):
            if isinstance(matrix[grid_row][grid_column], list):
                unsolved_cells += [[(grid_row, grid_column), matrix[grid_row][grid_column]]]
    for group_size in range(2, 5):
        for unsolved_cell in unsolved_cells:
            for possibility_subset in itertools.combinations(unsolved_cell[1], group_size):
                grid_indices = []
                for comparison_cell in unsolved_cells:
                    if set(possibility_subset).issubset(set(comparison_cell[1])):
                        grid_indices += [comparison_cell[0]]
                if len(grid_indices) == group_size:
                    counter = 0
                    for checking_cell in unsolved_cells:
                        disjoint = set(checking_cell[1]).isdisjoint(set(possibility_subset))
                        if (not disjoint) and (not checking_cell[0] in grid_indices):
                            counter += 1
                    if counter == 0:
                        for grid in grid_indices:
                            matrix[grid[0]][grid[1]] = list(possibility_subset)


def all_hidden_row_subset(matrix):
    for row in matrix:
        hidden_row_subset(row)


def all_hidden_column_subset(column, matrix):
    for column_index in range(9):
        hidden_column_subset(column_index, matrix)


def all_hidden_grid_subset(matrix):
    for grid_row_index in range(3):
        for grid_column_index in range(3):
            hidden_grid_subset(grid_row_index, grid_column_index, matrix)

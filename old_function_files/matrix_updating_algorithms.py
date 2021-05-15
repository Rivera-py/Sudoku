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
def lone_singles(matrix):
    for row in matrix:
        for column_index, elt in enumerate(row):
            if isinstance(elt, list):
                if len(elt) == 1:
                    row[column_index] = row[column_index][0]


def hidden_singles_rows(matrix):
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
                        return True
    return False


def hidden_singles_columns(matrix):
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
                        return True
    return False


def hidden_singles_grids(matrix):
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
                                if possibility in matrix[grid_row][grid_column]:
                                    counter += 1
                    if counter == 1:
                        row[column_index] = possibility
                        return True
    return False





# If n possibilities are relegated to n cells in a row/column/grid, then those possibilities are only in those cells
def naked_subset_row(row):
    unsolved_cells = []
    for column_index, cell in enumerate(row):
        if isinstance(cell, list):
            unsolved_cells += [[column_index, cell]]
    for group_size in range(2, 5):
        for cell_subset in itertools.combinations(unsolved_cells, group_size):
            collective_possibilities = []
            column_indices = []
            for selected_cell in cell_subset:
                collective_possibilities += selected_cell[1]
                column_indices += [selected_cell[0]]
            if len(set(collective_possibilities)) == group_size:
                for non_subset_cell in unsolved_cells:
                    if not non_subset_cell[0] in column_indices:
                        row[non_subset_cell[0]] = list(set(row[non_subset_cell[0]]) - set(collective_possibilities))


def naked_subset_column(column, matrix):
    unsolved_cells = []
    for row_index, row in enumerate(matrix):
        if isinstance(row[column], list):
            unsolved_cells += [[row_index, row[column]]]
    for group_size in range(2, 5):
        for cell_subset in itertools.combinations(unsolved_cells, group_size):
            collective_possibilities = []
            row_indices = []
            for selected_cell in cell_subset:
                collective_possibilities += selected_cell[1]
                row_indices += [selected_cell[0]]
            if len(set(collective_possibilities)) == group_size:
                for non_subset_cell in unsolved_cells:
                    if not non_subset_cell[0] in row_indices:
                        replacing_set = list(set(matrix[non_subset_cell[0]][column]) - set(collective_possibilities))
                        matrix[non_subset_cell[0]][column] = replacing_set


def naked_subset_grid(grid_row_index, grid_column_index, matrix):
    unsolved_cells = []
    grid_row_start = 3 * grid_row_index
    grid_column_start = 3 * grid_column_index
    for grid_row in range(grid_row_start, grid_row_start + 3):
        for grid_column in range(grid_column_start, grid_column_start + 3):
            if isinstance(matrix[grid_row][grid_column], list):
                unsolved_cells += [[(grid_row, grid_column), matrix[grid_row][grid_column]]]
    for group_size in range(2, 5):
        for cell_subset in itertools.combinations(unsolved_cells, group_size):
            collective_possibilities = []
            grid_indices = []
            for selected_cell in cell_subset:
                collective_possibilities += selected_cell[1]
                grid_indices += [selected_cell[0]]
            if len(set(collective_possibilities)) == group_size:
                for non_subset_cell in unsolved_cells:
                    if not non_subset_cell[0] in grid_indices:
                        indices = non_subset_cell[0]
                        replacing_set = list(set(matrix[indices[0]][indices[1]]) - set(collective_possibilities))
                        matrix[indices[0]][indices[1]] = replacing_set


def naked_subset_all_rows(matrix):
    for row in matrix:
        naked_subset_row(row)


def naked_subset_all_columns(matrix):
    for column_index in range(9):
        naked_subset_column(column_index, matrix)


def naked_subset_all_grids(matrix):
    for grid_row_index in range(3):
        for grid_column_index in range(3):
            naked_subset_grid(grid_row_index, grid_column_index, matrix)


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
def omission_row(grid_row_index, grid_column_index, matrix):
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


def omission_column(grid_row_index, grid_column_index, matrix):
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
def omission_all_rows(matrix):
    for grid_row in range(3):
        for grid_column in range(3):
            omission_row(grid_row, grid_column, matrix)


def omission_all_columns(matrix):
    for grid_row in range(3):
        for grid_column in range(3):
            omission_column(grid_row, grid_column, matrix)


# If there is a grid row/column possibility which is not in adjacent cells then it should be secluded to that line
def reverse_omission_row(grid_row_index, grid_column_index, matrix):
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


def reverse_omission_column(grid_row_index, grid_column_index, matrix):
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


def reverse_omission_all_rows(matrix):
    for grid_row_index in range(3):
        for grid_column_index in range(3):
            reverse_omission_row(grid_row_index, grid_column_index, matrix)


def reverse_omission_all_columns(matrix):
    for grid_row_index in range(3):
        for grid_column_index in range(3):
            reverse_omission_column(grid_row_index, grid_column_index, matrix)


def hidden_subset_row(row):
    unsolved_cells = []
    for column_index, cell in enumerate(row):
        if isinstance(cell, list):
            row[column_index].sort()
            unsolved_cells += [[column_index, cell]]
    for group_size in range(2, 5):
        for cell_subset in itertools.combinations(unsolved_cells, group_size):
            collective_possibilities = []
            column_indices = []
            collective_anti_possibilities = []
            for subset_cell in cell_subset:
                collective_possibilities += subset_cell[1]
                column_indices += [subset_cell[0]]
            for non_subset_cell in unsolved_cells:
                if not non_subset_cell[0] in column_indices:
                    collective_anti_possibilities += non_subset_cell[1]
            hidden_possibilities = set(collective_possibilities) - set(collective_anti_possibilities)
            if len(hidden_possibilities) == group_size:
                anti_possibilities = set(range(1, 10)) - hidden_possibilities
                for narrowing_index in column_indices:
                    row[narrowing_index] = list(set(row[narrowing_index]) - anti_possibilities)


def hidden_subset_column(column, matrix):
    unsolved_cells = []
    for row_index, row in enumerate(matrix):
        if isinstance(row[column], list):
            unsolved_cells += [[row_index, row[column]]]
    for group_size in range(2, 5):
        for cell_subset in itertools.combinations(unsolved_cells, group_size):
            collective_possibilities = []
            row_indices = []
            collective_anti_possibilities = []
            for subset_cell in cell_subset:
                collective_possibilities += subset_cell[1]
                row_indices += [subset_cell[0]]
            for non_subset_cell in unsolved_cells:
                if not non_subset_cell[0] in row_indices:
                    collective_anti_possibilities += non_subset_cell[1]
            hidden_possibilities = set(collective_possibilities) - set(collective_anti_possibilities)
            if len(hidden_possibilities) == group_size:
                anti_possibilities = set(range(1, 10)) - hidden_possibilities
                for narrowing_index in row_indices:
                    matrix[narrowing_index][column] = list(set(matrix[narrowing_index][column]) - anti_possibilities)


def hidden_subset_grid(grid_row_index, grid_column_index, matrix):
    unsolved_cells = []
    grid_row_start = 3 * grid_row_index
    grid_column_start = 3 * grid_column_index
    for grid_row in range(grid_row_start, grid_row_start + 3):
        for grid_column in range(grid_column_start, grid_column_start + 3):
            if isinstance(matrix[grid_row][grid_column], list):
                unsolved_cells += [[(grid_row, grid_column), matrix[grid_row][grid_column]]]
    for group_size in range(2, 5):
        for cell_subset in itertools.combinations(unsolved_cells, group_size):
            collective_possibilities = []
            grid_indices = []
            collective_anti_possibilities = []
            for subset_cell in cell_subset:
                collective_possibilities += subset_cell[1]
                grid_indices += [subset_cell[0]]
            for non_subset_cell in unsolved_cells:
                if not non_subset_cell[0] in grid_indices:
                    collective_anti_possibilities += non_subset_cell[1]
            hidden_possibilities = set(collective_possibilities) - set(collective_anti_possibilities)
            if len(hidden_possibilities) == group_size:
                anti_possibilities = set(range(1, 10)) - hidden_possibilities
                for index in grid_indices:
                    matrix[index[0]][index[1]] = list(set(matrix[index[0]][index[1]]) - anti_possibilities)


def hidden_subset_all_rows(matrix):
    for row in matrix:
        hidden_subset_row(row)


def hidden_subset_all_columns(matrix):
    for column_index in range(9):
        hidden_subset_column(column_index, matrix)


def hidden_subset_all_grids(matrix):
    for grid_row_index in range(3):
        for grid_column_index in range(3):
            hidden_subset_grid(grid_row_index, grid_column_index, matrix)

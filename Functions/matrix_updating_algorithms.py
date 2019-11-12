

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


# Using the retrieve functions to find grid row/column secluded possibilities and eliminate them from the other grids
def eliminate_grid_secluded_row_possibilities(grid_row_index, grid_column_index, matrix):
    grid_row_possibilities = retrieve_grid_row_possibilities(grid_row_index, grid_column_index, matrix)
    for row_index, grid_row in enumerate(grid_row_possibilities):
        for possibility in grid_row:
            counter = 0
            for row_check in range(3):
                if possibility in grid_row_possibilities[row_check]:
                    counter += 1
            if counter == 1:
                row_index = 3 * grid_row_index + row_index
                grid_column_start = 3 * grid_column_index
                for non_grid_cells in set(range(9)) - set(range(grid_column_start, grid_column_start + 3)):
                    if isinstance(matrix[row_index][non_grid_cells], list):
                        if possibility in matrix[row_index][non_grid_cells]:
                            matrix[row_index][non_grid_cells].remove(possibility)


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
                column_index = 3 * grid_column_index + column_index
                for non_grid_cells in set(range(9)) - set(range(grid_row_start, grid_row_start + 3)):
                    if isinstance(matrix[non_grid_cells][column_index], list):
                        if possibility in matrix[non_grid_cells][column_index]:
                            matrix[non_grid_cells][column_index].remove(possibility)


# Extending the two algorithms to each grid
def eliminate_secluded_row_possibilities(matrix):
    for grid_row in range(3):
        for grid_column in range(3):
            eliminate_grid_secluded_row_possibilities(grid_row, grid_column, matrix)


def eliminate_secluded_column_possibilities(matrix):
    for grid_row in range(3):
        for grid_column in range(3):
            eliminate_grid_secluded_column_possibilities(grid_row, grid_column, matrix)

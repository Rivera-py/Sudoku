

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
    for grid_row in range(grid_row_start, grid_row_start + 3, 1):
        for grid_column in range(grid_column_start, grid_column_start + 3, 1):
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




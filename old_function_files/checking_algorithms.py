

# Checks if the matrix is solved (i.e. all strings)
def is_solved(matrix):
    non_string_counter = 0
    for row in matrix:
        for elt in row:
            if not isinstance(elt, str):
                non_string_counter += 1
    return non_string_counter == 0


# Checks to see if a sudoku has been solved correctly
def check_illegal_row(row_index, matrix):
    if set("123456789") != set(matrix[row_index]):
        print("Illegal row found")


def check_illegal_column(column_index, matrix):
    if set("123456789") != set(matrix[row_index][column_index] for row_index in range(9)):
        print("Illegal column found")


def check_illegal_cell_grid(row_index, column_index, matrix):
    grid_row_start = 3 * int(row_index / 3)
    grid_column_start = 3 * int(column_index / 3)
    grid_set = []
    for grid_row in range(grid_row_start, grid_row_start + 3):
        for grid_column in range(grid_column_start, grid_column_start + 3):
            grid_set += [matrix[grid_row][grid_column]]
    if set("123456789") != set(grid_set):
        print("Illegal grid found")


def check_correct_solution(matrix):
    for row_index in range(9):
        for column_index in range(9):
            check_illegal_row(row_index, matrix)
            check_illegal_column(column_index, matrix)
            check_illegal_cell_grid(row_index, column_index, matrix)


from Functions import matrix_updating_algorithms, test_sudokus, display_algorithms, checking_algorithms
import copy


# Employs the two simplest sudoku solving methods until it cannot solve any further
def basic_sudoku_solve(matrix):
    copy_matrix = []
    matrix_updating_algorithms.initial_possibilities(matrix)
    matrix_updating_algorithms.scan_and_solve(matrix)
    while copy_matrix != matrix:
        copy_matrix = copy.deepcopy(matrix)
        matrix_updating_algorithms.one_possibility(matrix)
        matrix_updating_algorithms.scan_and_solve(matrix)


# Adds the unique possibility method
def simple_sudoku_solve(matrix):
    run = True
    while run:
        basic_sudoku_solve(matrix)
        if matrix_updating_algorithms.unique_row_possibility(matrix):
            continue
        if matrix_updating_algorithms.unique_column_possibility(matrix):
            continue
        if matrix_updating_algorithms.unique_grid_possibility(matrix):
            continue
        run = False


def intermediate_sudoku_solve(matrix):
    simple_sudoku_solve(matrix)
    copy_matrix = []
    while copy_matrix != matrix:
        copy_matrix = copy.deepcopy(matrix)
        matrix_updating_algorithms.eliminate_all_grid_secluded_row_possibilities(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.eliminate_all_grid_secluded_column_possibilities(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.all_locked_row_possibilities(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.all_locked_col_possibilities(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.all_locked_grid_possibilitites(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.reverse_all_grid_seclude_row_possibilities(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.reverse_all_grid_seclude_column_possibilities(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.all_hidden_row_subset(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.all_hidden_column_subset(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.all_hidden_grid_subset(matrix)
        simple_sudoku_solve(matrix)
from Functions import matrix_updating_algorithms, test_sudokus, display_algorithms, checking_algorithms
import copy


# Employs the two simplest sudoku solving methods until it cannot solve any further
def basic_sudoku_solve(matrix):
    copy_matrix = []
    matrix_updating_algorithms.initial_possibilities(matrix)
    matrix_updating_algorithms.scan_and_solve(matrix)
    while copy_matrix != matrix:
        copy_matrix = copy.deepcopy(matrix)
        matrix_updating_algorithms.lone_singles(matrix)
        matrix_updating_algorithms.scan_and_solve(matrix)


# Adds the unique possibility method
def simple_sudoku_solve(matrix):
    run = True
    while run:
        basic_sudoku_solve(matrix)
        if matrix_updating_algorithms.hidden_singles_rows(matrix):
            continue
        if matrix_updating_algorithms.hidden_singles_columns(matrix):
            continue
        if matrix_updating_algorithms.hidden_singles_grids(matrix):
            continue
        run = False


def intermediate_sudoku_solve(matrix):
    simple_sudoku_solve(matrix)
    copy_matrix = []
    while copy_matrix != matrix:
        copy_matrix = copy.deepcopy(matrix)
        matrix_updating_algorithms.naked_subset_all_rows(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.naked_subset_all_columns(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.naked_subset_all_grids(matrix)
        matrix_updating_algorithms.omission_all_rows(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.omission_all_columns(matrix)
        simple_sudoku_solve(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.reverse_omission_all_rows(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.reverse_omission_all_columns(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.hidden_subset_all_rows(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.hidden_subset_all_columns(matrix)
        simple_sudoku_solve(matrix)
        matrix_updating_algorithms.hidden_subset_all_grids(matrix)
        simple_sudoku_solve(matrix)

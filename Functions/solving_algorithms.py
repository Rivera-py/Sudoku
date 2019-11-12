from Functions import matrix_updating_algorithms, test_sudokus, display_algorithms
import copy


# Employs the two simplest sudoku solving methods until it cannot solve any further
def simple_sudoku_solve(matrix):
    copy_matrix = []
    matrix_updating_algorithms.initial_possibilities(matrix)
    matrix_updating_algorithms.scan_and_solve(matrix)
    while copy_matrix != matrix:
        copy_matrix = copy.deepcopy(matrix)
        matrix_updating_algorithms.one_possibility(matrix)
        matrix_updating_algorithms.scan_and_solve(matrix)
import itertools


# Takes initial information and replaces unknown values with possible values
def initial_possibilities(matrix):
    for row in matrix:
        for element in range(0, 9, 1):
            if row[element] == "?":
                row[element] = list(range(1, 10, 1))


# Removing possibilities based on solved cells
def update_row(r_i, c_j, matrix):
    num = matrix[r_i][c_j]
    for element in range(0, 9, 1):
        if isinstance(matrix[r_i][element], list):
            if num in matrix[r_i][element]:
                matrix[r_i][element].remove(num)


def update_col(r_i, c_j, matrix):
    num = matrix[r_i][c_j]
    for row in range(0, 9, 1):
        if isinstance(matrix[row][c_j], list):
            if num in matrix[row][c_j]:
                matrix[row][c_j].remove(num)


def update_grid(r_i, c_i, matrix):
    num = matrix[r_i][c_i]
    grid_row = 3 * int(r_i / 3)
    grid_col = 3 * int(c_i / 3)
    for row in range(grid_row, grid_row + 3, 1):
        for col in range(grid_col, grid_col + 3, 1):
            if isinstance(matrix[row][col], list):
                if num in matrix[row][col]:
                    matrix[row][col].remove(num)


# When a cell has been solved and its information updated, it will become a string.
def lock(r_i, c_j, matrix):
    matrix[r_i][c_j] = str(matrix[r_i][c_j])


def master_update(r_i, c_j, matrix):
    update_col(r_i, c_j, matrix)
    update_row(r_i, c_j, matrix)
    update_grid(r_i, c_j, matrix)
    lock(r_i, c_j, matrix)


# Checks if every cell is ready to be solved.
def scan_and_update(matrix):
    for row in range(0, 9, 1):
        for col in range(0, 9, 1):
            if isinstance(matrix[row][col], int):
                master_update(row, col, matrix)


# If a cell has only one possibility, it must be that number.
def scan_solve_cell(matrix):
    for row in range(0, 9, 1):
        for col in range(0, 9, 1):
            if isinstance(matrix[row][col], list):
                if len(matrix[row][col]) == 1:
                    matrix[row][col] = matrix[row][col][0]


def scan(matrix):
    scan_and_update(matrix)
    scan_solve_cell(matrix)


# Used for while loops to continually scan
def fin_scan(matrix):
    for row in range(0, 9, 1):
        for col in range(0, 9, 1):
            if not (isinstance(matrix[row][col], str) or isinstance(matrix[row][col], list)):
                return True
    return False


# Checks if a cell is the only possible candidate for a number in a row
def scan_special_cell_row(matrix):
    for row in range(0, 9, 1):
        for col in range(0, 9, 1):
            if isinstance(matrix[row][col], list):
                for number in matrix[row][col]:
                    check = 0
                    for column in range(0, 9, 1):
                        if isinstance(matrix[row][column], list):
                            if number in matrix[row][column]:
                                if column != col:
                                    check = check + 1
                    if check == 0:
                        matrix[row][col] = number


def scan_special_cell_col(matrix):
    for row in range(0, 9, 1):
        for col in range(0, 9, 1):
            if isinstance(matrix[row][col], list):
                for number in matrix[row][col]:
                    check = 0
                    for rows in range(0, 9, 1):
                        if isinstance(matrix[rows][col], list):
                            if number in matrix[rows][col]:
                                if rows != row:
                                    check = check + 1
                    if check == 0:
                        matrix[row][col] = number


def scan_special_cell_grid(matrix):
    for row in range(0, 9, 1):
        for col in range(0, 9, 1):
            if isinstance(matrix[row][col], list):
                for number in matrix[row][col]:
                    test = 0
                    for grid_row in range(3 * int(row / 3), 3 * int(row / 3) + 3, 1):
                        for grid_col in range(3 * int(col / 3), 3 * int(col / 3) + 3, 1):
                            if isinstance(matrix[grid_row][grid_col], list):
                                if (grid_row, grid_col) != (row, col):
                                    if number in matrix[grid_row][grid_col]:
                                        test = test + 1
                    if test == 0:
                        matrix[row][col] = number


# Suitable for a beginner sudoku
def solve(matrix):
    initial_possibilities(matrix)
    i = 0
    while i < 13:
        i += 1
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_row(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_col(matrix)
        while fin_scan(sudoku):
            scan(matrix)
        scan_special_cell_grid(sudoku)
    return matrix


# Used to display sudoku in console
def display_current(matrix):
    for row in range(0, 9, 1):
        print(matrix[row])
    print(" ")


# Retrieves the row possibilities of a specific grid
def retrieve_row_possibilities(row, grid_c, matrix):
    possibilities = []
    for elt in range(3 * grid_c, 3 + 3 * grid_c, 1):
        if isinstance(matrix[row][elt], list):
            possibilities = possibilities + matrix[row][elt]
    return list(set(possibilities))


def retrieve_col_possibilities(grid_r, col, matrix):
    possibilities = []
    for elt in range(3 * grid_r, 3 + 3 * grid_r, 1):
        if isinstance(matrix[elt][col], list):
            possibilities = possibilities + matrix[elt][col]
    return list(set(possibilities))


# Updates grid row possibility variables
def update_grid_row_possibilities(matrix):
    for grid_row in range(0, 3, 1):
        G_00[0][grid_row] = retrieve_row_possibilities(grid_row, 0, matrix)
        G_01[0][grid_row] = retrieve_row_possibilities(grid_row, 1, matrix)
        G_02[0][grid_row] = retrieve_row_possibilities(grid_row, 2, matrix)
        G_10[0][grid_row] = retrieve_row_possibilities(3 + grid_row, 0, matrix)
        G_11[0][grid_row] = retrieve_row_possibilities(3 + grid_row, 1, matrix)
        G_12[0][grid_row] = retrieve_row_possibilities(3 + grid_row, 2, matrix)
        G_20[0][grid_row] = retrieve_row_possibilities(6 + grid_row, 0, matrix)
        G_21[0][grid_row] = retrieve_row_possibilities(6 + grid_row, 1, matrix)
        G_22[0][grid_row] = retrieve_row_possibilities(6 + grid_row, 2, matrix)


def update_grid_col_possibilities(matrix):
    for grid_col in range(0, 3, 1):
        G_00[1][grid_col] = retrieve_col_possibilities(0, grid_col, matrix)
        G_10[1][grid_col] = retrieve_col_possibilities(1, grid_col, matrix)
        G_20[1][grid_col] = retrieve_col_possibilities(2, grid_col, matrix)
        G_01[1][grid_col] = retrieve_col_possibilities(0, 3 + grid_col, matrix)
        G_11[1][grid_col] = retrieve_col_possibilities(1, 3 + grid_col, matrix)
        G_21[1][grid_col] = retrieve_col_possibilities(2, 3 + grid_col, matrix)
        G_02[1][grid_col] = retrieve_col_possibilities(0, 6 + grid_col, matrix)
        G_12[1][grid_col] = retrieve_col_possibilities(1, 6 + grid_col, matrix)
        G_22[1][grid_col] = retrieve_col_possibilities(2, 6 + grid_col, matrix)


def update_grid_possibilities(matrix):
    update_grid_row_possibilities(matrix)
    update_grid_col_possibilities(matrix)


# If a grid has a possibility secluded to a row, eliminates possibilities for the row outside the grid
def eliminate_row_possibilities(matrix):
    for row_index in range(0, 3, 1):
        for col_index in range(0, 3, 1):
            for number in range(1, 10, 1):
                if number in grid_info[row_index][col_index][0][0]:
                    if not (number in grid_info[row_index][col_index][0][1] or number in
                            grid_info[row_index][col_index][0][2]):
                        for elt in set(range(0, 9, 1)).difference(set(range(col_index * 3, 3 + col_index * 3, 1))):
                            if isinstance(matrix[row_index * 3][elt], list):
                                if number in matrix[row_index * 3][elt]:
                                    matrix[row_index * 3][elt].remove(number)
                if number in grid_info[row_index][col_index][0][1]:
                    if not (number in grid_info[row_index][col_index][0][0] or number in
                            grid_info[row_index][col_index][0][2]):
                        for elt in set(range(0, 9, 1)).difference(set(range(col_index * 3, 3 + col_index * 3, 1))):
                            if isinstance(matrix[1 + row_index * 3][elt], list):
                                if number in matrix[1 + row_index * 3][elt]:
                                    matrix[1 + row_index * 3][elt].remove(number)
                if number in grid_info[row_index][col_index][0][2]:
                    if not (number in grid_info[row_index][col_index][0][0] or number in
                            grid_info[row_index][col_index][0][1]):
                        for elt in set(range(0, 9, 1)).difference(set(range(col_index * 3, 3 + col_index * 3, 1))):
                            if isinstance(matrix[2 + row_index * 3][elt], list):
                                if number in matrix[2 + row_index * 3][elt]:
                                    matrix[2 + row_index * 3][elt].remove(number)


def eliminate_col_possibilities(matrix):
    for row_index in range(0, 3, 1):
        for col_index in range(0, 3, 1):
            for number in range(1, 10, 1):
                if number in grid_info[row_index][col_index][1][0]:
                    if not (number in grid_info[row_index][col_index][1][1] or number in
                            grid_info[row_index][col_index][1][2]):
                        for elt in set(range(0, 9, 1)).difference(set(range(row_index * 3, 3 + row_index * 3, 1))):
                            if isinstance(matrix[elt][col_index * 3], list):
                                if number in matrix[elt][col_index * 3]:
                                    matrix[elt][col_index * 3].remove(number)
                if number in grid_info[row_index][col_index][1][1]:
                    if not (number in grid_info[row_index][col_index][1][0] or number in
                            grid_info[row_index][col_index][1][2]):
                        for elt in set(range(0, 9, 1)).difference(set(range(row_index * 3, 3 + row_index * 3, 1))):
                            if isinstance(matrix[elt][1 + col_index * 3], list):
                                if number in matrix[elt][1 + col_index * 3]:
                                    matrix[elt][1 + col_index * 3].remove(number)
                if number in grid_info[row_index][col_index][1][2]:
                    if not (number in grid_info[row_index][col_index][1][0] or number in
                            grid_info[row_index][col_index][1][1]):
                        for elt in set(range(0, 9, 1)).difference(set(range(row_index * 3, 3 + row_index * 3, 1))):
                            if isinstance(matrix[elt][2 + col_index * 3], list):
                                if number in matrix[elt][2 + col_index * 3]:
                                    matrix[elt][2 + col_index * 3].remove(number)


# Checks for secluded possibilities and removes them from other cells in the row
def secluded_row_possibilities(row, matrix):
    poss_list = []
    for element in range(0, 9, 1):
        if isinstance(matrix[row][element], list):
            poss_list = poss_list + [[matrix[row][element], row, element]]
    for poss_size in range(2, 7, 1):
        poss_size_list = []
        for poss in poss_list:
            poss[0].sort()
            if len(poss[0]) == poss_size:
                poss_size_list = poss_size_list + [poss]
        for poss_of_size in poss_size_list:
            counter = 0
            col_indices = []
            for possib in poss_size_list:
                if poss_of_size[0] == possib[0]:
                    counter = counter + 1
                    col_indices = col_indices + [possib[2]]
            if counter == poss_size:
                for column in set(range(0, 9, 1)).difference(set(col_indices)):
                    if isinstance(matrix[row][column], list):
                        matrix[row][column] = list(set(matrix[row][column]).difference(matrix[row][col_indices[0]]))


def secluded_col_possibilities(col, matrix):
    poss_list = []
    for element in range(0, 9, 1):
        if isinstance(matrix[element][col], list):
            poss_list = poss_list + [[matrix[element][col], element, col]]
    for poss_size in range(2, 7, 1):
        poss_size_list = []
        for poss in poss_list:
            poss[0].sort()
            if len(poss[0]) == poss_size:
                poss_size_list = poss_size_list + [poss]
        for poss_of_size in poss_size_list:
            counter = 0
            row_indices = []
            for possib in poss_size_list:
                if poss_of_size[0] == possib[0]:
                    counter = counter + 1
                    row_indices = row_indices + [possib[1]]
            if counter == poss_size:
                for row in set(range(0, 9, 1)).difference(set(row_indices)):
                    if isinstance(matrix[row][col], list):
                        matrix[row][col] = list(set(matrix[row][col]).difference(matrix[row_indices[0]][col]))


def secluded_grid_possibilities(row_index, col_index, matrix):
    poss_list = []
    for grid_row in range(row_index * 3, 3 + 3 * row_index, 1):
        for grid_col in range(col_index * 3, 3 + 3 * col_index, 1):
            if isinstance(matrix[grid_row][grid_col], list):
                poss_list = poss_list + [[matrix[grid_row][grid_col], grid_row, grid_col]]
    for poss_size in range(2, 7, 1):
        poss_size_list = []
        for poss in poss_list:
            poss[0].sort()
            if len(poss[0]) == poss_size:
                poss_size_list = poss_size_list + [poss]
        for poss_of_size in poss_size_list:
            counter = 0
            cell_indices = []
            for possib in poss_size_list:
                if poss_of_size[0] == possib[0]:
                    counter = counter + 1
                    cell_indices = cell_indices + [[possib[1], possib[2]]]
            if counter == poss_size:
                for grid_r in range(row_index * 3, 3 + 3 * row_index, 1):
                    for grid_c in range(col_index * 3, 3 + col_index, 1):
                        if not ([grid_r, grid_c] in cell_indices):
                            if isinstance(matrix[grid_r][grid_c], list):
                                matrix[grid_r][grid_c] = list(set(matrix[grid_r][grid_c]).difference(
                                    set(matrix[cell_indices[0][0]][cell_indices[0][1]])))


# Suitable for intermediate sudokus
def modded_solve(matrix):
    initial_possibilities(matrix)
    i = 0
    while i < 15:
        i = i + 1
        scan(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_row(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_col(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_grid(matrix)
        while fin_scan(matrix):
            scan(matrix)
        update_grid_possibilities(matrix)
        eliminate_row_possibilities(matrix)
        while fin_scan(matrix):
            scan(matrix)
        update_grid_possibilities(matrix)
        eliminate_col_possibilities(matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row in range(0, 9, 1):
            secluded_row_possibilities(row, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for col in range(0, 9, 1):
            secluded_col_possibilities(col, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 3, 1):
            for col_i in range(0, 3, 1):
                secluded_grid_possibilities(row_i, col_i, matrix)
    return matrix


# Checks for n possibilities relegated to n intersecting cells
def rule_of_n_row(row, matrix):
    row_possibilities = []
    for elt in range(0, 9, 1):
        if isinstance(matrix[row][elt], list):
            row_possibilities = row_possibilities + [[matrix[row][elt], row, elt]]
    for number in range(2, 6, 1):
        for n_tuple in itertools.combinations(row_possibilities, number):
            possibilities = []
            indices = []
            for sum_poss in n_tuple:
                possibilities = possibilities + sum_poss[0]
                indices = indices + [sum_poss[2]]
            if len(set(possibilities)) == number:
                for element in set(range(0, 9, 1)).difference(set(indices)):
                    if isinstance(matrix[row][element], list):
                        matrix[row][element] = list(set(matrix[row][element]).difference(set(possibilities)))


def rule_of_n_col(col, matrix):
    row_possibilities = []
    for elt in range(0, 9, 1):
        if isinstance(matrix[elt][col], list):
            row_possibilities = row_possibilities + [[matrix[elt][col], elt, col]]
    for number in range(2, 6, 1):
        for n_tuple in itertools.combinations(row_possibilities, number):
            possibilities = []
            indices = []
            for sum_poss in n_tuple:
                possibilities = possibilities + sum_poss[0]
                indices = indices + [sum_poss[1]]
            if len(set(possibilities)) == number:
                for element in set(range(0, 9, 1)).difference(set(indices)):
                    if isinstance(matrix[element][col], list):
                        matrix[element][col] = list(set(matrix[element][col]).difference(set(possibilities)))


def rule_of_n_grid(row_index, col_index, matrix):
    grid_possibilities = []
    for row_elt in range(row_index * 3, 3 + 3 * row_index, 1):
        for col_elt in range(col_index * 3, 3 + 3 * col_index):
            if isinstance(matrix[row_elt][col_elt], list):
                grid_possibilities = grid_possibilities + [[matrix[row_elt][col_elt], row_elt, col_elt]]
    for number in range(2, 6, 1):
        for n_tuple in itertools.combinations(grid_possibilities, number):
            possibilities = []
            indices = []
            for sum_poss in n_tuple:
                possibilities = possibilities + sum_poss[0]
                indices = indices + [[sum_poss[1], sum_poss[2]]]
            if len(set(possibilities)) == number:
                for row_element in range(3 * row_index, 3 + 3 * row_index, 1):
                    for col_element in range(3 * col_index, 3 + 3 * col_index, 1):
                        if not ([row_element, col_element] in indices):
                            if isinstance(matrix[row_element][col_element], list):
                                matrix[row_element][col_element] = list(
                                    set(matrix[row_element][col_element]).difference(set(possibilities)))


# Suitable for (some) hard sudokus
def modded_solve2(matrix):
    initial_possibilities(matrix)
    i = 0
    while i < 15:
        i = i + 1
        scan(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_row(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_col(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_grid(matrix)
        while fin_scan(matrix):
            scan(matrix)
        update_grid_possibilities(matrix)
        eliminate_row_possibilities(matrix)
        while fin_scan(matrix):
            scan(matrix)
        update_grid_possibilities(matrix)
        eliminate_col_possibilities(matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row in range(0, 9, 1):
            secluded_row_possibilities(row, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for col in range(0, 9, 1):
            secluded_col_possibilities(col, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 3, 1):
            for col_i in range(0, 3, 1):
                secluded_grid_possibilities(row_i, col_i, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row in range(0, 9, 1):
            rule_of_n_row(row, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for col in range(0, 9, 1):
            rule_of_n_col(col, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 3, 1):
            for col_i in range(0, 3, 1):
                rule_of_n_grid(row_i, col_i, matrix)
        while fin_scan(matrix):
            scan(matrix)
    return matrix


# Checks if possibilities SHOULD be relegated to one row of a grid
def reverse_row_possibilities(row_index, col_index, matrix):
    for row in range(0, 3, 1):
        for possibility in grid_info[row_index][col_index][0][row]:
            counter = 0
            for element in set(range(0, 9, 1)).difference(set(range(3 * col_index, 3 + 3 * col_index, 1))):
                if isinstance(matrix[3 * row_index + row][element], list):
                    if possibility in matrix[3 * row_index + row][element]:
                        counter += 1
            if counter == 0:
                for rows in set(range(3 * row_index, 3 + 3 * row_index)).difference({row_index * 3 + row}):
                    for cols in range(col_index * 3, 3 + 3 * col_index, 1):
                        if isinstance(matrix[rows][cols], list):
                            if possibility in matrix[rows][cols]:
                                matrix[rows][cols].remove(possibility)


def reverse_col_possibilities(row_index, col_index, matrix):
    for col in range(0, 3, 1):
        for possibility in grid_info[row_index][col_index][1][col]:
            counter = 0
            for element in set(range(0, 9, 1)).difference(set(range(3 * row_index, 3 + 3 * row_index, 1))):
                if isinstance(matrix[element][3 * col_index + col], list):
                    if possibility in matrix[element][3 * col_index + col]:
                        counter += 1
            if counter == 0:
                for cols in set(range(3 * col_index, 3 + 3 * col_index)).difference({col_index * 3 + col}):
                    for rows in range(row_index * 3, 3 + 3 * row_index, 1):
                        if isinstance(matrix[rows][cols], list):
                            if possibility in matrix[rows][cols]:
                                matrix[rows][cols].remove(possibility)


# Checks if there is extra information on a secluded set of possibilities
def secluded_row_possibilities2(row, matrix):
    poss_list = []
    for element in range(0, 9, 1):
        if isinstance(matrix[row][element], list):
            poss_list = poss_list + [[matrix[row][element], row, element]]
    for poss_size in range(2, 7, 1):
        poss_size_list = []
        for poss in poss_list:
            poss[0].sort()
            if len(poss[0]) == poss_size:
                poss_size_list = poss_size_list + [poss]
        for poss_of_size in poss_size_list:
            for comb in itertools.combinations(poss_of_size[0], poss_size):
                counter = 0
                col_indices = []
                for possib in poss_size_list:
                    if comb in itertools.combinations(possib[0], poss_size):
                        counter += 1
                        col_indices = col_indices + [poss_of_size[2]]
                if counter == poss_size:
                    for column in col_indices:
                        matrix[row][column] = list(comb)


def secluded_col_possibilities2(col, matrix):
    poss_list = []
    for element in range(0, 9, 1):
        if isinstance(matrix[element][col], list):
            poss_list = poss_list + [[matrix[element][col], element, col]]
    for poss_size in range(2, 7, 1):
        poss_size_list = []
        for poss in poss_list:
            poss[0].sort()
            if len(poss[0]) == poss_size:
                poss_size_list = poss_size_list + [poss]
        for poss_of_size in poss_size_list:
            for comb in itertools.combinations(poss_of_size[0], poss_size):
                counter = 0
                row_indices = []
                for possib in poss_size_list:
                    if comb in itertools.combinations(possib[0], poss_size):
                        counter += 1
                        row_indices = row_indices + [poss_of_size[1]]
                if counter == poss_size:
                    for row in row_indices:
                        matrix[row][col] = list(comb)


def secluded_grid_possibilities2(row_index, col_index, matrix):
    poss_list = []
    for row_elt in range(3 * row_index, 3 + 3 * row_index, 1):
        for col_elt in range(3 * col_index, 3 + 3 * col_index, 1):
            if isinstance(matrix[row_elt][col_elt], list):
                poss_list = poss_list + [[matrix[row_elt][col_elt], row_elt, col_elt]]
    for poss_size in range(2, 7, 1):
        poss_size_list = []
        for poss in poss_list:
            poss[0].sort()
            if len(poss[0]) == poss_size:
                poss_size_list = poss_size_list + [poss]
        for poss_of_size in poss_size_list:
            for comb in itertools.combinations(poss_of_size[0], poss_size):
                counter = 0
                indices = []
                for possib in poss_size_list:
                    if comb in itertools.combinations(possib[0], poss_size):
                        counter += 1
                        indices = indices + [(possib[0], possib[1])]
                if counter == poss_size:
                    for row_element in range(3 * row_index, 3 + 3 * row_index, 1):
                        for col_element in range(3 * col_index, 3 + 3 * col_index, 1):
                            if [row_element, col_element] in indices:
                                matrix[row_element][col_element] = list(comb)


def extract_neighbours_size_2(cell_row, cell_col, matrix):
    neighbours = []
    for element in range(0, 9, 1):
        if element != cell_col:
            if isinstance(matrix[cell_row][element], list):
                if len(matrix[cell_row][element]) == 2:
                    neighbours = neighbours + [[matrix[cell_row][element], cell_row, element]]
    for elt in range(0, 9, 1):
        if elt != cell_row:
            if isinstance(matrix[elt][cell_col], list):
                if len(matrix[elt][cell_col]) == 2:
                    neighbours = neighbours + [[matrix[elt][cell_col], elt, cell_col]]
    for grid_row in range(3 * int(cell_row / 3), 3 + 3 * int(cell_row / 3), 1):
        for grid_col in range(3 * int(cell_col / 3), 3 + 3 * int(cell_col / 3), 1):
            if grid_row != cell_row:
                if grid_col != cell_col:
                    if isinstance(matrix[grid_row][grid_col], list):
                        if len(matrix[grid_row][grid_col]) == 2:
                            neighbours = neighbours + [[matrix[grid_row][grid_col], grid_row, grid_col]]
    return neighbours


def extract_neighbours_any_size(cell_row, cell_col, matrix):
    neighbours = []
    for element in range(0, 9, 1):
        if element != cell_col:
            if isinstance(matrix[cell_row][element], list):
                neighbours = neighbours + [[matrix[cell_row][element], cell_row, element]]
    for elt in range(0, 9, 1):
        if elt != cell_row:
            if isinstance(matrix[elt][cell_col], list):
                neighbours = neighbours + [[matrix[elt][cell_col], elt, cell_col]]
    for grid_row in range(3 * int(cell_row / 3), 3 + 3 * int(cell_row / 3), 1):
        for grid_col in range(3 * int(cell_col / 3), 3 + 3 * int(cell_col / 3), 1):
            if grid_row != cell_row:
                if grid_col != cell_col:
                    if isinstance(matrix[grid_row][grid_col], list):
                        neighbours = neighbours + [[matrix[grid_row][grid_col], grid_row, grid_col]]
    return neighbours


# XY method
def xy_method1(row, col, matrix):
    if isinstance(matrix[row][col], list):
        if len(matrix[row][col]) == 2:
            possible_body = []
            for intersects in extract_neighbours_size_2(row, col, matrix):
                if matrix[row][col][0] in intersects[0]:
                    if not (matrix[row][col][1] in intersects[0]):
                        possible_body = possible_body + [intersects]
            for cell in possible_body:
                cell_wings = []
                for inters in extract_neighbours_size_2(cell[1], cell[2], matrix):
                    if list(set(cell[0]).difference(matrix[row][col]))[0] in inters[0]:
                        if matrix[row][col][1] in inters[0]:
                            cell_wings = cell_wings + [inters]
                for wings in cell_wings:
                    # print(wings, (row, col), (cell[1],cell[2]))
                    for all_neighbour in extract_neighbours_any_size(row, col, matrix):
                        if all_neighbour in extract_neighbours_any_size(wings[1], wings[2], matrix):
                            if matrix[row][col][1] in all_neighbour[0]:
                                matrix[all_neighbour[1]][all_neighbour[2]].remove(matrix[row][col][1])
                            #  print("Removing", matrix[row][col][1], "from", all_neighbour[1], all_neighbour[2])


def xy_method2(row, col, matrix):
    if isinstance(matrix[row][col], list):
        if len(matrix[row][col]) == 2:
            possible_body = []
            for intersects in extract_neighbours_size_2(row, col, matrix):
                if matrix[row][col][1] in intersects[0]:
                    if not (matrix[row][col][0] in intersects[0]):
                        possible_body = possible_body + [intersects]
            for cell in possible_body:
                cell_wings = []
                for inters in extract_neighbours_size_2(cell[1], cell[2], matrix):
                    if list(set(cell[0]).difference(matrix[row][col]))[0] in inters[0]:
                        if [inters[1], inters[2]] != [row, col]:
                            if matrix[row][col][0] in inters[0]:
                                cell_wings = cell_wings + [inters]
                for wings in cell_wings:
                    for all_neighbour in extract_neighbours_any_size(row, col, matrix):
                        if all_neighbour in extract_neighbours_any_size(wings[1], wings[2], matrix):
                            if matrix[row][col][0] in all_neighbour[0]:
                                matrix[all_neighbour[1]][all_neighbour[2]].remove(matrix[row][col][0])


# Suitable for hard and (some) expert sudokus
def modded_solve3(matrix):
    initial_possibilities(matrix)
    i = 0
    while i < 15:
        i = i + 1
        scan(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_row(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_col(matrix)
        while fin_scan(matrix):
            scan(matrix)
        scan_special_cell_grid(matrix)
        while fin_scan(matrix):
            scan(matrix)
        update_grid_possibilities(matrix)
        eliminate_row_possibilities(matrix)
        while fin_scan(matrix):
            scan(matrix)
        update_grid_possibilities(matrix)
        eliminate_col_possibilities(matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row in range(0, 9, 1):
            secluded_row_possibilities(row, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for col in range(0, 9, 1):
            secluded_col_possibilities(col, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 3, 1):
            for col_i in range(0, 3, 1):
                secluded_grid_possibilities(row_i, col_i, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row in range(0, 9, 1):
            rule_of_n_row(row, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for col in range(0, 9, 1):
            rule_of_n_col(col, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 3, 1):
            for col_i in range(0, 3, 1):
                rule_of_n_grid(row_i, col_i, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row in range(0, 9, 1):
            secluded_row_possibilities2(row, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for col in range(0, 9, 1):
            secluded_col_possibilities2(col, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 3, 1):
            for col_i in range(0, 3, 1):
                secluded_grid_possibilities2(row_i, col_i, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 9, 1):
            for col_i in range(0, 9, 1):
                xy_method1(row_i, col_i, sudoku)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 9, 1):
            for col_i in range(0, 9, 1):
                xy_method2(row_i, col_i, sudoku)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 3, 1):
            for col_i in range(0, 3, 1):
                reverse_row_possibilities(row_i, col_i, matrix)
        while fin_scan(matrix):
            scan(matrix)
        for row_i in range(0, 3, 1):
            for col_i in range(0, 3, 1):
                reverse_col_possibilities(row_i, col_i, matrix)
        while fin_scan(matrix):
            scan(matrix)
    return matrix


# Below are high level methods that take a few seconds to compute, use if unsolved
def expanded_x_wing_rows(matrix):
    for size in range(2, 5, 1):
        for row_comb in itertools.combinations(list(range(0, 9, 1)), size):
            for col_comb in itertools.combinations(list(range(0, 9, 1)), size):
                for number in range(1, 10, 1):
                    anti_counter = 0
                    for row in row_comb:
                        for anti_col in set(range(0, 9, 1)).difference(set(col_comb)):
                            if isinstance(matrix[row][anti_col], list):
                                if number in matrix[row][anti_col]:
                                    anti_counter += 1
                    if anti_counter == 0:
                        counter = 0
                        for rows in row_comb:
                            for cols in col_comb:
                                if isinstance(matrix[rows][cols], list):
                                    if number in matrix[rows][cols]:
                                        counter += 1
                        if counter == (size ** 2):
                            for anti_rows in set(range(0, 9, 1)).difference(set(row_comb)):
                                for col in col_comb:
                                    if isinstance(matrix[anti_rows][col], list):
                                        if number in matrix[anti_rows][col]:
                                            matrix[anti_rows][col].remove(number)


def expanded_x_wing_cols(matrix):
    for size in range(2, 5, 1):
        for row_comb in itertools.combinations(list(range(0, 9, 1)), size):
            for col_comb in itertools.combinations(list(range(0, 9, 1)), size):
                for number in range(1, 10, 1):
                    anti_counter = 0
                    for col in col_comb:
                        for anti_row in set(range(0, 9, 1)).difference(set(row_comb)):
                            if isinstance(matrix[anti_row][col], list):
                                if number in matrix[anti_row][col]:
                                    anti_counter += 1
                    if anti_counter == 0:
                        counter = 0
                        for rows in row_comb:
                            for cols in col_comb:
                                if isinstance(matrix[rows][cols], list):
                                    if number in matrix[rows][cols]:
                                        counter += 1
                        if counter == (size ** 2):
                            for anti_cols in set(range(0, 9, 1)).difference(set(col_comb)):
                                for row in row_comb:
                                    if isinstance(matrix[row][anti_cols], list):
                                        if number in matrix[row][anti_cols]:
                                            matrix[row][anti_cols].remove(number)


# Untested high level method
def swordfish_pattern(rows, cols, n, matrix):
    counters = [[], []]
    for count in range(0, 9, 1):
        counters[0] = counters[0] + [0]
        counters[1] = counters[1] + [0]
    for row in rows:
        for col in cols:
            if isinstance(matrix[row][col], list):
                if n in matrix[row][col]:
                    counters[0][row] = counters[0][row] + 1
                    counters[1][col] = counters[1][col] + 1
    for check_row in rows:
        if counters[0][check_row] != 2:
            return False
    for check_col in cols:
        if counters[1][check_col] != 2:
            return False
    return True


def swordfish_rows(matrix):
    for size in range(2, 5, 1):
        for row_comb in itertools.combinations(list(range(0, 9, 1)), size):
            for col_comb in itertools.combinations(list(range(0, 9, 1)), size):
                for number in range(1, 10, 1):
                    anti_counter = 0
                    for row in row_comb:
                        for anti_col in set(range(0, 9, 1)).difference(set(col_comb)):
                            if isinstance(matrix[row][anti_col], list):
                                if number in matrix[row][anti_col]:
                                    anti_counter += 1
                    if anti_counter == 0:
                        if swordfish_pattern(row_comb, col_comb, number, matrix):
                            for anti_rows in set(range(0, 9, 1)).difference(set(row_comb)):
                                for col in col_comb:
                                    if isinstance(matrix[anti_rows][col], list):
                                        if number in matrix[anti_rows][col]:
                                            matrix[anti_rows][col].remove(number)


def swordfish_cols(matrix):
    for size in range(2, 5, 1):
        for row_comb in itertools.combinations(list(range(0, 9, 1)), size):
            for col_comb in itertools.combinations(list(range(0, 9, 1)), size):
                for number in range(1, 10, 1):
                    anti_counter = 0
                    for col in col_comb:
                        for anti_row in set(range(0, 9, 1)).difference(set(row_comb)):
                            if isinstance(matrix[anti_row][col], list):
                                if number in matrix[anti_row][col]:
                                    anti_counter += 1
                    if anti_counter == 0:
                        if swordfish_pattern(row_comb, col_comb, number, matrix):
                            for anti_cols in set(range(0, 9, 1)).difference(set(col_comb)):
                                for row in row_comb:
                                    if isinstance(matrix[row][anti_cols], list):
                                        if number in matrix[row][anti_cols]:
                                            matrix[row][anti_cols].remove(number)
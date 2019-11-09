

# Colours for console
possibility_colour = '\033[96m'
solved_colour = '\033[1;30m'
end_colour = '\033[0m'
shade_grid_separators = '\033[40m'
grid_separator = shade_grid_separators + " " + end_colour
cell_separator = "------- ------- -------"


# Intended to display sudokus which the algorithm cannot solve; ideally this will not be needed when the project is
# completed.
def unsolved_display(matrix):
    for row_index, row in enumerate(matrix):
        if row_index in [3, 6]:
            print(shade_grid_separators + (" " * 71) + end_colour)
        elif row_index != 0:
            print(cell_separator + grid_separator + cell_separator + grid_separator + cell_separator)
        display_rows = ["","",""]
        for col_index, elt in enumerate(row):
            if isinstance(elt, str):
                display_rows[0] += "       "
                display_rows[1] += "   " + solved_colour + elt + end_colour + "   "
                display_rows[2] += "       "
            elif isinstance(elt, list):
                for possibility_row in range(3):
                    display_rows[possibility_row] += " "
                    for possibility in range(1, 4, 1):
                        if possibility == 3:
                            display_rows[possibility_row] += " "
                        if possibility + 3 * possibility_row in elt:
                            display_rows[possibility_row] += possibility_colour + str(possibility + 3 * possibility_row) + end_colour
                        else:
                            display_rows[possibility_row] += " "
                        if possibility == 1:
                            display_rows[possibility_row] += " "
                    display_rows[possibility_row] += " "
            if col_index in [0, 1, 3, 4, 6, 7]:
                for possibility_row in range(3):
                    display_rows[possibility_row] += "|"
            elif col_index in [2, 5]:
                for possibility_row in range(3):
                    display_rows[possibility_row] += shade_grid_separators + " " + end_colour
        for display in display_rows:
            print(display)